from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


class ApolloScrapeAutomation:
    def __init__(self, driver_path):
        # Initializing the webdriver
        service = Service(driver_path)
        self.driver = Chrome(service=service)

    def login(self):
        self.driver.get("https://app.apollo.io/#/login")

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located(
            (By.XPATH, '//input[contains(@name, "email")]')))
        self.driver.find_element(
            By.XPATH, '//input[contains(@name, "email")]').send_keys("thatsmystuff69@gmail.com")

        self.driver.find_element(
            By.XPATH, '//input[contains(@name, "password")]').send_keys("Kartik@12345")
        self.driver.find_element(By.XPATH, '//button[.= "Log In"]').click()

    def get_email(self, df, campaign_name):
        for index, row in df.iterrows():
            name_url = row['name_url']
            self.driver.get(name_url)
            try:
                self.driver.find_element(
                    By.XPATH, '//*[@id="general_information_card"]/div/div/div[1]/div[1]/div/div/div/div[2]/button[2]').click()
            except Exception:
                pass

            try:
                email_cls = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="general_information_card"]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div/a')))
                email = email_cls.text
            except:
                email = ''

            try:
                contact_cls = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="general_information_card"]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[3]/div/div[2]/div/div/div[1]/div[1]/a/span')))
                contact_number = contact_cls.text
            except:
                contact_number = ''

            df.at[index, 'Email'] = email
            df.at[index, 'Contact'] = contact_number

        df.to_csv(f"{campaign_name}.csv", index=False)

    def scrape_url(self, campaign_name):
        df = pd.DataFrame(
            columns=["name", "name_url", "linkedin_url", "title", "company", "company_url", "caddress", "employeeCounts", "Industry"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//div[@data-cy-loaded="true"]')))
        table = self.driver.find_elements(
            By.XPATH, '//div[@data-cy-loaded="true"]')
        rows = self.driver.find_elements(By.TAG_NAME, 'tr')

        try:
            for row in rows[1:]:
                name = ""
                name_url = ""
                linkedin_url = ""
                title = ""
                company_name = ""
                company_url = ""
                contact = ""
                employeecount = ""
                industry = ""
                keyword = ""
                email = ""
                phone_number = ""

                try:
                    name = row.find_element(
                        By.XPATH, './/div[@class="zp_xVJ20"]/a').text
                except Exception:
                    pass

                try:
                    name_url = row.find_element(
                        By.XPATH, './/div[@class="zp_xVJ20"]/a').get_attribute("href")
                except Exception:
                    pass

                try:
                    linkedin_url = row.find_element(
                        By.XPATH, './/div[@class="zp_I1ps2"]/span/a').get_attribute("href")
                except Exception:
                    pass

                try:
                    title = row.find_element(
                        By.XPATH, './/td[@class="zp_aBhrx"][2]/span[@class="zp_Y6y8d"]').text
                except Exception:
                    pass

                try:
                    company_name = row.find_element(
                        By.XPATH, './/a[@class="zp_WM8e5 zp_kTaD7"]').text
                except Exception:
                    pass

                try:
                    company_url = row.find_element(
                        By.XPATH, './/a[@class="zp_WM8e5 zp_kTaD7"]').get_attribute("href")
                except Exception:
                    pass

                try:
                    contact = row.find_element(
                        By.XPATH, './/td[@class="zp_aBhrx"][5]//span[@class="zp_Y6y8d"]').text
                except Exception:
                    pass

                try:
                    employeecount = row.find_element(
                        By.XPATH, './/td[@class="zp_aBhrx"][6]/span[@class="zp_Y6y8d"]').text
                except Exception:
                    pass

                try:
                    industry = row.find_element(
                        By.XPATH, './/td[@class="zp_aBhrx"][8]//span[@class="zp_lm1kV"]/div/span').text
                except Exception:
                    pass

                df.loc[len(df)] = [name, name_url, linkedin_url, title, company_name, company_url, contact, employeecount, industry]
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

        self.get_email(df, campaign_name)

    def run_scraper(self, dic_urls):
        for campaign_name, url in dic_urls.items():
            time.sleep(10)
            try:
                self.driver.get(url)
                time.sleep(10)
                self.scrape_url(campaign_name)
            except Exception as e:
                print(
                    f"Exception occurred while scraping {campaign_name}: {str(e)}")


if __name__ == "__main__":
    dic_urls = {
        "Fleet_leasing#1": "https://app.apollo.io/#/people?finderViewId=5b6dfc5a73f47568b2e5f11c&page=1&personTitles[]=fleet%20manager&personTitles[]=operation%20manager&personTitles[]=C-suit&personTitles[]=manager%20of%20operations&personTitles[]=managing%20director&personTitles[]=owner&personTitles[]=founder&personTitles[]=co%20founder&personTitles[]=ceo&personTitles[]=directors&organizationNumEmployeesRanges[]=10%2C&personLocations[]=Ontario%2C%20Canada&personLocations[]=Alberta%2C%20Canada&qOrganizationKeywordTags[]=Government%20Services&qOrganizationKeywordTags[]=Municipal&qOrganizationKeywordTags[]=Local%20Government&qOrganizationKeywordTags[]=Government%20fleet%20leasing&qOrganizationKeywordTags[]=government%20administration&qOrganizationKeywordTags[]=Environmental%20Services&qOrganizationKeywordTags[]=Waste%20Recycling%20and%20Management&qOrganizationKeywordTags[]=%22Waste%20management%20fleet%20leasing%22&qOrganizationKeywordTags[]=Food%20Distribution&qOrganizationKeywordTags[]=Wholesale%20Distributors&qOrganizationKeywordTags[]=%22Food%20distribution%20fleet%20leasing%22&qOrganizationKeywordTags[]=Food%20services&includedOrganizationKeywordFields[]=tags&includedOrganizationKeywordFields[]=name&contactEmailStatus[]=verified",
        "Fleet_leasing#2": "https://app.apollo.io/#/people?finderViewId=5b6dfc5a73f47568b2e5f11c&page=1&personTitles[]=fleet%20manager&personTitles[]=operation%20manager&personTitles[]=C-suit&personTitles[]=manager%20of%20operations&personTitles[]=managing%20director&personTitles[]=owner&personTitles[]=founder&personTitles[]=co%20founder&personTitles[]=ceo&personTitles[]=directors&organizationNumEmployeesRanges[]=10%2C&personLocations[]=Ontario%2C%20Canada&personLocations[]=Alberta%2C%20Canada&contactEmailStatus[]=verified&qOrganizationKeywordTags[]=Healthcare&qOrganizationKeywordTags[]=Non-emergency%20Medical%20Transport&qOrganizationKeywordTags[]=Medical%20transport%20fleet%20leasing&qOrganizationKeywordTags[]=IT%20Services&qOrganizationKeywordTags[]=IT%20and%20Network%20Support%20Services&qOrganizationKeywordTags[]=%22Manufacturing%20fleet%20operations%22&qOrganizationKeywordTags[]=Hospitality&qOrganizationKeywordTags[]=Hotel&qOrganizationKeywordTags[]=Resort%20Chains&qOrganizationKeywordTags[]=%22Hospitality%20industry%20fleet%20leasing%22&includedOrganizationKeywordFields[]=tags&includedOrganizationKeywordFields[]=name",
        "Fleet_leasing#3": "https://app.apollo.io/#/people?finderViewId=5b6dfc5a73f47568b2e5f11c&page=1&personTitles[]=fleet%20manager&personTitles[]=operation%20manager&personTitles[]=C-suit&personTitles[]=manager%20of%20operations&personTitles[]=managing%20director&personTitles[]=owner&personTitles[]=founder&personTitles[]=co%20founder&personTitles[]=ceo&personTitles[]=directors&organizationNumEmployeesRanges[]=10%2C&personLocations[]=Ontario%2C%20Canada&personLocations[]=Alberta%2C%20Canada&qOrganizationKeywordTags[]=Manufacturing&qOrganizationKeywordTags[]=Industrial%20Products&qOrganizationKeywordTags[]=Manufacturing%20fleet%20operations&qOrganizationKeywordTags[]=Landscaping&qOrganizationKeywordTags[]=Commercial%20Landscaping%20Services&qOrganizationKeywordTags[]=%22Landscaping%20fleet%20leasing%22&qOrganizationKeywordTags[]=%22Municipal%20fleet%20leasing%22&qOrganizationKeywordTags[]=Municipal%20Services&qOrganizationKeywordTags[]=Public%20Works&qOrganizationKeywordTags[]=Pest%20Control&qOrganizationKeywordTags[]=Pest%20Management%20Services&qOrganizationKeywordTags[]=%22Pest%20control%20fleet%20leasing%22&qOrganizationKeywordTags[]=Municipal&qOrganizationKeywordTags[]=pest%20services&qOrganizationKeywordTags[]=pest&qOrganizationKeywordTags[]=pest%20removel&includedOrganizationKeywordFields[]=tags&includedOrganizationKeywordFields[]=name&contactEmailStatus[]=verified",
        "Fleet_leasing#4": "https://app.apollo.io/#/people?finderViewId=5b6dfc5a73f47568b2e5f11c&page=1&personTitles[]=fleet%20manager&personTitles[]=operation%20manager&personTitles[]=C-suit&personTitles[]=manager%20of%20operations&personTitles[]=managing%20director&personTitles[]=owner&personTitles[]=founder&personTitles[]=co%20founder&personTitles[]=ceo&personTitles[]=directors&organizationNumEmployeesRanges[]=10%2C&personLocations[]=Ontario%2C%20Canada&personLocations[]=Alberta%2C%20Canada&qOrganizationKeywordTags[]=Real%20Estate%20Agencies&qOrganizationKeywordTags[]=Real%20estate%20fleet%20leasing&qOrganizationKeywordTags[]=real%20estate&qOrganizationKeywordTags[]=Recreation%20Services&qOrganizationKeywordTags[]=Parks&qOrganizationKeywordTags[]=Recreational%20Facility%20Management&qOrganizationKeywordTags[]=%22Recreational%20facility%20fleet%20leasing%22&qOrganizationKeywordTags[]=recreation&qOrganizationKeywordTags[]=Roadside%20Assistance&qOrganizationKeywordTags[]=Towing&qOrganizationKeywordTags[]=Roadside%20Service%20Companies&qOrganizationKeywordTags[]=%22Roadside%20assistance%20fleet%20leasing%22&includedOrganizationKeywordFields[]=tags&includedOrganizationKeywordFields[]=name&contactEmailStatus[]=verified",
        "Fleet_leasing#5": "https://app.apollo.io/#/people?finderViewId=5b6dfc5a73f47568b2e5f11c&page=1&personTitles[]=fleet%20manager&personTitles[]=operation%20manager&personTitles[]=C-suit&personTitles[]=manager%20of%20operations&personTitles[]=managing%20director&personTitles[]=owner&personTitles[]=founder&personTitles[]=co%20founder&personTitles[]=ceo&personTitles[]=directors&organizationNumEmployeesRanges[]=10%2C&personLocations[]=Ontario%2C%20Canada&personLocations[]=Alberta%2C%20Canada&contactEmailStatus[]=verified&qOrganizationKeywordTags[]=Telecommunications&qOrganizationKeywordTags[]=Field%20Services&qOrganizationKeywordTags[]=Telecom%20fleet%20management&qOrganizationKeywordTags[]=Security%20Services&qOrganizationKeywordTags[]=Private%20Security%20Companies&qOrganizationKeywordTags[]=%22Security%20services%20fleet%20leasing%22&qOrganizationKeywordTags[]=security&includedOrganizationKeywordFields[]=tags&includedOrganizationKeywordFields[]=name",
        "Fleet_leasing#6": "https://app.apollo.io/#/people?finderViewId=5b6dfc5a73f47568b2e5f11c&page=1&personTitles[]=fleet%20manager&personTitles[]=operation%20manager&personTitles[]=C-suit&personTitles[]=manager%20of%20operations&personTitles[]=managing%20director&personTitles[]=owner&personTitles[]=founder&personTitles[]=co%20founder&personTitles[]=ceo&personTitles[]=directors&organizationNumEmployeesRanges[]=10%2C&personLocations[]=Ontario%2C%20Canada&personLocations[]=Alberta%2C%20Canada&qOrganizationKeywordTags[]=Energy&qOrganizationKeywordTags[]=Oil%20%26%20Gas%20Exploration%20and%20Services&qOrganizationKeywordTags[]=Energy%20sector%20fleet%20leasing&qOrganizationKeywordTags[]=Emergency%20Services&qOrganizationKeywordTags[]=Fire&qOrganizationKeywordTags[]=police&qOrganizationKeywordTags[]=EMS&qOrganizationKeywordTags[]=%22Emergency%20services%20fleet%20leasing%22&qOrganizationKeywordTags[]=Environmental%20Consulting&qOrganizationKeywordTags[]=Environmental%20Survey&qOrganizationKeywordTags[]=Inspection&qOrganizationKeywordTags[]=%22Environmental%20consulting%20fleet%20leasing%22&includedOrganizationKeywordFields[]=tags&includedOrganizationKeywordFields[]=name&contactEmailStatus[]=verified",


    }
    apolloio = ApolloScrapeAutomation("C:/Users/krast/chromedriver-win64/chromedriver.exe")
    apolloio.login()
    apolloio.run_scraper(dic_urls)