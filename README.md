# Task 1: Business Sales Performance Analytics

**Intern:** Santu Mondal  
**CIN ID:** FIT/OCT26/DS24105  
**Domain:** Data Science & Analytics  
**Tools Used:** Python (pandas, matplotlib, ReportLab), Power BI

---

## 📌 Project 1: Online Retail Dataset (Kaggle) (1)

**Objective:** Provide a quick, client-ready visual summary of key business metrics from the Online Retail Dataset.

👉 **[Click here to view Project 1 Dashboard (PDF)](dashboard.pdf)**

---

## 📌 Project 2: Superstore Sales Dataset (2)

**Objective:** Help a retail business understand which products, categories and regions drive revenue and profit, how sales change over time, and where to focus to grow faster.

👉 **[Click here to view Project 2 Full Report (PDF)](README.pdf)** *(Make sure to upload the file with this name)*

### 📊 Dataset
Sample Superstore: four years of US orders (Jan 2014 to Dec 2017), 9,994 order lines and 21 columns. No missing values or duplicate rows were found.

### 🛠️ Approach
- **Cleaning:** Standardised column names, converted dates, checked duplicates, added Year, Month, Profit Margin and Shipping Days.
- **KPIs:** Total sales, profit, margin, orders, customers and average order value.
- **Analysis:** Trends by month and year, category, sub-category, region, segment, state, discount level and top products.
- **Dashboard:** Single-page visual summary with insights and recommendations.

### 📈 Headline KPIs

| Total Sales | Total Profit | Profit Margin | Orders | Customers | Avg Order Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$2.30M** | **$286K** | **12.47%** | **5,009** | **793** | **$459** |

### 🔍 Key Findings
- Sales grew from $484K (2014) to $733K (2017), but profit margin stayed near 13%.
- Discounts above 20% are loss-making: the 21-40% band runs at -15% margin and above 40% at -77%, about $135K lost in total.
- Furniture earns only 2.5% margin. Tables (-$17.7K) and Bookcases (-$3.5K) lose money.
- Technology and Office Supplies produce about 94% of total profit at roughly 17% margin.
- West and East lead on profit. Central has the lowest margin (7.9%); Texas, Ohio, Pennsylvania and Illinois are unprofitable.
- Sales peak in September, November and December; January and February are the weakest months.

### 💡 Recommendations
- Cap discounts at 20% and require approval for anything higher.
- Reprice Tables and Bookcases, or renegotiate supplier costs.
- Review pricing and shipping costs in the four loss-making states.
- Promote high-margin lines (Copiers, Accessories, Office Supplies) in marketing.
- Build stock and run campaigns before September and November; use January and February for clearance and bundles.

### 📁 Project 2 Repository Files
- `README.pdf` - Full project report
- `analysis.py` - Data cleaning and KPI script
- `make_dashboard_image.py` - Generates the dashboard image
- `cleaned_superstore.csv` - Cleaned dataset
- `Sample_-_Superstore.csv` - Raw data

---
*This project was completed as part of the Data Science & Analytics Internship at Future Interns.*
