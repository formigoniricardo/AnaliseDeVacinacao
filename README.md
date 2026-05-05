#  AnaliseDeVacinacao - Monitor de Hiatos Imunológicos (ES)

**Projeto Integrador III - Aplicações de Ciência de Dados**  
**Curso:** Tecnologia em Análise e Desenvolvimento de Sistemas (TADS)  
**Instituição:** FAESA  

---

##  Sobre o Projeto
Desenvolvimento de uma **Aplicação Web (Dashboard)** voltada para a Ciência de Dados que permite a visualização de indicadores e KPIs sobre a vacinação de rotina no estado do Espírito Santo. 

O sistema transforma dados brutos extraídos do DATASUS (TABNET) em inteligência geográfica, identificando visualmente "hiatos imunológicos" — municípios com taxas de cobertura abaixo da meta de segurança (95%) estipulada pelo Ministério da Saúde para vacinas infantis cruciais, como BCG e Poliomielite.

###  Funcionalidades Principais
* **ETL Automatizado:** Script em Python para limpeza, transformação e normalização de dados do DATASUS.
* **Mapa de Calor Interativo:** Visualização geográfica por município para detecção rápida de abandono vacinal.
* **Ranking de Hiatos:** Gráfico isolando os 20 municípios com as piores taxas de cobertura para direcionamento de campanhas.
* **KPIs de Desempenho:** Indicadores que cruzam doses aplicadas com estimativas de população alvo.

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.11+
* **Interface Web:** Streamlit
* **Manipulação de Dados:** Pandas, NumPy
* **Visualização de Dados:** Plotly Express

---

##  Como Executar o Projeto Localmente

Siga as instruções abaixo para rodar o projeto na sua máquina:

### 1. Pré-requisitos
Certifique-se de ter o Python instalado. Clone este repositório e instale as bibliotecas necessárias executando o comando no terminal:
`pip install streamlit pandas numpy plotly`

### 2. Passo a Passo de Execução

**Etapa 1: Processamento de Dados (ETL)**
Antes de abrir o dashboard, é necessário gerar a base de dados tratada. Coloque os arquivos brutos do DATASUS (`BCG.csv` e `Poliomielite.csv`) na raiz do projeto e rode:
`python etl.py`
*Isso irá limpar os dados, calcular as porcentagens reais e gerar o arquivo `dados_vacinacao_es.csv`.*

**Etapa 2: Iniciando o Dashboard**
Com os dados processados, inicie a aplicação Web com o comando:
`python -m streamlit run app.py`
*O painel abrirá automaticamente no seu navegador padrão no endereço `http://localhost:8501`.*

---

##  Estrutura de Arquivos
* `app.py`: Arquivo principal da aplicação Web (Streamlit). Contém a interface, mapas e gráficos.
* `etl.py`: Pipeline de Extração, Transformação e Carga. Limpa os dados do TABNET e gera as coordenadas geográficas.
* `dados_vacinacao_es.csv`: Tabela final gerada pelo ETL e consumida pelo Dashboard. *(Gerado localmente)*

---

## 👥 Equipe Desenvolvedora
* Ricardo Formigoni
* Addriel Teixeira
* Gabriel Moreira
* Renato Oliveira

---

##  Plano de Trabalho (Cronograma)
| Entrega | Prazo | Descrição | Status |
| :--- | :--- | :--- | :---: |
| **Entrega 1** | 01/04 a 05/04 | Relatório de escopo, justificativa e metodologia. | ✅ Concluído |
| **Entrega 2** | 06/05 a 10/05 | Protótipo funcional e análise preliminar de dados (Vídeo MVP). | 🔄 Em andamento |
| **Entrega 3** | 17/06 a 21/06 | Produto Final e documentação técnica completa. | ⏳ Pendente |
