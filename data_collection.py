# importing the glassdoor_scraper file for execution
import glassdoor_scraper as gs

# assigning the function to varible 'jobs_df'
# I have executed the code earlier so I know how many job postings are there in the website (total 901 job postings)
jobs_df = gs.find_jobs("Data Scientist", "India", 900, True)

# calling the function
jobs_df

# saving the dataframe to csv file
jobs_df.to_csv("jobs_data.csv", index=False)

