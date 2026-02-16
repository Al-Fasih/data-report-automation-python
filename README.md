# 📊 Data Report Automation (Python) — v1.0

Automação completa de geração de relatórios de vendas a partir de arquivos CSV.

O projeto realiza validação, limpeza, transformação, cálculo de métricas e geração automática de múltiplos artefatos (Excel, relatório textual, gráficos e logs).

---

## 🎯 Objetivo

Demonstrar competências profissionais em:

* Manipulação e transformação de dados com Python
* Validação e tratamento de dados inconsistentes
* Cálculo de métricas de negócio
* Automação de relatórios
* Estruturação de projeto com CLI e logging
* Geração de múltiplos outputs profissionais

Este projeto simula um pipeline de dados real de pequeno porte (ETL simplificado).

---

## 🧠 O que o sistema faz

### 1️⃣ Leitura e Validação

* Verifica colunas obrigatórias:

  * `date`, `product`, `category`, `quantity`, `price`
* Converte tipos de dados
* Remove linhas inválidas
* Aplica regras de negócio (quantidade > 0, preço ≥ 0)
* Registra logs da execução

---

### 2️⃣ Transformação e Métricas

Calcula automaticamente:

* Faturamento total
* Total de unidades vendidas
* Ticket médio
* Produto com maior faturamento
* Categoria com maior faturamento
* Melhor dia de vendas
* Pior dia de vendas
* Maior e menor venda individual

Também gera agregações:

* Receita por categoria
* Receita por produto
* Receita diária

---

### 3️⃣ Geração de Artefatos

A cada execução, o sistema gera arquivos versionados por timestamp:

📁 `reports/`

* `sales_report_<run_id>.xlsx`

  * summary
  * data_quality
  * data
  * revenue_by_category
  * revenue_by_product
  * daily_revenue

* `sales_report_<run_id>.txt`

  * Resumo executivo formatado

* `chart_revenue_by_category_<run_id>.png`

* `chart_daily_revenue_<run_id>.png`

* `run_<run_id>.log`

  * Log detalhado da execução

---

## 🗂 Estrutura do Projeto

```
data-report-automation-python/
│
├─ data/          # Arquivos CSV de entrada
├─ reports/       # Relatórios gerados automaticamente
├─ main.py        # Script principal
├─ .gitignore
└─ README.md
```

---

## ▶️ Como Executar

### Instale as dependências

```bash
pip install pandas openpyxl matplotlib
```

---

### Execução padrão

```bash
python main.py
```

---

### Execução avançada

```bash
python main.py --csv data/sales.csv --out reports --verbose
```

### Parâmetros disponíveis

| Parâmetro       | Descrição                                 |
| --------------- | ----------------------------------------- |
| `--csv`         | Caminho do CSV de entrada                 |
| `--out`         | Pasta de saída dos relatórios             |
| `--run-id`      | Identificador manual da execução          |
| `--date-format` | Formato específico da data (ex: %Y-%m-%d) |
| `--no-charts`   | Desativa geração de gráficos              |
| `--verbose`     | Exibe logs no console                     |

---

## 🛡 Robustez do Sistema

* Tratamento de exceções
* Logging estruturado
* Validação de esquema de dados
* Proteção contra divisão por zero
* Versionamento automático de execução
* Organização limpa e modular

---

## 🚀 Diferenciais Técnicos

✔ Estrutura orientada a produção
✔ CLI profissional com argparse
✔ Uso de dataclasses
✔ Logging estruturado
✔ Exportação multi-formato
✔ Separação clara de responsabilidades
✔ Código pronto para escalar

---

## 📈 Possíveis Evoluções Futuras

* Integração com banco de dados (SQL Server / PostgreSQL)
* API REST para disparar relatórios
* Containerização com Docker
* Testes automatizados (pytest)
* Deploy em ambiente cloud

---

## 📌 Sobre

Projeto desenvolvido para demonstrar domínio prático de Python aplicado a dados e automação de relatórios empresariais.
