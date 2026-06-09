# 📚 Documentação Técnica - Monitor de Hiatos Imunológicos

Este documento detalha a arquitetura do sistema, o fluxo de processamento de dados (Pipeline ETL), o dicionário de dados e as regras de negócio aplicadas no Projeto Integrador III.

---

## 1. Visão Geral da Arquitetura
A solução foi desenhada como um Produto de Dados (MVP) dividida em duas camadas principais: processamento em backend e renderização de interface (frontend/dashboard).

* **Linguagem Principal:** Python 3.11+
* **Camada de Dados (ETL):** A biblioteca `pandas` foi utilizada para ler, limpar, transformar (despivotar) e calcular métricas estatísticas, gerando uma base de dados analítica de alta performance estruturada em `.csv`.
* **Camada de Apresentação:** Construída com o framework `Streamlit` para renderização web reativa.
* **Motor Gráfico:** A biblioteca `plotly.express` aliada ao Mapbox (`carto-positron`) foi utilizada para a geração de visualizações geoespaciais e gráficos estatísticos imunes a sobreposição de elementos geométricos.

---

## 2. Pipeline de Dados (ETL)
O script `etl.py` é responsável por automatizar a preparação dos dados governamentais. O fluxo ocorre em três etapas:

1. **Extração (Extract):** Leitura iterativa dos arquivos brutos gerados via TABNET/DATASUS (`BCG.csv` e `Poliomielite.csv`), utilizando decodificação `latin1` para suporte a caracteres em português.
2. **Transformação (Transform):** * **Limpeza:** Remoção de colunas sintéticas ("Total") geradas automaticamente pela tabela dinâmica do Ministério da Saúde.
   * **Normalização Geométrica:** Aplicação da técnica de *Melt* (Unpivot) para converter colunas de datas em linhas, passando o dataset do formato *Wide* para *Long*, o que é exigido por ferramentas de BI e análise geoespacial.
   * **Enriquecimento:** Mapeamento de um dicionário estático contendo coordenadas geográficas (Lat/Lon) e estimativas de população alvo infantil para os 78 municípios capixabas.
3. **Carga (Load):** Consolidação dos dados filtrados e processados no arquivo final `dados_vacinacao_es.csv`, garantindo uma tipagem uniforme e segura para o carregamento em memória (cache) pelo Streamlit.

---

## 3. Regras de Negócio e Modelagem Matemática

Para transformar o dado bruto (número absoluto de vacinados) em uma métrica acionável de saúde pública, as seguintes regras foram estabelecidas na camada ETL e na interface:

### 3.1. Cálculo de Cobertura Vacinal
Não é estatisticamente viável dividir as doses aplicadas pela população geral do município para vacinas da primeira infância. O cálculo matemático aplicado segue a fórmula:
**Cobertura (%) = (Doses Aplicadas / Estimativa da População Alvo) * 100**
*Nota de Escopo:* Como a base de Nascidos Vivos (SINASC) necessitaria de um processamento temporal complexo para a Entrega 3, foi aplicada uma estimativa populacional constante baseada em médias para validação acadêmica do protótipo. Valores excedentes a 100% foram nivelados matematicamente (cap limit) para manter a padronização das escalas gráficas.

### 3.2. Categorização de Risco
O algoritmo aplica operadores lógicos para classificar cada município segundo as diretrizes de imunidade de rebanho do Ministério da Saúde, permitindo uma triagem visual imediata no aplicativo:
* 🟢 **Seguro (≥ 95%):** Município atingiu a meta oficial, possuindo barreira imunológica.
* 🟠 **Alerta (70% - 94%):** Município apresenta bolsões de vulnerabilidade. Requer campanhas locais.
* 🔴 **Crítico (< 70%):** Iminente risco de reintrodução de doenças erradicadas. Exige intervenção imediata da Secretaria de Saúde.

---

## 4. Dicionário de Dados
A tabela final processada (`dados_vacinacao_es.csv`) que alimenta o dashboard possui o seguinte schema:

| Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `ano` | Integer | Ano de referência da aplicação da vacina (2021, 2022). |
| `vacina` | String | Nome imunobiológico administrado (ex: BCG, Poliomielite). |
| `sigla_uf` | String | Sigla da unidade federativa (fixado em ES). |
| `municipio` | String | Nome padronizado do município capixaba (sem código IBGE). |
| `lat` | Float | Latitude geocodificada do centro do município. |
| `lon` | Float | Longitude geocodificada do centro do município. |
| `cobertura_vacinal` | Float | Percentual de alcance vacinal calculado na camada de transformação. |

---

## 5. Tratamento de Exceções e Resiliência
Para garantir a estabilidade da aplicação em ambiente de nuvem (Streamlit Cloud), o `app.py` possui travas de segurança estruturais:
* **Tratamento de Arquivo Inexistente:** Bloqueia a execução com logs visuais (UI Warnings) instruindo o usuário a rodar o pipeline ETL caso o CSV consolidado não seja encontrado.
* **Tipagem Forçada (Sanitization):** Conversão explícita de `strings` mal formatadas do DATASUS para `float` antes da renderização de gráficos, evitando falhas silenciosas de "Index Error" em agrupamentos do Pandas e do Plotly.
