import json
from contextlib import asynccontextmanager
from datetime import datetime

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query

gold_df: pd.DataFrame | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Loads the local Gold snapshot into memory once, when the API starts.
    global gold_df
    gold_df = pd.read_parquet("../data/gold_content_snapshot.parquet")
    print(f"Loaded {len(gold_df)} rows into memory")
    yield

app = FastAPI(lifespan=lifespan)


def df_to_json_records(df: pd.DataFrame) -> list[dict]:
    # Converts pandas' NaN (invalid in JSON) into null, which is valid JSON.
    return df.replace({np.nan: None}).to_dict(orient="records")


@app.get("/health")
def health():
    return {"status": "ok", "rows_loaded": len(gold_df)}

@app.get("/content")
def list_content(
    q: str | None = Query(None),
    content_type: str | None = Query(None),
    topic: str | None = Query(None),
    source: str | None = Query(None),
    limit: int = Query(30, le=500),   
    offset: int = Query(0),
):
    result = gold_df.copy()

    if q is not None and q.strip() != "":
        result = result[
            result["list_of_keywords"].astype(str).str.contains(q, case=False, na=False)
        ]

    if content_type is not None and content_type.strip() != "":
        result = result[result["content_type"] == content_type]

    if topic is not None and topic.strip() != "":
        result = result[result["topic"] == topic]

    if source is not None and source.strip() != "":
        result = result[
            result["source"].apply(lambda x: normalize_source(x)) == source.lower()
        ]

    if "published_date" in result.columns:
        result = result.sort_values("published_date", ascending=False, na_position="last")

    total = len(result)
    page = result.iloc[offset: offset + limit]

    return {"total": total, "count": len(page), "results": df_to_json_records(page)}
import re

# Mapping rules: how to normalize raw source values into 6 categories
SOURCE_RULES = [
    (r"^Blog\s*\|",           "blogs"),
    (r"^Newsletter\s*\|",     "newsletters"),
    (r"^YouTube$",            "youtube"),
    (r"^Coursera$",           "coursera"),
    (r"^Microsoft Learn$",    "microsoft learn"),
    (r"^GitHub$",             "github"),
]

ALLOWED_SOURCES = [
    "blogs",
    "newsletters",
    "coursera",
    "microsoft learn",
    "github",
    "youtube",
]


def normalize_source(raw: str) -> str | None:
    """Map a raw source string (e.g. 'Blog | NVIDIA') to one of the 6 categories."""
    if not isinstance(raw, str):
        return None
    for pattern, category in SOURCE_RULES:
        if re.match(pattern, raw.strip(), flags=re.IGNORECASE):
            return category
    return None


@app.get("/filters")
def get_filter_options():
    """Return available values for each filter (for dropdowns)."""
    # Map every raw source value to its category, keep only known ones
    mapped_sources = {
        normalize_source(s) for s in gold_df["source"].dropna().unique().tolist()
    }
    # Remove None and keep the order of ALLOWED_SOURCES
    available_sources = [s for s in ALLOWED_SOURCES if s in mapped_sources]

    return {
        "content_types": sorted(gold_df["content_type"].dropna().unique().tolist()),
        "topics": sorted(gold_df["topic"].dropna().unique().tolist()),
        "sources": available_sources,
    }

@app.get("/content/{content_id}")
def get_content(content_id: str):
    match = gold_df[gold_df["content_id"] == content_id]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"content_id '{content_id}' not found")
    return df_to_json_records(match)[0]


@app.get("/search")
def search_content(q: str = Query(..., min_length=1), limit: int = Query(30, le=500)):
    query_lower = q.lower()
    mask = (
        gold_df["title"].str.lower().str.contains(query_lower, na=False)
        | gold_df["description"].str.lower().str.contains(query_lower, na=False)
    )
    result = gold_df[mask].sort_values("published_date", ascending=False, na_position="last")
    page = result.head(limit)
    return {"total": len(result), "count": len(page), "results": df_to_json_records(page)}

# ... (rest of the previous code) ...
@app.get("/dashboard_stats")
def get_dashboard_stats():
    """Return aggregated statistics for the dashboard brief."""
    if gold_df is None or gold_df.empty:
        return {"error": "No data loaded"}

    # 1. Count items per source
    sources_series = gold_df["source"].apply(lambda x: normalize_source(x))
    source_counts = sources_series.value_counts().to_dict()

    # 2. Count items per content type
    content_type_counts = gold_df["content_type"].value_counts().to_dict()

    # 3. Count items per topic - take top 10 topics
    topic_counts = gold_df["topic"].value_counts().head(10).to_dict()

    # 4. Difficulty level distribution
    difficulty_counts = {}
    if "difficulty" in gold_df.columns:
        difficulty_counts = gold_df["difficulty"].value_counts().to_dict()
    elif "difficulty_level" in gold_df.columns:
        difficulty_counts = gold_df["difficulty_level"].value_counts().to_dict()

    # 5. General statistics
    total_rows = len(gold_df)

    return {
        "total_rows": total_rows,
        "source_counts": source_counts,
        "content_type_counts": content_type_counts,
        "topic_counts": topic_counts,
        "difficulty_counts": difficulty_counts,
    }

