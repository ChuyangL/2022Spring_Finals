# 2022Spring_Finals: Analysis changes in Lending data and relationship with state income
## Group members: 
Chuyang Li(chuyangl), github: ChuyangL  
Zheng Zhang(zhengz13), github: gahsty   
Yuting Xu(yutingx4), github: Msz-cx  

## Introduction of lending club
![image](https://user-images.githubusercontent.com/54805284/166623043-b7d1802a-7600-40db-8a57-bcdd6c17012a.png)

## Lending Club Loan Data Analysis
1. 10,000 rows, 55 columns, multiple data types, and has null value for some columns.
2. Value ranges for variables
   Numerical Variables: summary statistics (max, min, mean, ...)
   Categorical Variables: unique values and value count
3. Distribution of important variables
   3.1 Continuous Variables: Interest Rate, Loan Amount, Installment (monthly)
       Features: Right-skewed, higher proportion on bad loans as the values increase
   3.2 Categorical Variables: Term (36 or 60), Subgrades, Length of Employment, Purpose of Loan
       Features: Not evenly distributed
4. Geographical Distribution: Percentage of Good/Bad Loans, Loans Per User

## Limitation of current research
1. The analysis is based on the customer database of the company “Lending Club”, which might contain bias as it could not represent features of all loan transactions in the US.  
2. Current research shows concentration in geographic of users, which may cause bias.  
3. Lack of evidence about independency between variables while doing correlation analysis.  

## Hypothesis
1. The borrowers using Lending Club have worse economic situations(lower annual income, income/debt ratio, asset/debt ratio) than borrowers from all other lenders.  
2. The DTI (debt to income ratio) has negative correlations to the number of years that the applicant is in the job.  
3. People with higher annual incomes are more likely to make repayments on time.  

## Data Sources
### 1. Loan data from Lending Club
Source: https://www.lendingclub.com/info/statistics.action (Lending Club)  
Detailed Description: https://www.openintro.org/data/index.php?data=loans_full_schema  
### 2. Survey of Consumer Finances
Source(2010): https://www.federalreserve.gov/econres/scf_2010.htm#EXCELDATEX  
Source(2019): https://www.federalreserve.gov/econres/scfindex.htm  
Detailed Description: https://sda.berkeley.edu/sdaweb/docs/scfcomb2019/DOC/hcbkx01.htm#1.HEADING  
### 3. consumer price index
Source: https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-  

## Raw analysis on Lending Club dataset
https://kazink36.github.io/pdf/loans.html  

## Instructions to use the code
Ensure project.py and Final_project.ipynb are in the same directory, run cells Final_project.ipynb in order to get the right output. The project.py stores functions that would be called in notebook and has been imported at the top of the notebook.   

## Main conclusions of the hypothesis
![image](https://user-images.githubusercontent.com/54805284/167269153-115ab373-1e9d-48a9-803a-3a3222994558.png)
1. About 40% general borrowers have a debt-to-income ratio less than 0.5, which is a healthy ratio. And about 90% general borrowers have a ratio less than 1.5. For lending club users, their debt-to-income ratio is greater than 5, the main range is betwen 10-40, which is very unhealthy. According to most commercial banks, the DTI requirement for conducting a regular conforming Loan authorization is usually 43%. As a conclusion, lending club users have higher debt-to-income ratio, as well as worse economice situation than borrowers from all other lending resources.
![image](https://user-images.githubusercontent.com/30657669/167276830-62ec0ed8-9f3a-4261-b84f-49308dbdb346.png)
![image](https://user-images.githubusercontent.com/30657669/167276834-295c998d-92e7-48d3-86ed-50ffe574b771.png)
2. The DTI (debt to income ratio) has no correlations to the number of years that the applicant is in the job, but it do has a positive relationship with other factors such as people's total credit and current number of accounts. 
![image](https://user-images.githubusercontent.com/30657669/167276816-a021ec71-a52a-47a3-b0e2-fc7b89b118a3.png)
3. People's annual incomes are not related to loan status (whether people make repayment on time).
