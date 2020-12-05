import numpy as np
import pdb

class Deposicao(object):
    
    def _sortear_sitio(self, t):
        pass
    
    def _depositar_particula(self, t):
        pass
    
    def _simular_deposicao(self, t):
        pass
    
    def __init__(self, L, rng, tempo_maximo = 1000):
        self.L = L
        self.interface = []
        self.altura_interface = np.zeros(L, dtype = np.uint32)
        self.rng = rng
        self.tempo_maximo = tempo_maximo
        self.instantaneos = {}
        self.altura_sitios = np.zeros((tempo_maximo, L), dtype = np.uint32)
    
    def altura_sitio(self, i, t = None):
        if t != None:
            return self.altura_sitios[t][i]
        else:
            return self.altura_sitios[self.tempo_maximo - 1][i]
    
    def __simular_com_detalhamento(self, sequencia_de_sitios = None):
        L_deposicoes = 

    def simular(self, verbose = True):
        self.interface = [np.zeros(self.L, dtype = np.bool8)]
        for t in range(self.tempo_maximo):
            if t % (self.tempo_maximo / 20) == 0 and verbose:
                print('{}%'.format((t * 100) / self.tempo_maximo), end = '   ')
            self.instantaneos[t] = np.array(self.interface[-1])
            for l in range(self.L):
                self._depositar_particula(t)
        if verbose:
            print()
        return self.interface, self.instantaneos
    
    def __construir_interface_com_detalhamento(self):
        self.interface = [np.zeros(self.L, dtype = np.bool8)]
        for t in range(self.tempo_maximo):
            if t % (self.tempo_maximo / 20) == 0:
                print('{}%'.format((t * 100) / self.tempo_maximo), end = '   ')
            self.instantaneos[t] = np.array(self.interface[-1])
            for l in range(self.L):
                self._depositar_particula(t)
        print()
        return self.interface, self.instantaneos
    
    def __construir_interface(self):
        self.interface = [np.zeros(self.L, dtype = np.bool8)]
        for t in range(self.tempo_maximo):
            self.instantaneos[t] = np.array(self.interface[-1])
            for l in range(self.L):
                self._depositar_particula(t)
        return self.interface, self.instantaneos
    
    def construir_interface(self, processo_detalhado = False):
        if processo_detalhado:
            return self.__construir_interface_com_detalhamento()
        else:
            return self.__construir_interface()
    
    def altura_media(self, t = None):
        if t != None:
            return np.mean([self.altura_sitios[t][i] for i in range(self.L)])
        else:
            return [self.altura_media(t) for t in range(self.tempo_maximo)]
    
    def __desvio_quadratico_medio_distribuicao_alturas(self, t = None):
        variancia = lambda x, mu: (x - mu) ** 2
        variancia = np.vectorize(variancia)
        if t != None:
            return np.mean(variancia([self.altura_sitios[t][i] for i in range(self.L)], self.altura_media(t)))
        else:
            return [self.__desvio_quadratico_medio_distribuicao_alturas(t) for t in range(self.tempo_maximo)]
    
    def rugosidade(self, t = None):
        if t != None:
            return self.__desvio_quadratico_medio_distribuicao_alturas(t)
        else:
            return [self.rugosidade(t) for t in range(self.tempo_maximo)]
    
    def __momento(self, ordem, t):
        momento = lambda x, mu, n: (x - mu) ** n
        momento = np.vectorize(momento)
        if t != None:
            return np.mean(momento([self.altura_sitios[t][i] for i in range(self.L)], self.altura_media(t), ordem))
        else:
            return [self.__momento(t) for t in range(self.tempo_maximo)]
    
    def assimetria(self, t):
        if t != None:
            return self.__momento(3, t) / np.power(self.momento(2, t), 3/2)
        else:
            return [self.assimetria(t) for t in range(self.tempo_maximo)]
    
    def curtose(self, t):
        if t != None:
            return self.__momento(4, t) / np.power(self.momento(2, t), 2)
        else:
            return [self.curtose(t) for t in range(self.tempo_maximo)]
        
class DeposicaoAleatoria(Deposicao):
    
    def __init__(self, L, rng, tempo_maximo = 1000):
        super().__init__(L, rng, tempo_maximo = tempo_maximo)
        
    def _sortear_sitio(self, t):
        return np.int32(np.abs(self.rng.rng()) * (self.L / 2**31))
    
    def _depositar_particula(self, t):
        indice_sitio = self._sortear_sitio(t)
        altura_particula = self.altura_sitios[t][indice_sitio]
        if altura_particula >= len(self.interface): # incrementar a interface com zeros
            self.interface.append(np.zeros(self.L, dtype = np.bool8))
        self.interface[altura_particula][indice_sitio] = 1
        
        # atualiza a altura da particula nos instantes posteriores
        # de tempo
        self.altura_sitios[t:,indice_sitio] = altura_particula + 1
    
class DeposicaoAleatoriaRelaxacaoSuperficial(DeposicaoAleatoria):
    
    def __init__(self, L, rng, tempo_maximo = 1000):
        super().__init__(L, rng, tempo_maximo = tempo_maximo)
        
    def _sortear_sitio(self, t):
        minimo = sitio = np.int32(np.abs(self.rng.rng()) * (self.L / 2**31))
        if sitio < self.L - 1:
            if self.altura_sitios[t][sitio + 1] < self.altura_sitios[t][minimo]:
                minimo = sitio + 1
        if sitio > 0:
            if self.altura_sitios[t][sitio - 1] < self.altura_sitios[t][minimo]:
                minimo = sitio - 1
        return minimo
        

class DeposicaoBalistica(DeposicaoAleatoria):
    
    def __init__(self, L, rng, tempo_maximo = 1000):
        super().__init__(L, rng, tempo_maximo = tempo_maximo)
        
    def _depositar_particula(self, t):
        indice_sitio = self._sortear_sitio(t)
        
        candidatos = {}
        if indice_sitio > 0:
            candidatos[self.altura_sitios[t][indice_sitio - 1]] = indice_sitio - 1
        candidatos[self.altura_sitios[t][indice_sitio]] = indice_sitio
        if indice_sitio < self.L - 1:
            candidatos[self.altura_sitios[t][indice_sitio + 1]] = indice_sitio + 1
            
        altura_particula = max(candidatos)
        if altura_particula >= len(self.interface): # incrementar a interface com zeros
            self.interface.append(np.zeros(self.L, dtype = np.bool8))
        self.interface[altura_particula - 1][indice_sitio] = 1
        
        # atualiza a altura da particula nos instantes posteriores
        # de tempo
        self.altura_sitios[t:,indice_sitio] = altura_particula + 1