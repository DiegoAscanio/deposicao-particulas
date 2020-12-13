cimport cython
cimport numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
cdef _quick_add_at(np.ndarray[int, ndim=1] altura_sitios, np.ndarray[int, ndim=1] sequencia_sitios, int L):
    cdef int i, sitio, esquerda = 0, direita = L - 1
    cdef np.ndarray[int, ndim = 1] resultante = altura_sitios
    for i in range(L):
        sitio = sequencia_sitios[i]
        resultante[sitio] = resultante[sitio] + 1 
    return resultante


@cython.boundscheck(False)
@cython.wraparound(False)
def quick_add_at(np.ndarray[int, ndim=1] altura_sitios, np.ndarray[int, ndim=1] sequencia_sitios, int L):
    cdef np.ndarray[int, ndim = 1] resultante = _quick_add_at(altura_sitios, sequencia_sitios, L)
    return resultante
