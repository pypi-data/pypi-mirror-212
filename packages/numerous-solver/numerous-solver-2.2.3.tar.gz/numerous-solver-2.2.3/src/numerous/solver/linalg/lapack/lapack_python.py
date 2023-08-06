import numba.extending as nbe
import ctypes
import numpy as np

dpotrf_addr = nbe.get_cython_function_address('scipy.linalg.cython_lapack', 'dpotrf') # cholesky decomposition
dtrsv_addr = nbe.get_cython_function_address('scipy.linalg.cython_blas', 'dtrsv') # solve Ax=b
dgetrf_addr= nbe.get_cython_function_address('scipy.linalg.cython_lapack', 'dgetrf')
dgetrs_addr = nbe.get_cython_function_address('scipy.linalg.cython_lapack', 'dgetrs')

dpotrf_cfunc = ctypes.CFUNCTYPE(ctypes.c_int,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p)

dtrsv_cfunc = ctypes.CFUNCTYPE(ctypes.c_int,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p)

dgetrf_cfunc = ctypes.CFUNCTYPE(ctypes.c_int,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p)

dgetrs_cfunc = ctypes.CFUNCTYPE(ctypes.c_int,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                ctypes.c_void_p,
                                )

dpotrf_fun = dpotrf_cfunc(dpotrf_addr)
dtrsv_fun = dtrsv_cfunc(dtrsv_addr)
dgetrf_fun = dgetrf_cfunc(dgetrf_addr)
dgetrs_fun = dgetrs_cfunc(dgetrs_addr)

def lapack_solve_triangular(Lalloc, balloc, N):
    """solves the linalg equation A*x=L*L**T*x=b, where L is the lower cholesky decomposed matrix of A

    :param Lalloc: Lower triangle matrix after cholesky decomposition of positive-definite matrix A
    :param balloc: Right hand side of equation system
    :param N: Number of right hand sides
    :return: returns the content of balloc which has been modified to contain the solution x
    """


    side_a = np.empty(1, dtype=np.int32)
    side_a[0] = 76  # L
    t_a = np.empty(1, dtype=np.int32)
    t_a[0] = 78 # N - solve L*x=b and not L**T*x=b
    diag_a = np.empty(1, dtype=np.int32)
    diag_a[0] = 78
    N_a = np.empty(1, dtype=np.int32)
    N_a[0] = N
    lda_a = np.empty(1, dtype=np.int32)
    lda_a[0] = N
    incx_a = np.empty(1, dtype=np.int32)
    incx_a[0] = 1

    # forward substitution using Lower diagonal matrix L*y = b, solves for y
    dtrsv_fun(side_a.ctypes,
              t_a.ctypes,
              diag_a.ctypes,
              N_a.ctypes,
              Lalloc.ctypes,
              lda_a.ctypes,
              balloc.ctypes,
              incx_a.ctypes
              )

    #side_a[0] = 85 # U
    t_a[0] = 84 # T - since the matrix L**T is the upper matrix
    #t_a[0] = 78 # T

    # backward substitution using upper diagonal matrix U*x=y, solves for x
    dtrsv_fun(side_a.ctypes,
              t_a.ctypes,
              diag_a.ctypes,
              N_a.ctypes,
              Lalloc.ctypes,
              lda_a.ctypes,
              balloc.ctypes,
              incx_a.ctypes
              )

    return balloc


def lapack_cholesky(side, N, xalloc):
    """Cholesky decomposition of a square positive-definite matrix.

    :param side: The side of the square matrix (lower/upper). Use 76 for lower and 85 for upper.
    :type side: int
    :param N: Order of matrix - the dimension of the NxN matrix
    :type N: int
    :param xalloc: The NxN positive-definite matrix
    :type xalloc: :class:`np.ndarray` NxN
    :return:
    """
    xalloc = xalloc.T
    N_a = np.empty(1, dtype=np.int32)
    N_a[0] = N
    side_a = np.empty(1, dtype=np.int32)
    side_a[0] = side
    z_a = np.empty(1, dtype=np.int32)
    z_a[0] = 1

    dpotrf_fun(side_a.ctypes, N_a.ctypes, xalloc.ctypes, N_a.ctypes, z_a.ctypes)

    # return xalloc, containing the Lower cholesky decomposed matrix of xalloc stored in fortran order.
    # To get the actual lower matrix, transpose xalloc, but know that this slows down all subsequent code for some
    # reason

    return xalloc


def lu_factor(a) -> [np.array, np.array]:
    a_ = np.asfortranarray(a)
    m_ = np.empty(1, dtype=np.int32)
    m_[0] = a_.shape[0]
    n_ = np.empty(1, dtype=np.int32)
    n_[0] = a_.shape[1]
    lda_ = np.empty(1, np.int32)
    lda_[0] = a_.shape[0]

    ipiv = np.empty(min(m_[0], n_[0]), dtype=np.int32)
    info = np.empty(1, dtype=np.int32)
    info[0] = 1

    dgetrf_fun(m_.ctypes, n_.ctypes, a_.ctypes, m_.ctypes, ipiv.ctypes, info.ctypes)

    return np.asfortranarray(a_), ipiv


def lu_solve(a: np.array, piv: np.array, b: np.array) -> np.array:
    a_ = a
    b_ = b
    piv_ = piv
    trans_ = np.empty(1, dtype=np.int32)
    trans_[0] = 78 # 78: 'N', 84: 'T', 67: 'C'
    n_ = np.empty(1, dtype=np.int32)
    n_[0] = a_.shape[0]
    nrhs_ = np.empty(1, dtype=np.int32)
    nrhs_[0] = b_.shape[1]
    lda_ = np.empty(1, dtype=np.int32)
    lda_[0] = a_.shape[0]
    ldb_ = np.empty(1, dtype=np.int32)
    ldb_[0] = b_.shape[0]
    info = np.empty(1, dtype=np.int32)
    info[0] = 2

    dgetrs_fun(trans_.ctypes, n_.ctypes, nrhs_.ctypes, a_.ctypes, lda_.ctypes, piv_.ctypes, b_.ctypes, ldb_.ctypes,
               info.ctypes)

    return b_
