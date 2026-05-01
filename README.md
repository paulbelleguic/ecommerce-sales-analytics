# E-Commerce Sales Analytics

An end-to-end data analytics and machine learning project built on the **Olist Brazilian E-Commerce Public Dataset**.  
The goal of this project is to transform raw transactional data into a professional analytics workflow including:

- data cleaning and preparation
- business KPI analysis
- SQL integration
- interactive dashboarding with Streamlit
- predictive modeling for order value estimation
- integration with a deployed FastAPI backend for production-style predictions

## Project Overview

This project simulates a real-world data analyst / junior data scientist workflow.

Starting from raw e-commerce data, I:
- audited and explored the dataset
- cleaned and standardized key variables
- built an analytical table at the order level
- analyzed business performance across time, geography, and logistics
- stored processed data in SQLite for reproducible querying
- created an interactive Streamlit dashboard
- trained a baseline machine learning model to predict customer order value

## Dataset

Source: **Olist Brazilian E-Commerce Public Dataset**

The dataset contains information about:
- orders
- order items
- payments
- products
- customers
- sellers
- reviews
- geolocation
- delivery dates

It provides a rich business case for sales analysis, customer behavior, and logistics performance.

## Main Objectives

The project answers several business questions such as:
- How is revenue evolving over time?
- Which states and cities generate the most sales?
- How long do deliveries take on average?
- What is the impact of late delivery on customer satisfaction?
- Can we predict the total value of an order using available business features?

## Workflow

### 1. Data Audit
Initial exploration of the raw files:
- schema inspection
- missing values analysis
- duplicates check
- data types review
- first business observations

### 2. Data Cleaning
Preparation steps included:
- date conversion to datetime format
- null value inspection
- harmonization of columns
- creation of analysis-ready features

### 3. Analytical Table Construction
A final order-level table was created to support analysis and modeling.

Example derived metrics:
- total order value
- number of items per order
- freight cost
- delivery delay
- order status
- customer location
- review score

### 4. Business Analysis
Key analyses performed:
- total revenue
- average order value
- monthly sales evolution
- top-performing states and cities
- delivery performance
- relationship between delivery delay and review score

### 5. SQL Integration
Processed data was stored in a SQLite database to make the project more production-oriented.

This allowed:
- reproducible KPI queries
- SQL-based validation of business results
- a cleaner analytics pipeline

### 6. Interactive Dashboard
A Streamlit dashboard was developed to make the analysis accessible through an interactive interface.

Main dashboard components:
- KPI cards
- time series charts
- geographic performance views
- logistics insights
- filtered exploration
- machine learning prediction section connected to a deployed API

### 7. Machine Learning
A regression model was trained to predict **total order value**.

Models explored:
- Random Forest Regressor baseline
- HistGradientBoostingRegressor improvement

Evaluation metrics included:
- MAE
- RMSE
- R²

Special care was taken to avoid **data leakage** by excluding variables that directly reveal the target.

### 8. API Integration

The dashboard prediction form no longer loads the model directly inside Streamlit. It sends the prediction payload to a deployed FastAPI backend:

```text
https://ai-backend-api-3jn5.onrender.com/predict/
```

This separates the frontend dashboard from the model-serving layer and demonstrates a more production-oriented architecture.

## Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib / Seaborn**
- **Scikit-learn**
- **SQLite**
- **Streamlit**
- **Joblib**
- **FastAPI API integration**
- **Requests**

## Key Insights

- Sales are concentrated in a limited number of regions.
- Delivery performance has a measurable effect on customer satisfaction.
- Order value varies significantly depending on basket composition and logistics variables.
- A baseline machine learning model can capture part of the variability in order value, though there is still room for improvement.

## Deployment

The project is deployed on Streamlit Community Cloud.

Live app: https://ecommerce-sales-analytics-el8b4nsxcuw8emmu8f9idw.streamlit.app/

The prediction section calls the deployed FastAPI backend rather than running local inference in the Streamlit process.

## Model Limitations

- The prediction task is simplified to order value regression.
- Feature engineering can be extended further.
- Hyperparameter tuning remains limited.
- No advanced model tracking or deployment pipeline has been added yet.
- The prediction API accepts future years up to 2030 for demonstration, but predictions outside the original training period should be interpreted carefully.

## How to Run the Project

1. Clone the repository

git clone https://github.com/paulbelleguic/ecommerce-sales-analytics.git
cd ecommerce-sales-analytics

2. Install dependencies
pip install -r requirements.txt

3. Launch the Streamlit app
streamlit run app/dashboard.py

## What This Project Demonstrates

This project highlights skills in:
data cleaning
exploratory data analysis
KPI design
SQL usage
dashboard development
machine learning fundamentals
API integration
end-to-end project

## Author
Paul Belleguic
Portfolio project in data analytics / data science focused on transforming raw business data into actionable insights and deployable tools

## Future Improvements
Possible next steps:
add customer segmentation
build a delivery delay classification model
integrate more advanced visual storytelling
add automated retraining or experiment tracking
improve feature engineering for stronger predictive performance

## Project Structure

```bash
ecommerce-sales-analytics/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│       └── ecommerce.db
│
├── models/
│   └── baseline_sales_model.joblib
│
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_business_analysis.ipynb
│   └── 03_ml_modeling.ipynb
│
├── requirements.txt
└── README.md
