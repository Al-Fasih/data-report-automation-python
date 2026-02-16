#!/usr/bin/env python3
"""
Data Report Automation (Python) — v1.0

Reads a sales CSV, validates/cleans data, computes business metrics,
and generates a professional report package:
- Excel (.xlsx) with multiple sheets
- Text summary (.txt)
- Charts (.png)
- Logs (.log)

Expected CSV columns:
date, product, category, quantity, price
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

REQUIRED_COLUMNS = {"date", "product", "category", "quantity", "price"}


@dataclass(frozen=True)
class ReportPaths:
    base_dir: Path
    run_id: str

    @property
    def excel(self) -> Path:
        return self.base_dir / f"sales_report_{self.run_id}.xlsx"

    @property
    def text(self) -> Path:
        return self.base_dir / f"sales_report_{self.run_id}.txt"

    @property
    def log(self) -> Path:
        return self.base_dir / f"run_{self.run_id}.log"

    @property
    def chart_category(self) -> Path:
        return self.base_dir / f"chart_revenue_by_category_{self.run_id}.png"

    @property
    def chart_daily(self) -> Path:
        return self.base_dir / f"chart_daily_revenue_{self.run_id}.png"


# -----------------------------
# Logging
# -----------------------------

def setup_logger(log_path: Path, verbose: bool) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("data-report-automation")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler (always DEBUG)
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO if verbose else logging.WARNING)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


# -----------------------------
# Core steps
# -----------------------------

def load_csv(csv_path: Path, logger: logging.Logger) -> pd.DataFrame:
    logger.info(f"Loading CSV: {csv_path}")
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV: {e}") from e

    logger.info(f"Loaded rows: {len(df):,} | columns: {list(df.columns)}")
    return df


def validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def clean_and_transform(
    df: pd.DataFrame,
    logger: logging.Logger,
    date_format: Optional[str] = None,
) -> pd.DataFrame:
    """
    Cleans data robustly, converts types, removes invalid rows,
    and creates derived fields.
    """
    validate_columns(df)

    df = df.copy()

    # Normalize strings
    df["product"] = df["product"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()

    # Coerce numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Dates
    # If user provides a strict format, use it; else let pandas infer.
    if date_format:
        df["date"] = pd.to_datetime(df["date"], errors="coerce", format=date_format)
    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    before = len(df)

    # Drop missing essentials
    df = df.dropna(subset=["date", "product", "category", "quantity", "price"])

    # Business sanity rules
    df = df[(df["quantity"] > 0) & (df["price"] >= 0)]

    # Derived metrics
    df["total"] = df["quantity"] * df["price"]
    df["date"] = df["date"].dt.date  # keep clean date for grouping
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)

    removed = before - len(df)
    if removed:
        logger.warning(f"Removed invalid rows: {removed:,} | remaining: {len(df):,}")
    else:
        logger.info("No invalid rows removed.")

    if df.empty:
        raise ValueError("No valid data after cleaning.")

    return df


@dataclass(frozen=True)
class Metrics:
    total_revenue: float
    total_units: float
    avg_ticket: Optional[float]
    top_product: Optional[str]
    top_category: Optional[str]
    best_day: Optional[str]  # ISO date string
    worst_day: Optional[str]
    max_sale_row_total: Optional[float]
    min_sale_row_total: Optional[float]


def compute_metrics(df: pd.DataFrame) -> tuple[Metrics, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Aggregations
    by_category = (
        df.groupby("category", as_index=False)["total"]
        .sum()
        .sort_values("total", ascending=False)
    )

    by_product = (
        df.groupby("product", as_index=False)["total"]
        .sum()
        .sort_values("total", ascending=False)
    )

    by_day = (
        df.groupby("date", as_index=False)["total"]
        .sum()
        .sort_values("date", ascending=True)
    )
    by_day["date"] = by_day["date"].astype(str)

    total_revenue = float(df["total"].sum())
    total_units = float(df["quantity"].sum())

    avg_ticket = None
    if total_units > 0:
        avg_ticket = total_revenue / total_units

    top_product = None
    if not by_product.empty:
        top
