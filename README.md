🏡 Municipality Financial Health Prediction

This project aims to **predict whether a municipality is at risk of bankruptcy**, based on detailed financial, demographic, and structural data collected from Italian municipalities. The central goal is to leverage **machine learning** and **data-driven insights** to build a predictive model that can serve as an early warning system for municipal financial distress.

---

 🚀 Project Objective

The primary objective is to:
> **Develop a machine learning model that accurately classifies municipalities as financially solvent or at risk of bankruptcy.**

This system could support policymakers, auditors, and local governments in identifying at-risk municipalities before default occurs.

---

 📊 Data Sources

The dataset consists of various CSV files containing:

- 📉 **Annual municipal expenditure data**
- 👥 **Population and demographic statistics**
- 🏡 **Functional and institutional budget classifications**
- 🧾 **Indicators of public debt, third-party expenses, and administrative deficits**
- ❗ **Labeled data for municipalities that have defaulted**

These files have been cleaned, normalized, and combined into a structure suitable for predictive modeling.

---

 📦 Key Files in This Repo

- `expense_data_main.csv`: Cleaned municipal budget data
- `defaulted_municipalities.csv`: Municipalities officially declared in financial distress
- `inhabitants_data.csv`: Yearly population statistics
- `income_data_with_population.csv`: Income and population data for contextual modeling
- `extractExpense.py` / `extractincome.py`: Scripts used for cleaning and preparing data

---

🧠 Planned ML Pipeline

- Data preprocessing & feature engineering
- Exploratory data analysis (EDA)
- Label encoding of bankruptcy status
- Model training (Logistic Regression, Random Forest, XGBoost, etc.)
- Evaluation using cross-validation and metrics like accuracy, precision, recall
- Model interpretation with SHAP / feature importance

---

📌 Long-Term Vision

The ultimate goal is to deploy this model as a tool for **public finance transparency**, enabling early detection of financial instability across municipalities and aiding decision-making for both internal governance and external oversight.

---

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change or add.

