# 🥗 Explorador de Nutrição Global

Um aplicativo interativo desenvolvido em Python com **Streamlit** que utiliza dados científicos reais da Tabela Brasileira de Composição de Alimentos (**TACO**). O sistema permite explorar o perfil nutricional de centenas de alimentos, aplicar filtros inteligentes de alérgenos e restrições personalizadas, além de simular o impacto de refeições diárias na dieta.

## ✨ Funcionalidades

- **Exploração de Dados Reais:** Leitura integrada e automática das bases de macronutrientes e minerais da TACO.
- **Filtros Avançados:** Busca textual instantânea por nome do alimento.
- **Segurança Alimentar:** Filtros rápidos para dietas **Sem Glúten** e **Sem Lactose* baseados em engenharia de texto.
- **Exclusão Personalizada:** Caixa de texto que permite ao usuário omitir da listagem qualquer ingrediente ou alergênio específico (ex: *suíno*, *amendoim*, *frango*), com um aviso visual nítido na tela quando o filtro está ativo.
- **Gráficos Dinâmicos:** Comparativo visual em barras dos macronutrientes (Carboidratos, Proteínas e Gorduras) ajustado automaticamente para o modo escuro.
- **Simulador de Refeições Diárias:** Painel para somar o peso consumido de múltiplos alimentos e calcular em tempo real o total de calorias e macronutrientes do dia, com persistência de dados em *Session State*.

## 📂 Estrutura do Projeto

O código foi cuidadosamente modularizado para garantir a organização e boas práticas de desenvolvimento:
```
├── app.py                      # Interface gráfica e controle de fluxo do Streamlit
├── leitura.py                  # Módulo responsável pela carga, junção e limpeza dos dados
├── taco-db-nutrientes.csv      # Base de dados principal (Macronutrientes)
└── taco-db-nutrientes-2.csv    # Base de dados secundária (Minerais/Extras)
```
## 🛡️ Técnicas de Blindagem de Dados Aplicadas

Durante o desenvolvimento, o projeto foi robustecido contra falhas comuns em análises de tabelas científicas:

- **Tratamento de Dados Não-Numéricos:** Células contendo marcas de "Traços" (Tr) ou dados ausentes (*) são automaticamente identificadas pelo Pandas e convertidas em 0.0, prevenindo erros de compilação em gráficos.

- **Junção Segura de Dados:** Limpeza de espaços invisíveis nas colunas (str.strip()) e tratamento de quebra de linhas problemáticas via on_bad_lines='skip'.

## 🚀 Como Executar o Projeto
Pré-requisitos

- Certifique-se de ter o Python 3.12+ instalado na sua máquina.

- É necessário ter os arquivos da plataforma Kaggle (https://www.kaggle.com/datasets/ispangler/composio-nutricional-de-alimentos-taco), salvos na mesma pasta do projeto.

1. Clonar ou Acessar a pasta do projeto
```
cd "Caminho/Ate/O/Seu/p_explorador_de_nutrição"
```

2. Ativar o Ambiente Virtual (Virtualenv)
Se estiver no Linux/macOS:
```
source .venv/bin/activate
```
Se estiver no Windows
```
.venv\Scripts\activate
```
3. Instalar as Dependências necessárias
Caso ainda não tenha instalado, instale as bibliotecas principais:
```
pip install streamlit pandas matplotlib
```
4. Rodar o Aplicativo
```
streamlit run app.py
```

O seu navegador abrirá o sistema automaticamente no endereço local http://localhost:8501.

##🛠️ Tecnologias Utilizadas

  Python (Linguagem base)

  Streamlit (Interface Web e Componentes de Tela)

  Pandas (Tratamento, Filtragem e Estruturação de dados)

  Matplotlib (Renderização e Customização de Gráficos)

--

Este projeto foi desenvolvido durante meus estudos de Dados, Arquitetura de Códigos e Modularização, Engenharia de Recursos, Tratamento de Exceções e Resolução de Conflitos de Compilação e Customização Avançada de Gráficos e Estética (Design).
