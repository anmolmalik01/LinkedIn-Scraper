
def scrape_company(driver, company_url):
    """Scrape required fields from LinkedIn Company URL"""
    driver.get(company_url + "about/")

    company_name = driver.find_element(By.CSS_SELECTOR, "h1 span").get_attribute("innerText")

    # Get company about container
    about_section = driver.find_element(By.CSS_SELECTOR, "section.org-page-details-module__card-spacing").get_attribute("innerHTML").strip()
    about_section = about_section.replace("\n", "")

    # Remove extra double spaces
    while True:
        if about_section.find("  ") > 0:
            about_section = about_section.replace("  ", " ")
        else:
            break

    # Scrape Website URL
    if about_section.find('Website </dt>') > 0:
        company_website = about_section.split('Website </dt>')[1]
        company_website = company_website.split('</dd>')[0]

        if company_website.find('href="') > 0:
            company_website = company_website.split('href="')[1]
            company_website = company_website.split('"')[0]
        else:
            company_website = ""

    # Scrape Company Industry
    if about_section.find('Industry </dt>') > 0:
        company_industry = about_section.split('Industry </dt>')[1]
        company_industry = company_industry.split('</dd>')[0]
        company_industry = company_industry.split('">')[1].strip()
    else:
        company_industry = ""

    # Scrape Company headquarter
    if about_section.find('Headquarters </dt>') > 0:
        company_headquarter = about_section.split('Headquarters </dt>')[1]
        company_headquarter = company_headquarter.split('</dd>')[0]
        company_headquarter = company_headquarter.split('">')[1].strip()
    else:
        company_headquarter = ""


    print("Company Name: {}".format(company_name))
    print("Website: {}".format(company_website))
    print("Industry: {}".format(company_industry))
    print("Headquarter: {}".format(company_headquarter))