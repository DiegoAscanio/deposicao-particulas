# Deposicao de Particulas

Repositório Para Trabalho Final da Disciplina de Princípios de Modelagem Matemática Computacional - MMC CEFET-MG.

Simulação de fenômenos de deposição de partículas

## Deposição Aleatória
## Deposição Aleatória com Relaxamento Superficial
## Deposição Balística

# Instruções de Instalação
1. Criar Ambiente Virtual Python Separadamente
```
$ virtualenv3 venv3 # criar ambiente
$ source venv3/bin/activate # ativar ambiente - executar todas as vezes que simular
```
2. Instalar Dependências
```
$ pip install -r requirements.txt
```

3. Compilar Deposições Balística e Aleatória Com Relaxação Superficial
```
$ make
```

4. Iniciar Jupyter Lab
```
$ jupyter lab
```

Para executar a Simulação de Deposições de Exemplo de Mattos(2005), presentes no capítulo 2, abrir o arquivo **simulacao_experimentos_crescimento_interfaces_thiago_mattos.ipynb** e executar as células deste notebook.  

Para simular outras deposições, abrir o arquivo **executar_simulacoes.ipynb**, descomentar o tipo de deposição desejada, configurar o número de núcleos de processamento disponíveis, a quantidade de amostras (sempre multipla do numero de nucleos de processamento disponiveis), o tempo minimo de simulação, os comprimentos de substratos a erem simulados, a quantidade de janelas para armazenar os snapshots e execute as células do notebok.  

Para plotar as simulações, abrir o arquivo **plotar_simulacoes_e_estimar_parametros.ipynb**, descomentar o tipo de deposição desejada, configurar os comprimentos dos substratos a serem plotados e executar as células do notebook.  

Por padrão, os scripts **executar_simulacoes** e **plotar_simulacoes** já vêm pré-configurados para simular (e plotar) deposições aleatórias com relaxação superficial de 128 amostras de substratos de tamanho ***L = [200, 400]*** que demandam menos de 30 minutos para serem simulados.  

Em testes executados em um processador core i5 (4 núcleos) de 5ª geração, a simualção de 128 amostras de tamanho ***L = 1600*** demandou 3800 segundos (ou pouco mais de 1 hora e 3 minutos).
