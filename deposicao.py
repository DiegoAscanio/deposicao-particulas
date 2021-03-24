import numpy as np
import pdb
import time
from db_utils import executar_deposicao_balistica
from dars_utils import executar_relaxamento_superficial
from da_utils import quick_add_at

class Deposicao(object):
    
    def _depositar_particula(self, t):
        pass
    
    def _depositar_particulas(self, t): # vetorizado - mais eficiente
        pass
    
    def _sortear_sitio(self):
        return self.rng.rng(high = self.L)[0]
    
    def _sortear_sitios(self):
        return self.rng.rng(high = self.L, numbers = self.L)
    
    def __init__(self, instancia, L, rng, tempo_maximo = 1000, snapshots = None):
        self.instancia = instancia
        self.L = np.int32(L)
        self.rng = rng
        self.tempo_maximo = tempo_maximo
        self.snapshots = snapshots if snapshots != None else tempo_maximo
        self.periodo_das_amostras = self.tempo_maximo // self.snapshots
        self.altura_interface = np.zeros(L, dtype = np.int32)
        self.altura_sitios = np.zeros((self.snapshots, L), dtype = np.int32)
        self.interface = [np.zeros(self.L, dtype = np.bool8)]
        self.instantaneos = {}
    
    def altura_sitio(self, i, t = None):
        if t != None:
            return self.altura_sitios[t // self.periodo_das_amostras][i]
        else:
            return self.altura_sitios[self.snapshots - 1][i]
    
    def __simular(self):
        for t in range(self.tempo_maximo):
            self._depositar_particulas(t)
    
    def __simular_com_detalhamento(self):
        begin = time.time()
        for t in range(self.tempo_maximo):
            if t % (self.tempo_maximo / 20) == 0:
                print('Instancia {}, {}%, {:.2f}s'.format(self.instancia,
                                                         (t * 100) / self.tempo_maximo,
                                                          time.time() - begin))
            self._depositar_particulas(t)
        print('Instancia {}, {}%, {:.2f}s'.format(self.instancia,
                                                  100,
                                                  time.time() - begin))

    def simular(self, verbose = True):
        if verbose:
            self.__simular_com_detalhamento()
        else:
            self.__simular()
        return self.altura_interface
    
    def __construir_interface_com_detalhamento(self):
        for t in range(self.tempo_maximo):
            if t % (self.tempo_maximo / 20) == 0:
                print('{}%'.format((t * 100) / self.tempo_maximo), end = '   ')
            self.instantaneos[t] = np.array(self.interface[-1])
            for l in range(self.L):
                self._depositar_particula(t)
        print()
        return self.interface
    
    def __construir_interface(self):
        for t in range(self.tempo_maximo):
            for l in range(self.L):
                self._depositar_particula(t)
        return self.interface
    
    def construir_interface(self, processo_detalhado = False):
        if processo_detalhado:
            return self.__construir_interface_com_detalhamento()
        else:
            return self.__construir_interface()
    
    def altura_media(self, t = None):
        if t != None:
            return np.mean([self.altura_sitios[t][i] for i in range(self.L)])
        else:
            return [self.altura_media(t) for t in range(self.snapshots)]
    
    def __desvio_quadratico_medio_distribuicao_alturas(self, t = None):
        if t != None:
            return np.var(self.altura_sitios[t])
        else:
            return np.array([self.__desvio_quadratico_medio_distribuicao_alturas(t) for t in range(self.snapshots)])
    
    def rugosidade(self, t = None):
        if t != None:
            return self.__desvio_quadratico_medio_distribuicao_alturas(t)
        else:
            return np.sqrt(np.array([self.rugosidade(t) for t in range(self.snapshots)]))
    
    def __momento(self, ordem, t):
        momento = lambda x, mu, n: (x - mu) ** n
        momento = np.vectorize(momento)
        if t != None:
            return np.mean(momento([self.altura_sitios[t][i] for i in range(self.L)], self.altura_media(t), ordem))
        else:
            return np.array([self.__momento(t) for t in range(self.snapshots)])
    
    def assimetria(self, t):
        if t != None:
            return self.__momento(3, t) / np.power(self.momento(2, t), 3/2)
        else:
            return np.array([self.assimetria(t) for t in range(self.snapshots)])
    
    def curtose(self, t):
        if t != None:
            return self.__momento(4, t) / np.power(self.momento(2, t), 2)
        else:
            return np.array([self.curtose(t) for t in range(self.snapshots)])
        
class DeposicaoAleatoria(Deposicao):
    
    def __init__(self, instancia, L, rng, tempo_maximo = 1000, snapshots = None):
        super().__init__(instancia, L, rng, tempo_maximo = tempo_maximo, snapshots = snapshots)
        self.quick_add_at = quick_add_at
    
    def _depositar_particula(self, t):
        t_ = t // self.periodo_das_amostras
        indice_sitio = self._sortear_sitio()
        altura_particula = self.altura_sitios[t_][indice_sitio]
        if altura_particula >= len(self.interface): # incrementar a interface com zeros
            self.interface.append(np.zeros(self.L, dtype = np.bool8))
        self.interface[altura_particula][indice_sitio] = 1
        
        # atualiza a altura da particula nos instantes posteriores
        # de tempo
        self.altura_sitios[t_:,indice_sitio] += 1
    
    def _depositar_particulas(self, t):
        t_ = t // self.periodo_das_amostras
        self.altura_sitios[t_] = self.altura_interface
        indices_sitios = np.int32(self._sortear_sitios())
        np.add.at(self.altura_interface, indices_sitios, 1)
    
class DeposicaoAleatoriaRelaxacaoSuperficial(Deposicao):
    
    def __init__(self, instancia, L, rng, tempo_maximo = 1000, snapshots = None):
        super().__init__(instancia, L, rng, tempo_maximo = tempo_maximo, snapshots = snapshots)
        self.executar_relaxamento_superficial = executar_relaxamento_superficial

    def _depositar_particula(self, t):
        t_ = t // self.periodo_das_amostras
        sitio = self._sortear_sitio()
        esquerda = max(sitio - 1, sitio * (sitio == 0))
        direita = max(sitio, (sitio + 1) * (sitio != (self.L - 1)))
        if self.altura_sitios[t_][direita] < self.altura_sitios[t_][sitio]:
            sitio = direita
        if self.altura_sitios[t_][esquerda] < self.altura_sitios[t_][sitio]:
            sitio = esquerda
        altura_particula = self.altura_sitios[t][sitio] = self.altura_sitios[t][sitio] + 1
        if altura_particula >= len(self.interface): # incrementar a interface com zeros
            self.interface.append(np.zeros(self.L, dtype = np.bool8))
        self.interface[altura_particula - 1][sitio] = 1
        
        # atualiza a altura da particula nos instantes posteriores
        # de tempo
        self.altura_sitios[t_:,sitio] = altura_particula
        
    def _depositar_particulas(self, t):
        t_ = t // self.periodo_das_amostras
        self.altura_sitios[t_] = self.altura_interface
        indices_sitios = np.int32(self._sortear_sitios())
        self.altura_interface = self.executar_relaxamento_superficial(self.altura_interface, indices_sitios, self.L)
        
class DeposicaoBalistica(Deposicao):

    def __init__(self, instancia, L, rng, tempo_maximo = 1000, snapshots = None):
        super().__init__(instancia, L, rng, tempo_maximo = tempo_maximo, snapshots = snapshots)   
        self.executar_deposicao_balistica = executar_deposicao_balistica
    
    def _depositar_particula(self, t):
        t_ = t // self.periodo_das_amostras
        sitio = self._sortear_sitio()
        esquerda = max(sitio - 1, sitio * (sitio == 0))
        direita = max(sitio, (sitio + 1) * (sitio != (self.L - 1)))
        altura_particula = self.altura_sitios[t_][sitio] + 1
        if self.altura_sitios[t_][esquerda] > altura_particula:
            altura_particula = self.altura_sitios[t_][esquerda]
        if self.altura_sitios[t_][direita] > altura_particula:
            altura_particula = self.altura_sitios[t_][direita]
            
        if altura_particula >= len(self.interface): # incrementar a interface com zeros
            self.interface.append(np.zeros(self.L, dtype = np.bool8))
        self.interface[altura_particula - 1][sitio] = 1
        
        # atualiza a altura da particula nos instantes posteriores
        # de tempo
        self.altura_sitios[t_:,sitio] = altura_particula
    
    def _depositar_particulas(self, t):
        t_ = t // self.periodo_das_amostras
        self.altura_sitios[t_] = self.altura_interface
        indices_sitios = np.int32(self._sortear_sitios())
        self.altura_interface = self.executar_deposicao_balistica(self.altura_interface, indices_sitios, self.L)
