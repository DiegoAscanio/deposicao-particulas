from matplotlib import pyplot
from matplotlib.colors import ListedColormap
import matplotlib._color_data as mcd
import pdb
import numpy as np

def plotar_interface(titulo, interface):
    pyplot.matshow(interface, cmap = ListedColormap(['w', 'k']))
    pyplot.title(titulo)
    pyplot.show()
    
comutar_representacao = lambda r: 'w.' if r == 'k.' else 'k.'
    
def plotar_instantaneos(titulo, interface, instantaneos, t_comutacao = 25, comutar_representacao = comutar_representacao):
    pyplot.title(titulo)
    representacao = comutar_representacao(None)
    for instantaneo, t in zip(instantaneos, range(len(instantaneos))):
        pyplot.plot(instantaneo, representacao)
        if t % t_comutacao == 0: # hora de comutar a cor
            representacao = comutar_representacao(representacao)
    representacao = comutar_representacao(representacao)
    pyplot.plot(interface, representacao)
    pyplot.show()
    
def plotar_rugosidades(titulo, rugosidades, comprimentos_subestratos, logscale = False):
    pyplot.title(titulo)
    if logscale:
        pyplot.xscale('log')
        pyplot.yscale('log')
    for rugosidade, L in zip(rugosidades, comprimentos_subestratos):
        if rugosidade.shape[0] == 2:
            pyplot.plot(rugosidade[1], rugosidade[0], '-', label = 'L: {}'.format(L))
        else:
            pyplot.plot(rugosidade)
    pyplot.legend()
    pyplot.show()