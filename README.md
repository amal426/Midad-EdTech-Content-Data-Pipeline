# EdTech Content Data Pipeline

A scalable data pipeline designed to collect, clean, standardize, and organize educational content from multiple public sources into a unified dataset for search and discovery.

## Project Overview

This data engineering project includes:

1. **Data Source Selection:** Integration of multiple public educational content sources covering **AI, Data, and Cloud Computing**.

2. **Data Architecture:** Implementation of **Bronze, Silver, and Gold** layers using **Delta Lake** and the Medallion Architecture.

3. **ETL Pipelines:** Data ingestion, cleaning, transformation, and standardization using **PySpark, SQL, dbt, and Databricks notebooks**.

4. **Data Quality & Testing:** Validation of row counts, duplicate records, missing values, URLs, dates, and pipeline repeatability.

5. **Unified Data Model:** Combining educational content from different sources into a standardized Gold dataset for search, filtering, and discovery.

6. **API Integration:** A **FastAPI** backend that provides endpoints for content retrieval, search, filtering, pagination, and health checks.

7. **Web Application:** A **Streamlit** interface that allows users to search, filter, and explore educational content through the API.

8. **GitHub Integration:** Version-controlling project notebooks, code, and documentation using GitHub.

🎯 This repository showcases skills in:

* Azure Databricks & Delta Lake
* PySpark & SQL
* dbt & ETL/ELT Pipelines
* Data Cleaning & Transformation
* Data Quality & Testing
* Medallion Architecture
* FastAPI & REST APIs
* Streamlit
* Python
* Git & GitHub

## Project Goal

The goal of this project is to build a **repeatable and structured data pipeline** that collects educational content from multiple public sources and transforms it into a **unified, high-quality dataset**.

The project focuses on content related to **Artificial Intelligence, Data, and Cloud Computing**, making it easier to **search, filter, and discover relevant educational resources** through an API and user interface.

## Architecture

## Selected Sources

The project uses several selected public source types:

* **Coursera** — educational courses
* **Microsoft Learn** — learning modules and resources
* **GitHub** — repositories and technical projects
* **YouTube** — educational videos
* **Educational Blogs** — technical articles and tutorials
* **Newsletters** — educational and technical newsletters through RSS feeds

## Medallion Layers

### Bronze Layer

Stores raw data collected from the selected sources with minimal transformation.

### Silver Layer

Cleans and standardizes the data by:

* Removing invalid records
* Handling missing values
* Standardizing topics and fields
* Parsing dates
* Removing duplicates
* Applying data quality rules

### Gold Layer

Combines the cleaned data from all sources into a unified dataset ready for consumption.

The Gold dataset includes:

* Content ID
* Title
* Description
* Content Type
* Category
* Topic
* Difficulty Level
* Language
* Keywords
* Source
* Published Date
* Last Updated
* URL

## API Layer

The project includes a **FastAPI** backend that exposes the Gold data through REST API endpoints.

Current API functionality includes:

* Health check
* Retrieve educational content
* Retrieve content by `content_id`
* Search content
* Filter content by topic and source
* Date-based filtering
* Pagination
* Result limits

The API loads the curated Gold dataset from a Parquet snapshot for content retrieval and search.

## User Interface

A **Streamlit** web interface is used to interact with the API.

Users can:

* Search educational content
* Filter by content type
* Filter by topic
* Filter by source
* Select the number of results
* View returned content in a structured table

## Project Structure

```text
EdTech-Content-Data-Pipeline/
│
├── src/
│   ├── database/
│   ├── ingestion/
│   └── transformation/
│
├── data sources/
│   ├── notebooks/
│   │   ├── API's_sources.ipynb
│   │   └── RSS Feeds.ipynb
│   │
│   └── raw/
│       ├── api_sources_1200.json
│       └── rss_feeds_600.json
│
├── exploration/
│   ├── 04_data_exploration_bronze.ipynb
│   ├── 07_data_exploration_silver.ipynb
│   └── 10_data_exploration_gold.ipynb
│
├── midad data pipline/
│   ├── setup/
│   │   └── 01_create_schema.ipynb
│   │
│   ├── bronze/
│   │   ├── 02_ddl_bronze.ipynb
│   │   └── 03_load_bronze.ipynb
│   │
│   ├── silver/
│   │   ├── 05_ddl_silver.ipynb
│   │   └── 06_load_silver.ipynb
│   │
│   ├── gold/
│   │   └── 09_load_gold.ipynb
│   │
│   └── data quality/
│       ├── 08_data_quality_silver.ipynb
│       └── 11_data_quality_gold.ipynb
│
├── data/
│   ├── gold_content_snapshot.parquet
│   └── quality_report.json
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Team

Developed as part of the **SDA Data Engineering Bootcamp**.

* Amal Al Dawsari 
* Ewan Hamoh
* Renad Alghamdi
