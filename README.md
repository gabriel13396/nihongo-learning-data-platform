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

## Future improvements

- Add real Anki export ingestion
- Add Power BI dashboard screenshots
- Add Azure Data Factory orchestration
- Add Azure SQL Database as the serving layer
- Add weekly automated pipeline runs with GitHub Actions
- Add a lightweight Streamlit dashboard
