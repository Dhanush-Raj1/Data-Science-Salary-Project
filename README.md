# End to End Data Science Project "Predicting Salary of a Data Scientist in India". 
## Project Overview :
   - Developed a robust model to predict the salary of Data Scientists in India.
   - Collected data from glassdoor website, scraped over 900 job postings.
   - Cleaned and pre-processed the raw data. 
   - Engineered featues, created new features that captures the importance of tools like 'python', 'r', 'sql', 'aws', 'spark', 'genai', 'LLMs' for a data science role.
   - Trained the model by utilizing different machine learning algorithms, optimized it using cross validation, gridsearch methods.
   - Deployed the model as an application using Flask, pickle.


## 1. Data Collection:
   - Using selenium framework I scraped the Data Science job postings within India from the glassdoor website. 
   - Scraped all the job postings from the website (around 900 job postings).
   - For each job I collected the following:
       * Company Name
       * Job Title
       * Salary Estimate 
       * Location of the job
       * Job Description
       * Rating of the company
       * Size of the company (total number of employees working)
       * Industry
       * Sector
       * Founded date of the company
       * Ownership type of the company
       * Revenue of the company
   - Took me a while to complete the scraping process (around 3 hours for the scraping process to complete).


## 2. Data Cleaning & Preprocessing: 
   - Once the data is scraped I performed data clearning process and also prepared the data for model building.
   - During the clearning process I did the following:
        * Filled the missing values using the most suitable method (there were a lot of missing values so couldn't just drop it)
        * Removed unwanted text, black spaces from the values of different columns
        * Parsed numeric data from 'Salary Esitmate' column.
        * Found the age of the company using 'Founded' column.
        * Created the following new columns for the skills, tools listed in 'Job Description' column 
             * Python
             * r
             * sql
             * aws
             * spark
             * genai
             * LLMs

## 3. Exploratory Data Analysis & Feature Engineering:
   - Once the data is clearned I analyzed the data to find hidden patterns, trends other relationship between features.
   - Performed both univariate and bivariate/multi-variate analysis.
   - Visualized the distribution of each features and explored the values and their counts of each features.
   - Visualized the presence of missing values in the dataset.
   - Found relationship (correlation) between features.
   - Found relationship between the revenue of the company and the salary they provide.
   - Found the companies which has higher ratings (more than 4.0 & 4.5)
   - Found the common industries and sectors the company is in and so on.

<img src="https://github.com/Dhanush-Raj1/Data-Science-Salary-Project/blob/main/eda_images/correlation.png" width="500" height="500">  

<img src="https://github.com/Dhanush-Raj1/Data-Science-Salary-Project/blob/main/eda_images/founded_date.png" width="500" height="500">   

<img src="https://github.com/Dhanush-Raj1/Data-Science-Salary-Project/blob/main/eda_images/location.png" width="500" height="500">  

<img src="https://github.com/Dhanush-Raj1/Data-Science-Salary-Project/blob/main/eda_images/missing_values.png" width="500" height="500">  

<img src="https://github.com/Dhanush-Raj1/Data-Science-Salary-Project/blob/main/eda_images/word_cloud.png" width="600" height="500">  

        

        
