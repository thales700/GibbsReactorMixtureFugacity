# GibbsReactorMixtureFugacity

Este repositório contém o código-fonte de uma ferramenta computacional para simulação de equilíbrio químico, desenvolvida como parte de uma dissertação de mestrado sobre o acoplamento de reatores de reforma de biogás.

O software utiliza a abordagem de minimização direta da energia livre de Gibbs para determinar a composição de equilíbrio de sistemas reacionais complexos, com foco em reações na fase gás.

## Principais Funcionalidades

* **Minimização de Gibbs:** Utiliza o método de minimização da energia livre de Gibbs, uma abordagem robusta que não requer a especificação prévia de reações independentes.
* **Arquitetura Modular (POO):** Projetado com princípios de Programação Orientada a Objetos para alta flexibilidade, manutenção e extensibilidade.
* **Base de Dados Extensível:** Permite que o usuário adicione facilmente novas espécies químicas editando um único arquivo de banco de dados.
* **Suporte a Fases:** O modelo atual suporta sistemas com múltiplas espécies na fase gás e um único componente na fase sólida (ex: Carbono).
* **Cálculo de Não-Idealidade:** Inclui módulos para o cálculo de fugacidade utilizando a Equação de Estado de Peng-Robinson, permitindo a análise de sistemas em pressões elevadas.

## Arquitetura do Projeto

O código é organizado em módulos com responsabilidades bem definidas:

├── Reforma/
│   ├── ReatorDeGibbs/
│   │   └── GibbsMinimization.py           # <-- Módulo principal com o otimizador
│   ├── Molecula/
│   │   ├── Molecula.py                    # <-- Classe principal que define uma espécie
│   │   └── DataBase.py                    # <-- BANCO DE DADOS para adicionar/editar moléculas
│   ├── ConstanteDeEquilibrio/
│   │   └── ConstanteDeEquilibrio.py       # <-- Calcula propriedades termodinâmicas (dG, dH)
│   └── Fugacidade/
│       ├── PengRobinsonPuro.py            # <-- Fugacidade de componentes puros
│       └── FugacidadeMisturaPengRobinson.py # <-- Coeficientes de fugacidade em misturas
│
├── FirstReactor.py                        # <-- Exemplo de script para simular o 1º reator
└── SecondReactor.py                       # <-- Exemplo de script para simular o reator acoplado

## Como Começar

Siga os passos abaixo para configurar o ambiente e executar uma simulação.

### Pré-requisitos

* Python 3.8 ou superior

### Instalação

1.  **Clone o repositório:**
    ```sh
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```sh
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    Crie um arquivo `requirements.txt` com o seguinte conteúdo e execute o comando de instalação.

    **requirements.txt:**
    ```txt
    numpy
    scipy
    pandas
    tables
    matplotlib
    joblib
    ```

    **Comando de instalação:**
    ```sh
    pip install -r requirements.txt
    ```

## Como Utilizar

A execução de uma simulação é feita através de um script "driver", como o `FirstReactor.py`. O processo é o seguinte:

1.  **Verificar/Adicionar Moléculas:** Abra o arquivo `Reforma/Molecula/DataBase.py`. Se a sua simulação necessita de uma molécula que não está listada, adicione-a seguindo o padrão existente.

2.  **Configurar a Simulação:** Abra um script driver (ex: `FirstReactor.py`) e edite as seguintes seções:
    * **`nomeMoleculas` e `moleculas`:** Liste as moléculas que participarão da reação.
    * **`molsIniciais`:** Defina a composição molar da alimentação do reator.
    * **`Temperatures` e `Pressao`:** Defina as condições operacionais a serem simuladas.

3.  **Executar o Código:**
    ```sh
    python FirstReactor.py
    ```
    O script irá executar a simulação e salvar os resultados em um arquivo (por padrão, `.h5`), que pode ser facilmente lido com a biblioteca `Pandas`.

## Extensibilidade e Possibilidades Futuras

A arquitetura modular da ferramenta permite diversas expansões.

### Ativando o Cálculo de Fugacidade (Não-Idealidade)

O framework já possui os módulos para o cálculo de fugacidade pela Equação de Estado de Peng-Robinson. Na implementação atual em `GibbsMinimization.py`, o coeficiente de fugacidade ($$\phi_i$$) está simplificado para `1` (comportamento ideal).

Para ativar o cálculo rigoroso, o usuário pode modificar a função `SystemToMinimize` em `GibbsMinimization.py`:

1.  **Chamar a função de fugacidade:** Antes do laço de cálculo da energia de Gibbs, chame a função para calcular os coeficientes de fugacidade da mistura.
    ```python
    # Dentro de SystemToMinimize(molsFinal:list):
    ...
    # Atualiza as frações molares primeiro
    for molFinal, molecula in zip(molsFinal, moleculas):
        # ... lógica de atualização ...

    # CHAME A FUNÇÃO AQUI:
    FugacidadeMisturaPengRobinson(Temperatura, Pressao, moleculas)
    ```

2.  **Utilizar o coeficiente de fugacidade no cálculo de Gibbs:** Modifique a linha que calcula a energia livre de Gibbs para incluir o `molecula.fugacidade`.
    ```python
    # Altere a linha do dGibbsReactions:
    dGibbsReactions += molFinal * (molecula.dGFormacaoReal + R * Temperatura * np.log(molecula.fracaoMolar * Pressao * molecula.fugacidade))
    ```

### Implementando Outros Modelos Termodinâmicos

Devido à modularidade, é possível implementar outras equações de estado (ex: Soave-Redlich-Kwong). Para isso, bastaria criar um novo módulo dentro da pasta `Fugacidade/` e substituir a chamada da função `FugacidadeMisturaPengRobinson` pela nova implementação.

## Como Citar este Trabalho

Se você utilizar este código em sua pesquisa, por favor, cite a dissertação original.

**Exemplo de citação (formato BibTeX):**
```bibtex
@mastersthesis{Sobrinho2025,
  author  = {Thales Uchoa da Costa Sobrinho},
  title   = {Análise de Operabilidade da Produção de Gás de Síntese a Partir do Processo Sequencial de Reforma e Reforma a Vapor do Biogás},
  school  = {Programa de Pós-Graduação em Engenharia Química - Universidade Estadual do Oeste do Paraná - Campus Toledo},
  year    = {2025},
  address = {Toledo, Paraná},
}
