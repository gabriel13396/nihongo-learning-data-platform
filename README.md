# Nihongo Learning Data Platform

A personal data engineering portfolio project that turns Japanese study activity into analytics-ready datasets.

This project models a real learning workflow: Anki-style vocabulary reviews, reading logs, listening practice, grammar drills, and tutor sessions. It uses a cloud-style medallion architecture and can run locally or optionally sync outputs to Azure Blob Storage.

## Why this project exists

I wanted a portfolio project that felt more personal than a generic public dataset pipeline. Since I study Japanese consistently, I built a small data platform that answers questions like:

- How many focused study hours am I completing each week?
- Am I spending too much time on flashcards compared to reading, listening, and speaking?
- Which vocabulary levels have the weakest retention?
- How close is my study mix to my target N2/N1 learning goals?
- What does my progress look like across vocabulary, reading, grammar, listening, and tutoring?

The sample data in this repo is synthetic, but the schema is designed so real exported study logs can be dropped in later.

## Architecture

```text
Raw CSV logs
  ↓
Bronze layer: lightly standardized source tables
  ↓
Silver layer: cleaned, validated, typed Parquet datasets
  ↓
Gold layer: analytics marts and KPI tables
  ↓
SQLite local warehouse / optional Azure Blob Storage
  ↓
Power BI, notebooks, dashboards, or SQL analysis
```

## Tech stack

- Python
- pandas
- Parquet / pyarrow
- SQLite analytics warehouse
- Azure Blob Storage optional sync
- Azure Bicep infrastructure template
- GitHub Actions CI
- pytest data quality tests

## Project structure

```text
nihongo-learning-data-platform/
├── data/
│   ├── raw/               # synthetic source CSV files
│   ├── bronze/            # standardized source extracts
│   ├── silver/            # cleaned Parquet datasets
│   └── gold/              # analytics-ready marts
├── infra/
│   └── main.bicep         # optional Azure storage infrastructure
├── reports/
│   └── sample_queries.sql # SQL examples for the local warehouse
├── scripts/
│   └── upload_to_azure_blob.py
├── src/
│   ├── config.py
│   ├── data_quality.py
│   ├── generate_sample_data.py
│   ├── load.py
│   ├── pipeline.py
│   └── transform.py
├── tests/
│   ├── test_data_quality.py
│   └── test_pipeline_outputs.py
└── .github/workflows/ci.yml
```

## Run locally

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create synthetic study data and run the full pipeline:

```bash
python -m src.generate_sample_data
python -m src.pipeline
```

Run tests:

```bash
python -m pytest -q
```

After the pipeline runs, check these folders:

```text
data/silver/
data/gold/
warehouse/nihongo_analytics.db
```

## Main outputs

The pipeline creates four analytics marts:

| Output | Purpose |
|---|---|
| `gold_daily_study_summary` | Daily study time, activity count, and skill mix |
| `gold_weekly_skill_balance` | Weekly balance between vocab, reading, listening, grammar, and speaking |
| `gold_vocab_retention_by_level` | Vocabulary retention by JLPT level and review stage |
| `gold_learning_readiness_score` | Simple scoring model for consistency, balance, and retention |

## Example SQL questions

```sql
-- Which weeks had the highest total study time?
SELECT week_start, total_minutes
FROM gold_weekly_skill_balance
ORDER BY total_minutes DESC;

-- Which JLPT level has the weakest retention?
SELECT jlpt_level, retention_rate
FROM gold_vocab_retention_by_level
ORDER BY retention_rate ASC;

-- How balanced was my study mix this week?
SELECT *
FROM gold_weekly_skill_balance
ORDER BY week_start DESC
LIMIT 1;
```

More queries are in `reports/sample_queries.sql`.

## Optional Azure setup

This project can run fully locally. Azure is optional.

To create a storage account and four containers using Bicep:

```bash
az login
az group create --name rg-nihongo-learning-dev --location eastus
az deployment group create \
  --resource-group rg-nihongo-learning-dev \
  --template-file infra/main.bicep \
  --parameters storageAccountName=<globally_unique_storage_name>
```

Create a `.env` file:

```bash
cp .env.example .env
```

Add your connection string:

```text
AZURE_STORAGE_CONNECTION_STRING="<your_connection_string>"
AZURE_STORAGE_CONTAINER_RAW="raw"
AZURE_STORAGE_CONTAINER_BRONZE="bronze"
AZURE_STORAGE_CONTAINER_SILVER="silver"
AZURE_STORAGE_CONTAINER_GOLD="gold"
```

Upload local pipeline outputs to Azure Blob Storage:

```bash
python scripts/upload_to_azure_blob.py
```

## Resume bullet

Built a personal Azure-style data engineering platform for Japanese study analytics using Python, Parquet, SQLite, Azure Blob Storage, data quality checks, and GitHub Actions CI to transform raw learning logs into analytics-ready KPI marts.

## Interview pitch

I wanted a project that was more personal than a generic Kaggle pipeline, so I built a data platform around my Japanese learning workflow. It ingests synthetic Anki-style reviews, reading logs, listening sessions, grammar drills, and tutor sessions, then processes them through bronze, silver, and gold layers. I added validation checks, Parquet outputs, a SQLite analytics warehouse, GitHub Actions tests, and optional Azure Blob Storage sync. The project shows how I think about practical pipeline structure, data quality, and analytics modeling.

## Future improvements

- Add real Anki export ingestion
- Add Power BI dashboard screenshots
- Add Azure Data Factory orchestration
- Add Azure SQL Database as the serving layer
- Add weekly automated pipeline runs with GitHub Actions
- Add a lightweight Streamlit dashboard
