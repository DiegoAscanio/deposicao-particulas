cimport cython
cimport numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
cdef _executar_relaxamento_superficial(np.ndarray[int, ndim=1] altura_sitios, np.ndarray[int, ndim=1] sequencia_sitios, int L):
    cdef int i, sitio, esquerda = 0, direita = L - 1
    cdef np.ndarray[int, ndim = 1] resultante = altura_sitios
    for i in range(L):
        sitio = sequencia_sitios[i]
        if sitio > 0:
            esquerda = sitio - 1
        if sitio < L - 1:
            direita = sitio + 1
        if altura_sitios[direita] < altura_sitios[sitio]:
            sitio = direita
        if altura_sitios[esquerda] < altura_sitios[sitio]:
            sitio = esquerda
        resultante[sitio] = resultante[sitio] + 1 
    return resultante


@cython.boundscheck(False)
@cython.wraparound(False)
def executar_relaxamento_superficial(np.ndarray[int, ndim=1] altura_sitios, np.ndarray[int, ndim=1] sequencia_sitios, int L):
    cdef np.ndarray[int, ndim = 1] resultante = _executar_relaxamento_superficial(altura_sitios, sequencia_sitios, L)
    return resultante
