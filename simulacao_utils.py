from matplotlib import pyplot
from matplotlib.colors import ListedColormap
import matplotlib._color_data as mcd
import pdb
import numpy as np

def plotar_interface(titulo, interface, cmap = ListedColormap(['white', 'black'])):
    pyplot.matshow(interface, cmap = cmap)
    pyplot.title(titulo)
    pyplot.show()
    
comutar_representacao = lambda r: 'w-' if r == 'k-' else 'k-'
    
def plotar_instantaneos(titulo, interface, instantaneos, t_comutacao = 25, comutar_representacao = comutar_representacao):
    pyplot.title(titulo)
    representacao = comutar_representacao(None)
    for instantaneo, t in zip(instantaneos, range(len(instantaneos))):
        pyplot.plot(instantaneo, representacao)
        if t % t_comutacao == 0: # hora de comutar a cor
            representacao = comutar_representacao(representacao)
    pyplot.show()
    
def plotar_rugosidades(titulo, rugosidades, comprimentos_subestratos, logscale = False, colapso = False):
    pyplot.title(titulo)
    if logscale:
        pyplot.xscale('log')
        pyplot.yscale('log')
    for rugosidade, L in zip(rugosidades, comprimentos_subestratos):
        if rugosidade.shape[0] == 2:
            x, y = rugosidade[1], rugosidade[0]
        else:
            y = rugosidade
            x = np.arange(rugosidade.shape[0])
        if colapso:
            x = x / np.power(L, 2)
            y = y / np.power(L, 1/2)
        pyplot.plot(x, y, '-', label = 'L: {}'.format(L))
    pyplot.legend()
    pyplot.show()