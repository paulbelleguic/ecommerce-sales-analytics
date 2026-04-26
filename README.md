# E-commerce Sales Analytics

End-to-end data portfolio project focused on e-commerce sales analysis, dashboarding, and sales value prediction using the public Olist dataset.

## Project Overview
This project was built as a complete data workflow similar to a professional analytics / machine learning project:
- raw data audit and cleaning
- analytical table construction
- business KPI analysis
- SQL integration with SQLite
- interactive Streamlit dashboard
- baseline machine learning model for order value prediction
- public deployment of the final app

## Business Objective
The goal is to analyze e-commerce sales performance and build a first predictive model able to estimate the total value of a delivered order from a set of order-level features.

## Live App
- [Streamlit Dashboard](https://fgwxckwvqwefghgqe3ursh.streamlit.app/)

## Dataset
- Olist Brazilian E-Commerce Public Dataset

## Tech Stack
- Python
- Pandas
- NumPy
- SQL
- SQLite
- Scikit-learn
- Joblib
- Streamlit

## Project Structure
- `data/raw/`: raw source files
- `data/processed/`: processed assets and SQLite database
- `notebooks/`: audit, business analysis, and machine learning notebooks
- `models/`: saved ML pipeline
- `sql/`: SQL scripts and business queries
- `app/`: Streamlit dashboard application

## Main Deliverables
- Initial data audit across relational e-commerce tables
- Order-level analytical dataset (`delivered_sales`)
- Business KPI analysis:
  - revenue
  - average order value
  - customer distribution
  - monthly trends
  - geography
  - delivery performance
- SQLite integration for SQL querying
- Streamlit dashboard with interactive filters
- Baseline regression model for sales value prediction
- Prediction interface integrated into the dashboard
- Publicly deployed interactive application

## Key Insight
Late deliveries are strongly associated with lower customer satisfaction. In the analysis, delayed orders received significantly lower average review scores than on-time or early deliveries.

## Current Progress
- [x] Project setup
- [x] Initial data audit
- [x] Initial cleaning and date conversion
- [x] Analytical table construction
- [x] Business analysis and KPI exploration
- [x] SQL database integration
- [x] Dashboard creation
- [x] Baseline sales prediction model
- [x] Prediction interface integrated into the dashboard
- [x] Public deployment
- [ ] Final project polishing

## Run Locally
Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
