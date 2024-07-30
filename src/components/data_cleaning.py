import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv')

df1 = df.copy()



 

# 1. Preprocessing 'Salary Estimate'
# removing unwanted texts 
# handling missing values
# creating new columns from 'Salary Estimate' 

# split the texts from salary 
salary = df1['Salary Estimate'].apply(lambda x: x.split('(')[0])
salary = salary.apply(lambda x: x.split('/')[0])


# removing the ₹ symbol and L text
salary = salary.apply(lambda x: x.replace('₹', '').replace('L', '')) 


# replacing missing values with the minimum salary range of 4LPA and the maximum salary range of 30LPA
salary = salary.replace('-1', '4 - 30')


# filtering the salaries which are in thousands 
filtered_salary = salary[salary.str.contains(r'[T\.]')]
filtered_salary.value_counts() 


# converting the thousands into lakhs with the average value which was found from 'filtered_salary' series
replacement_value = '2 - 10'
salary= salary.replace(to_replace=r'.*[T\.].*', value=replacement_value, regex=True)


# we have to split the salary  by '-' and '–' 
# spliting the salary into two separate series and storing them in new columns 
df1[['min_salary', 'max_salary']] = salary.str.split('–|-', expand=True)


# filling NaN values in 'max_salary' column with corresponding values from 'min_salary' column
df1['max_salary'] = df1['max_salary'].fillna(df1['min_salary'])


# there is a 'Cr' value in the 'min_salary' & 'max_salary' of the 626 row, we have to remove it 
df1.loc[626, ['min_salary', 'max_salary']] = df1.loc[626, ['min_salary', 'max_salary']].str.replace('Cr', '')


# the salary in 626 row is in crores therofore we have to convert it into lakhs
df1.loc[626, ['min_salary', 'max_salary']] = df1.loc[626, ['min_salary', 'max_salary']].replace('1', '8')


# converting the dtype of 'min_salary' and 'max_salary'
df1[['min_salary', 'max_salary']] = df1[['min_salary', 'max_salary']].astype('int64')


# finding the average salary 
df1['avg_salary'] = (df1.min_salary+df1.max_salary)/2
df1['avg_salary'] = df1['avg_salary'].astype('int64')


# dropping the 'Salary Estimate' columns as we no longer need it
df1.drop(['Salary Estimate'], axis=1, inplace=True)


# double checking the new columns
df1[['min_salary', 'max_salary', 'avg_salary']].isna().any()





# 2. Preprocessing 'Rating' 
# handling missing values 

# finding the most suitable value to replace NaN 
df1['Rating'].value_counts(ascending=False)
df1['Rating'].describe()


# filling NaN values with 4.0
# more than half of the ratings are higher than or equal to 4.0 
df1['Rating'] = df1['Rating'].replace(-1, 4.0)


# dtype of rating 
df1['Rating'].dtype


# double checking for missing values
df1['Rating'].isna().any()





# 3. Preprocessing 'Size'
# handling missing values

# filling NaN values with:
# the most repeated value is 10000+ employees 
# most of the company's size in India is not more than 10000+ employees but 100-500 and 1000-5000 employees
# therefore we will be using 51-200, 1000-5000 and 10000+ employees to fill the NaN values
df1['Size'].value_counts()


# Define replacement values
replacement_values = {
    '-1': '1001 to 5000 Employees',
    'Unknown': '201 to 500 Employees',
    '4.1': '201 to 500 Employees',
    '3.9': '201 to 500 Employees',
    '4.4': '201 to 500 Employees',
    '3.8': '10000+ Employees',
    '3.7': '10000+ Employees',
    '4.0': '10000+ Employees',
    '4.2': '10000+ Employees',
    '3.5': '10000+ Employees',
    '4.5': '10000+ Employees',
    '3.6': '10000+ Employees',
    '3.4': '10000+ Employees',
    '4.3': '10000+ Employees',
    '4.7': '10000+ Employees',
    '4.8': '10000+ Employees',
    '4.6': '10000+ Employees',
    '5.0': '10000+ Employees',
    '3.3': '10000+ Employees',
    '4.9': '10000+ Employees',
    '3.1': '10000+ Employees',
    '2.9': '10000+ Employees',
    '1.0': '10000+ Employees',
    '3.0': '10000+ Employees',
    '2.6': '10000+ Employees',
    '2.7': '10000+ Employees',
    '3.2': '10000+ Employees',
    '2.8': '10000+ Employees'   }


# Replace values in the 'Size' column using the replacement dictionary
df1['Size'] = df1['Size'].replace(replacement_values)


# replacing 'to' with '-'
df1['Size'] = df1['Size'].str.replace('to', '-', regex=True) 



# 4. Preprocessing 'Industry'
# handling missing values

# finding most suitable value to replace missing values
df1.Industry.value_counts()


# Defining the common industry values
common_industries = ['Information Technology Support Services',
                     'Enterprise Software & Network Solutions',
                     'Business consulting' ]


# Replace '-1' and '--' values nan 
df1['Industry'].replace({'-1': np.nan, '--': np.nan}, inplace=True)


# filling nan with 'common_industries' on random selection
df1['Industry'].fillna(pd.Series(np.random.choice(common_industries, size=len(df1.index))), inplace=True)





# 5. Preprocessing 'Sector'
# handling missing values

df1.Sector.value_counts()


# defining the common sector values 
common_sectors = ['Information Technology', 
                  'Finance',
                  'Manufacturing',
                  'Management and consulting']


# replacing -1 and -- with nan
df1['Sector'].replace({'-1': np.nan, '--': np.nan}, inplace=True)


