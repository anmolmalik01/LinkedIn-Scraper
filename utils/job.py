def scrape_jobs(driver, jobs_url):
    """Scrape required fields from LinkedIn job page"""
    driver.get(jobs_url)
 
    for job in driver.find_elements(By.CSS_SELECTOR, "ul#jobs-home-vertical-list__entity-list li"):
        try:
            job_title = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute("innerText")
            company_name = job.find_element(By.CSS_SELECTOR, "span.job-card-container__primary-description").get_attribute("innerText")
            company_location = job.find_element(By.CSS_SELECTOR, "li.job-card-container__metadata-item").get_attribute("innerText")
        except:
            continue
 
        print("Job title: {}".format(job_title))
        print("Company name: {}".format(company_name))
        print("Company location: {}".format(company_location))