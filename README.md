# EdTech Content Data Pipeline

A scalable data pipeline designed to collect, clean, standardize, and organize educational content from multiple public sources into a unified dataset for search and discovery.

## Project Overview

This data engineering project includes:

1. **Data Source Selection:** Integration of multiple public educational content sources covering **AI, Data, and Cloud Computing**.

2. **Data Architecture:** Implementation of **Bronze, Silver, and Gold** layers using **Delta Lake** and the Medallion Architecture.

3. **ETL Pipelines:** Data ingestion, cleaning, transformation, and standardization using **PySpark, SQL, dbt, and Databricks notebooks**.

4. **Data Quality & Testing:** Validation of row counts, duplicate records, missing values, URLs, dates, and pipeline repeatability.

5. **Unified Data Model:** Combining educational content from different sources into a standardized Gold dataset for search, filtering, and discovery.

6. **API Integration:** Providing access to the curated Gold data through a REST API for content search and discovery.

7. **GitHub Integration:** Version-controlling project notebooks, code, and documentation using GitHub.

🎯 This repository showcases skills in:

* Azure Databricks & Delta Lake
* PySpark & SQL
* dbt & ETL/ELT Pipelines
* Data Cleaning & Transformation
* Data Quality & Testing
* Medallion Architecture
* Git & GitHub
* REST API Integration

## Project Goal

The goal of this project is to build a **repeatable and structured data pipeline** that collects educational content from multiple public sources and transforms it into a **unified, high-quality dataset**.

The project focuses on content related to **Artificial Intelligence, Data, and Cloud Computing**, making it easier to **search, filter, and discover relevant educational resources**.

## Selected Sources

The project uses several selected public source types:

* **Coursera** — educational courses
* **Microsoft Learn** — learning modules and resources
* **GitHub** — repositories and technical projects
* **YouTube** — educational videos
* **Educational Blogs** — technical articles and tutorials
* **Newsletters** — educational and technical newsletters through RSS feeds

## Architecture

```text
Selected Public Sources
        │
        ▼
     Ingestion
        │
        ▼
      Bronze
    Raw Data Layer
        │
        ▼
      Silver
Cleaned & Standardized
        │
        ▼
       Gold
Curated & Unified Data
        │
        ▼
        API
Search & Discovery
```

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

## Project Structure

```text
EdTech-Content-Data-Pipeline/
│
├── Sources/
│   └── Selected Data Sources
│
├── Bronze/
│   └── Raw Data Ingestion
│
├── Silver/
│   ├── Blogs
│   ├── Newsletters
│   ├── Coursera
│   ├── Microsoft Learn
│   ├── GitHub
│   └── YouTube
│
├── Gold/
│   └── Unified EdTech Content
│
├── Testing/
│   └── Data Quality Checks
│
└── README.md
```

## Team

Developed as part of the **SDA Data Engineering Bootcamp**.

* Amal Al Dawsari
* Ewan Hamoh
* Renad Alghamdi
