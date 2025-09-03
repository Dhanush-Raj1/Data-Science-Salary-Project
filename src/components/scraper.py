import time
import sys
import pandas as pd
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.exception_handling import Custom_Exception
from src.logger import logging

def find_jobs(keyword:str) -> pd.DataFrame: 
    '''
    Scraps job postings and returns the job posting as a DataFrame'''

    # path of chromedriver
    path = Service("F:/Data Science/Projects/2.Data-Science-Salary-Project/chromedriver1.exe")
    
    # Initializing chrome_options
    chrome_options = Options()
    #chrome_options.add_argument("--window-size=1920,1080")   
    chrome_options.add_argument("--start-maximized")     
    #chrome_options.add_argument('--timeout=15')                   # timeout value for 15 seconds
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument('headless')
    chrome_options.add_argument("--no-sandbox")                   # to avoid issues with sandboxing
    chrome_options.add_argument("--disable-gpu")                  # to avoid issues with GPU

    # initializing regular driver
    #driver = webdriver.Chrome(service=path, options=chrome_options)

    # initializing undetected_chromedriver
    driver = uc.Chrome(service=path, options=chrome_options)

    try:

        # url of the website
        #url = "https://www.glassdoor.co.in/Job/index.htm"
        url = "https://www.glassdoor.co.in/Job/data-scientist-jobs-SRCH_KO0,14.htm?locT=C&sc.keyword=data%20scientist"

        try:
            logging.info(f"Attempting to navigate to: {url}")
            driver.get(url)
            time.sleep(5)
            logging.info(f"Successfully navigated to: {driver.current_url}")
        except Exception as e:
            logging.error(f"Error navigating to URL: {str(e)}", sys)

        # try:
        #     # enter the job title on the search bar
        #     logging.info("Entering the job title")
        #     search_tab = driver.find_element(By.ID, "searchBar-jobTitle")  
        #     search_tab.send_keys(keyword)
        #     search_tab.send_keys(Keys.ENTER)
        #     time.sleep(3)

        #     # enter the location on the location bar
        #     logging.info("Entering the location")
        #     location_tab = driver.find_element(By.ID, "searchBar-location")              
        #     location_tab.send_keys(location)
        #     location_tab.send_keys(Keys.ENTER) 
        #     logging.info(f"Searching for job title: {keyword} and location: {location}")
        #     time.sleep(4)
        # except Exception as e:
        #     logging.error(f"Error finding search and location bar: str{(e)}", sys)

        try: 
            # click the 2nd job posting to check for sign-in popup 
            logging.info("Checking for sign-in popup...")
            #element = driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/ul/li[2]")
            #element = driver.find_element(By.XPATH, "//li[@data-jobid='1009764455757']")

            wait = WebDriverWait(driver, 10)
            job_cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@data-test="jobListing"]')))

            # Click the 2nd job card
            if len(job_cards) >= 2:
                second_job = job_cards[1]
                driver.execute_script("arguments[0].scrollIntoView(true);", second_job)
                second_job.click()
            else:
                print("Less than 2 job postings available.")

            time.sleep(3)
            #element.click()
    
            # close sign-in popup 
            close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'CloseButton')]"))
                    )
            if close_button.is_displayed():
                logging.info("Sign-in popup is displayed, closing it...")
            time.sleep(2)
            close_button.click()
            logging.info("Closed the sign-in popup")
        except Exception as e:
            raise Custom_Exception(f"Error closing popup: {str(e)}", sys)


        # click the "Show More" button to load more job postings
        logging.info("Loading all job postings...")
        while True:
            time.sleep(3)
            try:
                show_more_button = driver.find_element(By.XPATH, "//button[@data-test='load-more']")
                #show_more_button.click()
                driver.execute_script("arguments[0].click();", show_more_button)
                logging.info("Clicked 'Show More' button")
            except NoSuchElementException:
                logging.info("No more 'Show More' button found - all jobs loaded")
                break
            except Exception as e:
                logging.error(f"Error clicking 'Show More' button: {str(e)}")
                break

        time.sleep(6)

        job_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'JobsList_jobListItem__wjTHv')]")
        time.sleep(3)
        logging.info(f"Number of Job positings found: {len(job_elements)}")
        print(f"Number of job postings found: {len(job_elements)}")

        jobs = []

        missing_company_rating = 0
        missing_description = 0
        missing_location = 0
        missing_salary = 0
        missing_median_salary = 0

        logging.info("Starting scraping")

        # Loop through each job element 
        for i, job_element in enumerate(job_elements):
            logging.info(f"Progress: {i+1} / {len(job_elements)}")
            print(f"Progress: {i+1} / {len(job_elements)}")

            try:
                # Scroll to element to ensure it's visible
                driver.execute_script("arguments[0].scrollIntoView(true);", job_element)
                time.sleep(1)
                
                job_element.click()
                
                # Wait for job details pane to load completely
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'heading_Level1')]"))
                )
                time.sleep(4)  # Increased wait time for dynamic content
            except Exception as e:
                logging.error(f"Error loading job details pane for job {i+1}: {e}")
                continue 

            try:
                company_name = driver.find_element(By.XPATH, "//h4[contains(@class, 'heading_Subhead')]").text
                job_title = driver.find_element(By.XPATH, "//h1[contains(@class, 'heading_Level1')]").text
            except Exception as e:
                logging.error(f"Error scraping basic details for job {i+1}: {str(e)}")
                continue
            
            try: 
                company_rating = job_element.find_element(By.XPATH, ".//span[contains(@class, 'rating-single-star_RatingText__XENmU')]").text
            except NoSuchElementException:
                company_rating = "N/A"
                missing_company_rating += 1

            try:    
                description = driver.find_element(By.XPATH, ".//div[contains(@class, 'JobDetails_jobDescription')]").text.strip()
            except NoSuchElementException:
                description = "N/A"
                missing_description += 1

            try:
                location = driver.find_element(By.XPATH, "//div[@data-test='location']").text
            except NoSuchElementException:
                location = "N/A"
                missing_location += 1

            # Attempt to find salary range
            salary_range = "N/A"
            salary_attempts = 0
            max_salary_attempts = 3
            
            while salary_range == "N/A" and salary_attempts < max_salary_attempts:
                salary_attempts += 1
                try:
                    # Wait explicitly for salary elements to be present
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'SalaryEstimate_salaryRange__brHFy')]"))
                    )
                    
                    salary_element = driver.find_element(By.XPATH, "//div[contains(@class, 'SalaryEstimate_salaryRange__brHFy')]")
                    salary_range = salary_element.text.strip()
                    
                    if salary_range and salary_range != "":
                        break
                    else:
                        time.sleep(2)  # Wait before retry
                        
                except (NoSuchElementException, TimeoutException):
                    if salary_attempts < max_salary_attempts:
                        logging.info(f"Salary not found on attempt {salary_attempts}, retrying...")
                        time.sleep(1)
                    continue
            
            if salary_range == "N/A":
                missing_salary += 1
                logging.warning(f"Could not find salary for job {i+1}: {company_name} - {job_title}")

            # Attempt to find median salary
            median_salary = "N/A"
            try:
                # Wait for median salary elements
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'SalaryEstimate_medianEstimate__fOYN1')]"))
                )
                
                median_value = driver.find_element(By.XPATH,"//div[contains(@class, 'SalaryEstimate_medianEstimate__fOYN1')]").text.strip()
                median_suffix = driver.find_element(By.XPATH,"//div[contains(@class, 'SalaryEstimate_payPeriod__RsvG_') and contains(text(), 'Median')]").text.strip()
                median_salary = f"{median_value}{median_suffix}"
            except (NoSuchElementException, TimeoutException):
                median_salary = "N/A"
                missing_median_salary += 1

            jobs.append({
                "Company Name": company_name,
                "Company Rating": company_rating,
                "Job Title": job_title,
                "Location": location,
                "Description": description,
                "Salary Range": salary_range,
                "Median Salary": median_salary
            })

            print(
                f"Scraped job {len(jobs)}: "
                f"company_name: {company_name}, "
                #f"job_title: {job_title}, "
                f"company_rating: {company_rating}, "
                #f"Location: {location}, "
                #f"Description: {description[:100]}..., "
                f"Salary_range: {salary_range}, "
                f"Median_salary: {median_salary}\n\n"
            )

        logging.info(f"Scraping completed. Total jobs scraped: {len(jobs)}")
        logging.info(
            f"Missing fields - "
            f"Company rating: {missing_company_rating}, "
            f"Description: {missing_description}, "
            f"Location: {missing_location}, "
            f"Salary: {missing_salary}, "
            f"Median Salary: {missing_median_salary}"
        )
        
        df = pd.DataFrame(jobs)
        return df

    finally:
        driver.quit()
