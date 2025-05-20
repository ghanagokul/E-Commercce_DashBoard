# 🛒 Ecommerce Dashboard on GCP

This project demonstrates an end-to-end Big Data pipeline for ecommerce analytics, leveraging Google Cloud Platform (GCP), PySpark for ETL, and Plotly for interactive dashboards.

---

## 📌 Overview

- 📦 Data Source: [Kaggle Ecommerce Dataset](https://www.kaggle.com/)
- 🚀 Platform: Google Cloud Platform (GCP)
- 🔧 ETL Framework: PySpark
- 🗃️ Storage: Google Cloud Storage (GCS)
- 📊 Dashboarding: Python (Plotly)
- ☁️ Deployment: GCP Dataproc + GCS + Local Dashboard

---

## 🔄 Workflow Summary

1. **Data Ingestion**
   - Downloaded the raw ecommerce dataset from Kaggle.
   - Uploaded it to Google Cloud Storage (GCS).

2. **ETL using PySpark**
   - Set up a Dataproc cluster on GCP.
   - Performed data cleaning, transformation, and aggregation using PySpark on Dataproc.
   - Output: Cleaned and processed files saved to GCS in Parquet/CSV format.

3. **Data Storage**
   - Final transformed datasets stored in GCS, optimized for query and analytics.

4. **Dashboard Creation**
   - Used **Plotly** in Python to create interactive visualizations.
   - Built a local dashboard showcasing:
     - 📈 Total Sales Over Time
     - 📊 Orders by Category
     - 💰 Revenue Trends
     - 🛍️ Top-Selling Products
   - Data read from GCS using `pandas` with `gcsfs` or directly through BigQuery.
   - Dashboard served locally via **Plotly Dash** or within **Jupyter Notebook**.

5. **Deployment**
   - ETL pipeline deployed using GCP Dataproc.
   - Dashboard can be hosted locally or on GCP using App Engine / Cloud Run for broader access.

---

## 🛠️ Tech Stack

| Component       | Tool/Service       |
|----------------|--------------------|
| Data Source     | Kaggle             |
| Compute Engine  | Dataproc (PySpark) |
| Storage         | Google Cloud Storage |
| Language        | Python (PySpark, Pandas) |
| Dashboard       | Plotly / Dash      |
| Deployment      | GCP                |

---

## 📁 Project Structure