# filling nan with 'common_sectors' on random selection
df1['Sector'].fillna(pd.Series(np.random.choice(common_sectors, size=len(df1.index))), inplace=True)





# 6. Preprocessing 'Founded'
# handling missing values
# creating new feature 'age'

# determining the most suitable replacement values 
df1['Founded'].value_counts()
found = df1['Founded'][(df1['Founded'] != '-1') & (df1['Founded'] != '--')]
sns.distplot(found)
found = found.astype('int64')
plt.scatter(found.index, found.values)
plt.show()
found.value_counts().head(40)   # couldn't find suitable replacement values, going with forward fill


df1['Founded'].value_counts().head(30)


# replacing '-1' and '--' with NaN
df1['Founded'] = df1['Founded'].replace({'-1': np.nan, '--': np.nan})


# Converting 'Founded' column to numeric dtype, handling missing values
df1['Founded'] = pd.to_numeric(df1['Founded'], errors='coerce')


# filling nan values with forward fill method as missing values are completely at random
# mean/mode imputation is not suitable as we are dealing with 'Founded' column
df1['Founded'] = df1['Founded'].ffill()


# there still some missing values that are not replaced
df1[df1['Founded'].isna()]


# we have to separately replace the 1st row of founded column as ffill() method will not work for it
df1['Founded'].fillna(2006, inplace=True)


# create a new feature which is the age of the company
df1['age'] = df1.Founded.apply(lambda x: x if x < 1 else 2024 - x)




# 7. Preprocessing 'Ownership'
# handling missing values

# observing values and its counts
df1['Ownership'].value_counts()


# among the many companies in India including foreign based the ownership is either public or private
# therefore we can fill 60% of the missing values with Private and rest 40% with Public
private_missing = int(0.6 * 332)  # 60% of 332
public_missing = int(round(0.4 * 332))  # 40% of 332


# list containing values for filling missing values
private_fill = ['Company - Private'] * private_missing
public_fill = ['Company - Public'] * public_missing


# replacing '-1' and 'Unknown' with NaN in the 'Ownership' column
df1['Ownership'].replace({'-1': np.nan, 'Unknown': np.nan}, inplace=True)


# 'Ownership' after .loc[] specifies the column where the replacement will occur which is the 'Ownership' column
df1.loc[df1['Ownership'].isna(), 'Ownership'] = private_fill + public_fill





# 8. Preprocessing 'Revenue'
# handling missing values 
# removing unwanted texts 

df1['Revenue'].value_counts()


# replacement values
reven_replacement = ['$10+ billion (USD)',           
                     '$2 to $5 billion (USD)', 
                     '$100 to $500 million (USD)']


# replacing -1 and unknown with NaN
df1['Revenue'] = df1['Revenue'].replace({'-1': np.nan, 'Unknown / Non-Applicable': np.nan})


# in total we have to replace 602 nan values 
df1.Revenue.isna().sum()


# 70% of 602 values to be replaced with '$10+ billion (USD)'
# 20% of 602 values to be replaced with  '$2 to $5 billion (USD)'
# 10% of 602 values to be replaced with '$100 to $500 million (USD)'
seventy_per = int(0.7 * 602)    
twenty_per = int(0.2 * 602)
ten_per = int(0.102 * 602) # 10.2% to get 61 not 60

seventy_fill = ['$10+ billion (USD)'] * seventy_per
twenty_fill = ['$2 to $5 billion (USD)'] * twenty_per
ten_fill = ['$100 to $500 million (USD)'] * ten_per


# replacing the nan values of 'Revenue' column with those 3 replacement values
df1.loc[df1['Revenue'].isna(), 'Revenue'] = seventy_fill + twenty_fill + ten_fill


# removing '$' and '(USD)'
df1['Revenue'] = df1['Revenue'].str.replace(r'[$(USD)]', '', regex=True) 


# replacing 'to' with '-'
df1['Revenue'] = df1['Revenue'].str.replace('to', '-', regex=True)


# converting billions to millions 
df1['Revenue'] = df1['Revenue'].str.replace('10+ billion', '10000+ million')
df1['Revenue'] = df1['Revenue'].str.replace('2 - 5 billion', '2000 - 5000 million')
df1['Revenue'] = df1['Revenue'].str.replace('5 - 10 billion', '5000 - 10000 million')
df1['Revenue'] = df1['Revenue'].str.replace('500 million - 1 billion', '500 - 1000 million')
df1['Revenue'] = df1['Revenue'].str.replace('Less than 1 million', '1 - 5 million')





# 9. Preprocessing 'Job Description'
# parsing keywords 

# 1 if is present in 'Job Description' else 
# python
df1['python'] = df1['Job Description'].str.contains('Python', case=False).astype(int)


# r studio
df1['r'] = df1['Job Description'].str.contains('r studio', case=False).astype(int)


# spark
df1['spark'] = df1['Job Description'].str.contains('spark', case=False).astype(int)


# aws 
df1['aws'] = df1['Job Description'].str.contains('aws', case=False).astype(int)


# excel
df1['excel'] = df1['Job Description'].str.contains('excel', case=False).astype(int)


# GenAI
df1['genai'] = df1['Job Description'].str.contains('GenAI', case=False).astype(int)


# LLMs
df1['LLMs'] = df1['Job Description'].str.contains('LLM', case=False).astype(int)


# Sql
df1['sql'] = df1['Job Description'].str.contains('sql', case=False).astype(int)





# saving the file 
df1.to_csv("data_cleaned.csv", index=False)
