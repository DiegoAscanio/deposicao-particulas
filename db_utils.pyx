cimport cython
cimport numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
cdef (int) calcular_altura_sitio(np.ndarray[int, ndim=1] altura_sitios, int sitio, int L):
    cdef int e = 0, d = L - 1, altura = altura_sitios[sitio] + 1
    # setar indice da esquerda e da direita
    if sitio > 0:
        e = sitio - 1
    if sitio < L - 1:
        d = sitio + 1
    if altura_sitios[e] > altura:
        altura = altura_sitios[e]
    if altura_sitios[d] > altura:
        altura = altura_sitios[d]
    return altura


@cython.boundscheck(False)
@cython.wraparound(False)
cdef _executar_deposicao_balistica(np.ndarray[int, ndim=1] altura_sitios, np.ndarray[int, ndim=1] sequencia_sitios, int L):
    cdef int i, sitio
    cdef np.ndarray[int, ndim = 1] resultante = altura_sitios
    for i in range(L):
        sitio = sequencia_sitios[i]
        resultante[sitio] = calcular_altura_sitio(resultante, sitio, L)
    return resultante


@cython.boundscheck(False)
@cython.wraparound(False)
def executar_deposicao_balistica(np.ndarray[int, ndim=1] altura_sitios, np.ndarray[int, ndim=1] sequencia_sitios, int L):
    cdef np.ndarray[int, ndim = 1] resultante = _executar_deposicao_balistica(altura_sitios, sequencia_sitios, L)
    return resultante
