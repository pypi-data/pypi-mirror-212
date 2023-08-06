import os
from datetime import date, datetime
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import mande_integration_gisel.config as conf
from mande_integration_gisel import MandEIntegration
from mande_integration_gisel.utils import to_csv
from mande_integration_gisel.config import __DIR__
from mande_integration_gisel.config.types import PaginationDirection
from pprint import pprint
from data import data

def get_expenditure_report_data(project_code: str, browser: MandEIntegration) -> None:
    grant_expenditure_report = []
    browser.login()
    browser.open_grant(project_code, filter_by=project_code)
    browser.open_first_report()
    browser.open_expenditure_report()
    
    report_level = browser.get_category_header_list()

    for level in report_level:
        report_details = browser.retrieve_expenditure_report_data(
            project_code, level,
        )
        
        grant_expenditure_report.append(report_details)
    
    result = {
        "expenditures": grant_expenditure_report,
        "project": f"USADF-{project_code}"
    }
    pprint(result, indent=2, width=60)

def get_grant_data(project_code: str, browser: MandEIntegration) -> None:
    browser.login()
    browser.get_grant_data(project_code, filter_by=project_code)

def create_or_edit_expenditure_report(
    project_code: str, browser: MandEIntegration
) -> None:
    # Login
    browser.login()
    
    # clears filter
    browser.clear_filters()

    # Open Grants List
    browser.open_grant(project_code)

    report_period_start = datetime.strptime("2019-12-31", "%Y-%m-%d")
    report_period_end = datetime.strptime("2020-02-14", "%Y-%m-%d")

    # report_period_start = datetime.strptime('09/30/2018', '%m/%d/%Y')
    # report_period_end = datetime.strptime('11/14/2018', '%m/%d/%Y')

    # Open report List
    browser.open_reports(report_period_start, report_period_end)

    # Open expenditure report
    browser.open_expenditure_report()

    values = data.data
    categories = browser.get_category_header_list()

    # Create new report
    browser.edit_report(categories, values)

def main():
  # Get credentials
    email = os.getenv("USADF_GRANT_USERNAME")
    password = os.getenv("USADF_GRANT_TEST_PASSWORD")

    project_code = "400334"
    # project_code = '4377'
    # 2365, 2956, 4003, 4626, 2182
    # grants = ['2365', '2956', '4003', '4626', '2182']

    # Navigator options
    options = ChromeOptions()
    options.add_argument("headless")

    # Instantiate new MandE Integration Class
    browser = MandEIntegration(Chrome, email, password, options)

    # create_or_edit_expenditure_report(project_code, browser)

    get_grant_data(project_code, browser)

if __name__ == '__main__':
    main()