# ============================================
# Helper: infer difficulty level for sources
# that don't provide one (blogs, newsletters)
# ============================================

BEGINNER_KEYWORDS = [
    "introduction", "intro", "beginner", "beginners", "basics",
    "getting started", "fundamentals", "what is", "what are",
    "tutorial", "101", "crash course", "first steps", "overview",
    "guide", "explained", "learn", "start", "simple", "easy",
    "walkthrough", "step by step", "for dummies",
]

ADVANCED_KEYWORDS = [
    "advanced", "deep dive", "expert", "production", "scaling",
    "optimization", "optimizing", "architecture", "internals",
    "under the hood", "fine-tuning", "research", "paper",
    "benchmark", "best practices", "design patterns",
    "performance", "distributed", "internals", "profiling",
    "high-level", "cutting edge", "state of the art",
]


def infer_level(row) -> str:
    """
    Infer the difficulty level of a content row.
    - If difficulty_level is already set (Coursera/GitHub/YouTube), keep it.
    - Otherwise (blogs/newsletters = null), infer from title + keywords + description.
    - Fallback to "Intermediate" if no strong signal.
    """
    existing = row.get("difficulty_level")
    if pd.notna(existing):
        val = str(existing).strip()
        if val and val.lower() not in ("nan", "none", "null"):
            return val

    # Build searchable text
    parts = [
        str(row.get("title") or ""),
        str(row.get("list_of_keywords") or ""),
        str(row.get("category") or ""),
        str(row.get("description") or "")[:400],
    ]
    text = " ".join(parts).lower()

    b_hits = sum(1 for kw in BEGINNER_KEYWORDS if kw in text)
    a_hits = sum(1 for kw in ADVANCED_KEYWORDS if kw in text)

    if a_hits > b_hits:
        return "Advanced"
    if b_hits > a_hits:
        return "Beginner"
    return "Intermediate"
@app.get("/learning-path")
def get_learning_path(
    topic: str = Query(..., description="Topic: AI, Data, or Cloud"),
    level: str = Query(..., description="Difficulty: Beginner, Intermediate, Advanced, or All"),
    keyword: str | None = Query(None, description="Optional keyword filter"),
    per_level: int = Query(5, le=50),
):
    """
    Build a targeted learning path.
    - level='All' → no level filter (across all levels).
    - Otherwise → strict level filter using inferred levels.
    - keyword is applied on top of the level filter.
    """
    df = gold_df[gold_df["topic"] == topic].copy()

    if df.empty:
        raise HTTPException(status_code=404, detail=f"No content found for topic '{topic}'")

    # 1. Infer level for every row
    df["_level"] = df.apply(infer_level, axis=1)

    # 2. Level filter — skipped when level == "All"
    if level != "All":
        df = df[df["_level"] == level].copy()

    if df.empty:
        return {
            "topic": topic, "level": level, "keyword": keyword,
            "total": 0, "results": [],
        }

    # 3. Keyword filter (optional)
    if keyword and keyword.strip():
        kw = keyword.strip().lower()
        mask = (
            df["list_of_keywords"].astype(str).str.lower().str.contains(kw, na=False)
            | df["title"].astype(str).str.lower().str.contains(kw, na=False)
            | df["description"].astype(str).str.lower().str.contains(kw, na=False)
        )
        df = df[mask].copy()

    if df.empty:
        return {
            "topic": topic, "level": level, "keyword": keyword,
            "total": 0, "results": [],
        }

    # 4. Sort
    if "published_date" in df.columns:
        df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    df["_desc_len"] = df["description"].astype(str).str.len()
    df = df.sort_values(
        by=["published_date", "_desc_len"],
        ascending=[False, False],
        na_position="last",
    )

    top = df.head(per_level).copy()
    top["inferred_level"] = top["_level"]
    top = top.drop(columns=["_level", "_desc_len"], errors="ignore")

    records = df_to_json_records(top)

    return {
        "topic": topic,
        "level": level,
        "keyword": keyword,
        "total": len(df),
        "results": records,
    }