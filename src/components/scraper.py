from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd


def find_jobs(keyword, location, num_jobs, verbose):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    # path of chromedriver
    path = Service("F:/Data Science/Data-Science-Salary-Project/chromedriver.exe")
    
    # Initializing chrome_options
    chrome_options = Options()
    
    # opening the new chrome window with maximum size
    chrome_options.add_argument("--start-maximized")
    
    # timeout value for 10 seconds
    chrome_options.add_argument('--timeout=15')
    
    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # chrome_options.add_argument('headless')

    # initializing the driver
    driver = webdriver.Chrome(service=path, options=chrome_options)
    
    #driver.set_window_size(1120, 1000)

    # url of the website
    url = "https://www.glassdoor.co.in/Job/SRCH_KO0,14.htm"

    # connecting to the url
    driver.get(url)

    # wait time of 3 seconds for the website to load
    time.sleep(3)

    # finding the search tababs
    search_tab = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/form/div[2]/div[1]/div/input")

    # entering the search text
    search_tab.send_keys(keyword)

    # clicking "ENTER" key to initiate search
    search_tab.send_keys(Keys.ENTER)

    # 2 seconds wait time before finding the location tab
    time.sleep(2)
    
    # finding the location tab
    location_tab = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/form/div[2]/div[2]/div/input")

    # entering the location 
    location_tab.send_keys(location)

    # clicking the "ENTER" key 
    location_tab.send_keys(Keys.ENTER)

    # empty list for storing the scraping data
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        # 4 seconds wait time for the website to load
        time.sleep(4)

        # clicking on the 2nd job (div class) to check for the signup prompt
        try:
            driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[2]/div/div/div[1]/div[1]").click()
        except ElementClickInterceptedException:    
            pass  
            
        # 3 seconds wait time for the signup prompt to appear
        time.sleep(3)

        # closing the signup prompt by clicking on the "X"
        try:
            driver.find_element(By.XPATH, "/html/body/div[11]/div[2]/div[2]/div[1]/button").click() 
            time.sleep(2)
            print('x out worked')
        except:
            print('x out failed')
            pass
        
        time.sleep(3)

        # clicking the show more button till all the job postings has been loaded then we can scrape all the jobs one by one
        while True:
            time.sleep(3)
            try:
                show_more = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/div/button")
                show_more.click()
            except NoSuchElementException:
                break        
        
        # Going through each job postings
        job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv") 
        
        time.sleep(3)
        
        print('Number of jobs found:', len(job_buttons))

        for job_button in job_buttons:  
            #print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            print("Progess: ", str(len(jobs)) + "/", str(num_jobs)) 
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:

                # the below details are present in every job postings and does not need a 'not found value'
                try:
                    # the xpath of all the company names is the same except for the 4th job 
                    # /html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]/a/div[2]/h4
                    # 4th job's different xpath
                    # /html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]/div[1]/div/h4

                    # chatgpt made a change to the xpath and it works
                    company_name = driver.find_element(By.XPATH, "//h4[contains(@class, 'heading')]").text
                    job_title = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]/h1").text 
                    job_description = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/div[2]/div[1]").text
                    collected_successfully = True
                except:
                    time.sleep(5)

                
                # the below details are not present in every job postings therefore need a 'not found value'
                try:
                    location = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]/div").text
                except NoSuchElementException:
                    location = -1              # -1 is for not found value
                    
                try:
                    salary_estimate = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section/div/div[1]/div[1]/div[2]").text
                except NoSuchElementException:
                    salary_estimate = -1       # -1 is for "not found value.
            
                try:
                    rating = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]/a/div[2]/div/span").text                                                 
                except NoSuchElementException:
                    rating = -1                # -1 is for "not found value.


            
            #Printing for debugging
            if verbose:
                print("Company Name: {}".format(company_name))
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Location: {}".format(location))
                print("Rating: {}".format(rating))
                


            # clicking on the company overview inside a job posting 
            try:
                driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/h2").click()

                try:
                    size = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[1]/div").text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[2]/div").text
                except NoSuchElementException:
                    founded = -1

                try:
                    ownership = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[3]/div").text
                except NoSuchElementException:
                    ownership = -1

                try:
                    industry = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[4]/div").text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[5]/div").text
                except NoSuchElementException:             
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[6]/div").text
                except NoSuchElementException:
                    revenue = -1

            except NoSuchElementException:    # some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                ownership = -1
                industry = -1
                sector = -1
                revenue = -1


            
            # printing for debugging 
            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Ownership: {}".format(ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


            # add the collected details to jobs(an empty list which we created before the while loop)            
            jobs.append({"Company Name" : company_name,
            "Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Location" : location,
            "Job Description" : job_description,
            "Rating" : rating,
            "Size" : size,
            "Industry" : industry,
            "Sector" : sector,
            "Founded" : founded,
            "Ownership" : ownership,
            "Revenue" : revenue})
            
            time.sleep(4)



    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.