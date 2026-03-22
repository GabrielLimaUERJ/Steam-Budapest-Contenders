# 🏆 Steam Budapest Contenders Analyzer

Aplicação em Python que permite analisar stickers do Steam Market relacionados ao evento Budapest 2025, gerando comparações de preços e evitando bloqueios de API com cache.

---

## 🎯 Objetivo

Permitir a análise rápida de stickers do Steam Market, possibilitando:

- Seleção de até 16 stickers por vez  
- Consulta automática de preços no Steam Market  
- Geração de tabela de comparação entre os stickers selecionados  
- Redução de requisições repetidas via cache para evitar bloqueios  

---

## 🛠️ Tecnologias

- Python  
- Streamlit (interface interativa)  
- Pandas (manipulação de dados)  
- Requests / API do Steam (extração de preços)  
- Cache em JSON / CSV (armazenamento de requisições)  

---

## 📚 Funcionalidades

- Seleção interativa de até 16 stickers  
- Extração automática de appid e nome do sticker  
- Consulta de preço atual e mediano no Steam Market  
- Leitura de volume de vendas  
- Cache de requisições para reduzir chamadas à API  
- Geração de tabela comparativa dos stickers  
- Exportação de resultados em CSV ou JSON  

---

## ⚠️ Limitações

- Funciona apenas com stickers holográficos e dourados dentro do Steam Market  
- Depende da API do Steam (limites e disponibilidade)  
- Máximo de 16 stickers por execução  

---

## ▶️ Como executar

1. Clone o repositório:

```bash
git clone https://github.com/GabrielLimaUERJ/Steam-Budapest-Contenders.git
cd Steam-Budapest-Contenders
pip install -r requirements.txt
streamlit run app.py
