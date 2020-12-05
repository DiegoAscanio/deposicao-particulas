from matplotlib import pyplot
from matplotlib.colors import ListedColormap
import matplotlib._color_data as mcd
import pdb
import numpy as np

def plotar_interface(titulo, interface):
    pyplot.matshow(interface, cmap = ListedColormap(['w', 'k']))
    pyplot.title(titulo)
    pyplot.show()
    
def plotar_instantaneos(titulo, interface, instantaneos, t_comutacao = 25):
    comutar_cor = lambda cor: 'w' if cor == 'k' else 'k'
    pyplot.title(titulo)
    cor = 'k'
    for instantaneo, t in zip(instantaneos, range(len(instantaneos))):
        pyplot.plot(instantaneo, cor + '.')
        if t % t_comutacao == 0: # hora de comutar a cor
            cor = comutar_cor(cor)
    pyplot.plot(interface, cor + '.')
    pyplot.show()
    
def plotar_rugosidades(titulo, rugosidades):
    pyplot.title(titulo)
    for rugosidade in rugosidades:
        pyplot.plot(rugosidade)
    pyplot.show()