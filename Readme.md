# Desafio Klike

## 📌 Visão geral

Este projeto foi desenvolvido como solução para o **take-home challenge da Klike**, simulando problemas reais de **análise de criativos em vídeo com IA, modelagem preditiva e geração de recomendações acionáveis**.

A entrega foi estruturada em **4 partes principais**, cobrindo desde exploração de dados até visão de produto.

---

## 📂 Estrutura do projeto

```text
klike_take_home/
│
├── notebook_analise.ipynb
├── recommendation_engine.py
├── klike_challenge_dataset.csv
├── README.md
├── requirements.txt
└── PRODUCT_VISION.md
```

* **notebook_analise.ipynb** → EDA, modelagem, testes e demonstração do protótipo.
* **recommendation_engine.py** → motor de recomendação modularizado.
* **dataset CSV** → base fornecida no challenge.
* **README.md** → visão geral da solução.

---

# ✅ Parte 1 — Análise Exploratória (EDA)

Foi realizada uma análise exploratória completa para entender:

* perfil geral dos dados
* distribuições
* valores faltantes
* padrões por plataforma
* sinais criativos com maior impacto na performance

### 🔍 Principais tratamentos

* Conversão da coluna `date` para datetime
* Missing numéricos preenchidos com **mediana**
* Missing categóricos preenchidos com **"unknown"**
* Preservação inicial de outliers por potencial valor de negócio

### 📊 Principais insights

* **Hook nos primeiros 3s** → +39.2% em CTR
* **CTA explícito** → +12.4% em conversões
* **Rosto humano** → +25% em retenção
* **TikTok** → maior ROAS e forte aderência a vídeos verticais
* **LinkedIn** → maior watch time e melhor aderência a horizontal

---

# 🤖 Parte 2 — Modelagem Preditiva

Foi desenvolvido um modelo de regressão para prever o **`klike_score`**.

## 🧠 Feature engineering

As features foram organizadas em três grupos:

### 🎬 Criativo

* duração
* formato
* subtitle
* CTA
* hook
* face
* densidade de texto
* relação música/voz

### 📱 Contexto

* plataforma
* categoria
* objetivo
* público

### 📈 Performance

* CTR
* CPC
* conversões
* ROAS
* watch time
* engagement

### ⭐ Features derivadas

* `watch_rate`
* `revenue_per_conversion`

## 🌳 Modelo escolhido

Foi utilizado **RandomForestRegressor**, por capturar:

* relações não lineares
* robustez em datasets pequenos
* feature importance interpretável

## 📏 Resultado

* **RMSE:** 8.42
* **MAE:** 6.63
* **R²:** 0.69

O resultado indica boa capacidade de generalização para um dataset de 500 registros.

---

# 🚀 Parte 3 — Recommendation Engine

Foi construído um **motor de recomendações híbrido**, baseado em:

* benchmarks do dataset
* regras contextuais por plataforma
* uplift estimado
* fallback heurístico

## ⚙️ Como funciona

O sistema:

1. recebe **uma campanha (1 linha)**
2. identifica gaps em relação aos benchmarks
3. estima uplift esperado
4. ordena por impacto

## 📌 Exemplo de saída

```text
--- ANALISANDO CAMPANHA KLK-0001 | SCORE ATUAL: 63.6 ---
1. [Alta] Adicionar um hook nos primeiros 3s pode elevar o CTR em aproximadamente 39.2%.
2. [Alta] No TikTok, migrar para formato vertical pode melhorar a retenção e ROAS em aproximadamente 18%.
3. [Média] No LinkedIn, migrar para formato horizontal pode elevar o watch time em aproximadamente 12%, melhorando retenção e percepção de qualidade."
```

## 🧩 Arquitetura do engine

O motor foi modularizado em:

```python
recommendation_engine.py
```

permitindo futura integração com:

* APIs
* dashboards
* interfaces de produto

---

# ▶️ Como executar a análise de uma campanha



Para testar o **Recommendation Engine** no notebook, basta selecionar o `campaign_id` da campanha desejada no final do arquivo `notebook_analise.ipynb`.

Exemplo:

```python
campaign_id = "KLK-0003"  # Substitua pelo ID da campanha que deseja analisar
sample_campaign = df[df["campaign_id"] == campaign_id].iloc[0]
recs = get_recommendations(sample_campaign, df)
```

Essa abordagem torna a análise mais dinâmica e próxima de um cenário real de produto, permitindo consultar campanhas específicas sem depender do índice da linha no dataset.

---

# 📝 Parte 4 — Visão de Produto

As respostas abertas da Parte 4 serão apresentadas no documento **Product_vision.md**, cobrindo:

* extração de features diretamente do vídeo
* arquitetura de produção do recommendation engine escalabilidade e integração
* melhorias futuras
* experimentos adicionais

---

