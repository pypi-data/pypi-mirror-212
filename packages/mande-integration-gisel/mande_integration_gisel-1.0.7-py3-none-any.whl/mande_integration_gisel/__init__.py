import os
from tkinter.tix import Tree
from typing import Any, Dict, List, Tuple, Union
from dataclasses import dataclass, field
from selenium.webdriver import Chrome, Safari, Firefox, Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from mande_integration_gisel.config import LOGIN_URL, __DIR__
from mande_integration_gisel.config.selectors import BrowserSelector
from mande_integration_gisel.config.types import ExpenditureReport, ExpenditureReportDetail, Project, PaginationDirection
from datetime import datetime
import time

# __version__ = '0.1.5'

class NotFoundError(Exception):
    pass


@dataclass
class MandEIntegration:
    """
        MandE Integration Module class.
    """
    browser: Union[Safari, Edge, Firefox, Chrome]
    email: str
    password: str
    options: Union[FirefoxOptions, ChromeOptions, SafariOptions, EdgeOptions] = field(default_factory=ChromeOptions)
    
    _TIMER_SLEEP: int =  field(default=3, repr=False, init=False)
    _LOGIN_URL: str = field(default=LOGIN_URL, repr=False, init=False)
    _HOMEPAGE_URL: str = field(default=os.getenv('USADF_GRANT_URL'), repr=False, init=False)
    _REPORT_SUMMARY_TOTAL_ITEM = 'Grand Total'
    _REPORT_STATUS_DRAFT = '0 Draft'
    
    
    def setup(self) -> None:
        """
            Setup the USADF Grants application.
        """
        
        print('#️⃣  Setting up...')
        self.browser = Chrome(ChromeDriverManager().install(), options=self.options)
        self.browser.maximize_window()
        self.browser.delete_all_cookies()
        
    @property
    def categories_list(self) -> List[str]:
        return ['Infrastructure', 'Equipment Purchases', 'Working Capital / Input', 'Training', 'Technical Assistance', 'Administrative Support']
    
    @property
    def report_detail_header(self) -> List[str]:
        return ['description', 'narrative', 'lc_total', 'usd_total', 'percent_by_category', 'unexpended_balance', 'current_spend_lc', 'spend_to_date', 'exch_rate']
    
    @property
    def report_summary_header(self) -> List[str]:
        return ['category', 'lc_total', 'usd_total', 'percent_by_category', 'current_spend', 'spend_to_date_lc', 'spend_to_date_usd']
    
    def filter_div(self) ->  Union[Any, None]:
        print(self)
        loptionbar = self.browser.find_element(By.ID, 'loptionbar')
        search_wrapper = loptionbar.find_element(By.ID, 'search_container')
        search_div = search_wrapper.find_element(By.CLASS_NAME, 'search_div')
        return search_div.find_element(By.CLASS_NAME, 'searchtext_container')
        

    def clear_filters(self) -> None:
        button = self.filter_div().find_element(By.CLASS_NAME, 'showallbutton')
        self.browser.execute_script("arguments[0].click();", button)
    
    def filter_grant_by(self, search: str):
        search_input = self.filter_div().find_element(By.ID, 'searchvalue')
        search_input.clear()
        search_input.send_keys(search)
        
        search_button =self.filter_div().find_element(By.ID, 'quicksearchbutton')
        self.browser.execute_script("arguments[0].click();", search_button)        
    
    def logout(self):
        self.browser.delete_all_cookies()
        self.browser.close()
        self.browser.quit()

    def login(self) -> None:
        """
            Login to the USADF Grants application.
        """
        
        self.setup()
        self.browser.get(self._LOGIN_URL)
        _times = 0
        
        while True:
            _times += 1
            print('🔐 Logging in...')
            email_field = self.browser.find_element(By.CSS_SELECTOR, BrowserSelector.LOGIN_USERNAME)
            email_field.clear()
            email_field.send_keys(self.email)
            
            password_field = self.browser.find_element(By.CSS_SELECTOR, BrowserSelector.LOGIN_PASSWORD)
            password_field.clear()
            password_field.send_keys(self.password)
            
            button = self.browser.find_element(By.CSS_SELECTOR, BrowserSelector.LOGIN_SUBMIT_BUTTON)
            self.browser.execute_script("arguments[0].click();", button)
            
            if BrowserSelector.GRANT_MENU_BAR not in self.browser.page_source and _times != 3:
                print("Invalid Username or Password. try again...")
            elif BrowserSelector.GRANT_MENU_BAR not in self.browser.page_source and _times == 3:
                print("Invalid Username or Password. try again...")
                print("🔴 Unable to login")
                print("Quit process...")
                self.logout()
                exit(0)
            else:
                print('🟢 Logged in!')
                break


    def paginate_grant_list(self, code: str, direction: PaginationDirection = PaginationDirection.RIGHT, filter_by='niger') -> Union[List[Any], None]:
        menu_bar = self.browser.find_element(By.ID, BrowserSelector.GRANT_MENU_BAR)
        menu_bar_button = menu_bar.find_element(By.CSS_SELECTOR, BrowserSelector.GRANT_LIST_CSS_SELECTOR)
        self.browser.execute_script("arguments[0].click();", menu_bar_button)
        self.browser.switch_to.frame('app_win_1')
        
        if filter_by:
            self.filter_grant_by(filter_by)
                
        nav_div = self.browser.find_element(By.ID, 'navdiv')
        pagination = nav_div.find_element(By.CLASS_NAME, 'pagination')
        pagination_button_group = pagination.find_element(By.CLASS_NAME, 'btn-group')
        paginate_button = None
        
        if direction == PaginationDirection.RIGHT:
            paginate_button = pagination_button_group.find_element(By.XPATH, '//a[@data-action="next"]')
        elif direction == PaginationDirection.LEFT:
            paginate_button = pagination_button_group.find_element(By.XPATH, '//a[@data-action="previous"]')

        project_tr = self.search_grant(code)
        if project_tr is not None:
            return project_tr
        
        while 'disabled' not in paginate_button.get_attribute('class'):
            # paginate_button.click()
            self.browser.execute_script("arguments[0].click();", paginate_button)
            print("📖 Paginate to next.block...")
            project_tr = self.search_grant(code)
            if project_tr is not None:
                return project_tr
            
        return None
            
    def search_grant(self, code: str) -> Union[Any, None]:
        print('🔎 Searching grant...')        
        container  = self.browser.find_element(By.ID, 'container')
        container_tabs = container.find_element(By.ID, 'custabs')
        projects_tab = container_tabs.find_element(By.ID, 'custab-0')
        project_form = projects_tab.find_element(By.XPATH, '//form[@name="listviewform"]')
        project_list_container = project_form.find_element(By.ID, 'list_container')
        project_list_table = project_list_container.find_element(By.ID, BrowserSelector.GRANT_LIST_TABLE_ID)
        project_list_body = project_list_table.find_element(By.TAG_NAME, 'tbody')
        project_list_tr = project_list_body.find_elements(By.TAG_NAME, 'tr')
        
        for project_tr in project_list_tr:
            if project_tr.find_element(By.TAG_NAME, 'td').text.lower() == 'no results found':
                continue
            elif project_tr.find_elements(By.TAG_NAME, 'td')[2].text.strip() == code:
                return project_tr
            else:
                continue
        print("🔴 Grant not found!")
        return None
        
    
        
    def open_grant(self, code: str, direction: PaginationDirection = PaginationDirection.RIGHT, filter_by: str = 'niger'):
        """_summary_
        """
        parent_selection =  self.paginate_grant_list(code, direction, filter_by)
        if parent_selection is not None:
            element = WebDriverWait(self.browser, 30).until(lambda driver: driver.find_element(By.XPATH, f"//td[normalize-space()='{code}']"))
            element_parent = self.browser.execute_script("return arguments[0].parentNode", element)
            self.browser.execute_script("arguments[0].scrollIntoView();", element_parent)
            self.browser.execute_script("arguments[0].click();", element_parent)
            print('🟢 Grant found!')
            print(f'Opening grant {code}...')
        else:
            print("🔴 Grant not found!")
            self.logout()
            exit(0)
        
    def switch_to_report_frame(self) -> None:
        body = self.browser.find_element(By.TAG_NAME, 'body')
        container =body.find_element(By.ID, 'container')
        container_wrapper = container.find_element(By.ID, 'objtabs')
        sidebar = container_wrapper.find_element(By.ID, 'objtabbar_container')
        menu_bar = sidebar.find_element(By.ID, 'objtabbar')
        menu_bar_button = menu_bar.find_element(By.ID, 'sf_1039835_tb')
        self.browser.execute_script("arguments[0].click();", menu_bar_button)
        self.browser.switch_to.frame('listframe')
        
    def get_report_rows(self) -> List[Any]:
        report_table = self.browser.find_element(By.ID, 'table_1753')
        report_body = report_table.find_element(By.TAG_NAME, 'tbody')
        report_list = report_body.find_elements(By.TAG_NAME, 'tr')
        return report_list
    

    def open_first_report(self) -> None:
        self.switch_to_report_frame()
        report_list = self.get_report_rows()
        if report_list:
            report = report_list[0]
            self.browser.execute_script("arguments[0].click();", report)
        else:
            print('🔴 No report defined...!')
            self.logout()
            exit(0)
        
        

    def open_reports(self, period_start: datetime, period_end: datetime, name: str = '') -> None:
        """_summary_

        Args:
            name (str): _description_
        """
        
        print('📊 Opening reports...')
        report = None
        
        self.switch_to_report_frame()
        report_list = self.get_report_rows()
        
        print('🔎 Searching report...')
        for report_item in report_list:
            start_p, end_p = self.get_report_by_period(report_item)
            if start_p == period_start and end_p == period_end:
                print('🟢 Report found!')
                report = report_item
                break
        
        if report is None:
            print(f"😞 Oops! Report for the period of {period_start.strftime('%m/%d/%Y')} to {period_end.strftime('%m/%d/%Y')} not found!")
            print('❗ Quitting...')
            exit(1)
        
        print('🔎 Checking report status...')
        
        if self.get_report_status(report) == 1:
            print(f"🆖 Report is already approved for the period of {period_start.strftime('%m/%d/%Y')} to {period_end.strftime('%m/%d/%Y')}!")
            print('❗ Quitting...')
            exit(1)
            
        print('🆗 Report is in draft...')
        
        self.browser.execute_script("arguments[0].click();", report)
        
        print('🟢 Reports opened!')


    def open_expenditure_report(self) -> None:
        """_summary_
        """
        
        print('📊 Opening expenditure report...')
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame('app_win_1')
        
        # expenditure_report_item = 
        expenditure_report_tab = self.browser.find_element(By.ID, 'cf_1434655_tb')
        self.browser.execute_script("arguments[0].click();", expenditure_report_tab)
        # sleep(2)
        
        self.browser.window_handles[0]
        
        expenditure_report_file = self.browser.find_element(By.ID, 'xml_1434749')
        self.browser.execute_script("arguments[0].click();", expenditure_report_file)
        # sleep(self._TIMER_SLEEP)
        
        window_after = self.browser.window_handles[1]
        
        self.browser.switch_to.window(window_after)
        
        # sleep(self._TIMER_SLEEP)
        print('🟢 Expenditure report opened!')
        
    
    def format_project_data(self, project_data: Any) -> Project:
        """_summary_"""
        code = project_data[0].text
        country = project_data[1].text
        grant_type = project_data[2].text
        name = project_data[4].text
        status = project_data[10].text
        start_date = project_data[8].text
        end_date = project_data[9].text
        budget_total_amount = project_data[6].text
        
        def format_amount(amount: str) -> float:
            return float(amount.replace('$', '').replace(',', ''))
        
        def format_country(country: str) -> str:
            return "NE" if country.upper() == "NIGER" else "US"
        
        def format_date(date: str) -> str:
            return datetime.strftime(datetime.strptime(date, '%m/%d/%Y'), '%Y-%m-%d').strip() if date else ""
        
        def format_status(status: str) -> str:
            return status.upper().replace(" ", "").strip() if status else ""
        
        def format_name(name: str) -> str:
            return name.lower().strip() if name else ""
        
        def format_code(code: str) -> str:
            return f"USADF-{code.strip()}" if code else ""
        
        project = Project(format_code(code), format_name(name), format_date(start_date), format_date(end_date), format_amount(budget_total_amount), format_status(status), grant_type, format_country(country))
        
        return project
    
    # GRANT DATA
    def get_grant_data(self, code: str, filter_by='niger') -> Union[Project, None]:
        """_summary_
        """
        parent_selection = self.paginate_grant_list(code, filter_by=filter_by);
        if parent_selection is not None:
            project_info_td = parent_selection.find_elements(By.TAG_NAME, 'td')
            project_data = project_info_td[2:13]
            
            return self.format_project_data(project_data)
        return None
        

    def get_report_row_data(self, report_row: Any) -> List[Any]:
        return report_row.find_elements(By.TAG_NAME, 'td')
    
    def get_report_status(self, report_row: Any) -> int:
        report_data = self.get_report_row_data(report_row)
        status = report_data[6].text
        
        if status.lower() in self._REPORT_STATUS_DRAFT.lower():
            return 0
        return 1
        

    def get_report_by_period(self, report_row: Any) -> Tuple[datetime, datetime]:
        report_data = self.get_report_row_data(report_row)
        report_period_start = datetime.strptime(report_data[3].text, '%m/%d/%Y')
        report_period_end = datetime.strptime(report_data[4].text, '%m/%d/%Y')
        
        return report_period_start, report_period_end


    # Report Summary Section
    def get_summary_report_container(self) -> Any:
        report_summary = self.browser.find_element(By.ID, 'headingDiv')
        return report_summary.find_element(By.CLASS_NAME, 'summaryDetails')
    
    
    def get_summary_report_table(self) -> Any:
        return self.get_summary_report_container().find_element(By.TAG_NAME, 'table')
    
    
    def get_summary_report_body(self) -> Any:
        return self.get_summary_report_table().find_element(By.TAG_NAME, 'tbody')

                
    def get_summary_report_row(self, row_index_start: int, row_index_stop: int = 0) -> Any:
        """_summary_
        """
        if row_index_stop == 0:
            return self.get_summary_report_body().find_elements(By.TAG_NAME, 'tr')[row_index_start:]
        return self.get_summary_report_body().find_elements(By.TAG_NAME, 'tr')[row_index_start:row_index_stop]

    # Report Detail Section
    
    def get_detail_report_body(self, content_wrapper: Any) -> Any:
        return content_wrapper.find_element(By.TAG_NAME, 'tbody')
    
    def get_detail_report_footer(self, content_wrapper: Any) -> Any:
        return content_wrapper.find_element(By.TAG_NAME, 'tfoot')
    
    def get_detail_report_body_row(self, content_wrapper: Any) -> Any:
        return self.get_detail_report_body(content_wrapper).find_elements(By.TAG_NAME, 'tr')
    
    def get_detail_report_footer_row(self, content_wrapper: Any) -> Any:
        return self.get_detail_report_footer(content_wrapper).find_elements(By.TAG_NAME, 'tr')[0]
    
    def add_report_body_content_name(self, row_data: Any) -> Any:
        return row_data[0].find_element(By.TAG_NAME, 'textarea').get_attribute('value').strip().lower()
    
    def add_report_body_content(self, row_data: Any) -> ExpenditureReportDetail:
        """_summary_
        """
        report = ExpenditureReportDetail(
                description=row_data[0].find_element(By.TAG_NAME, 'textarea').get_attribute('value'),
                narrative=row_data[1].find_element(By.TAG_NAME, 'textarea').get_attribute('value'),
                lc_total=row_data[2].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                usd_total=row_data[3].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                percent_by_category=row_data[4].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                unexpended_balance=row_data[5].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                current_spend_lc=row_data[6].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                spend_to_date=row_data[7].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                exch_rate=row_data[8].find_element(By.TAG_NAME, 'input').get_attribute('value'),
        )
        
        return report
    
    def add_report_footer_content(self, row_data) -> ExpenditureReportDetail:
        report_total = ExpenditureReportDetail(
            description=row_data[0].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            narrative=row_data[1].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            lc_total=row_data[2].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            usd_total=row_data[3].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            percent_by_category=row_data[4].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            unexpended_balance=row_data[5].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            current_spend_lc=row_data[6].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            spend_to_date=row_data[7].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            exch_rate=row_data[8].find_element(By.TAG_NAME, 'input').get_attribute('value'),
        )
        
        return report_total
    
    def add_report_summary_content(self, row_data) -> ExpenditureReport:
        report = ExpenditureReport(
                category=row_data[0].text,
                lc_total=row_data[1].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                usd_total=row_data[2].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                percent_by_category=row_data[3].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                current_spend=row_data[4].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                spend_to_date_lc=row_data[5].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                spend_to_date_usd=row_data[6].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            )
        
        return report
        
    
    def retrieve_expenditure_report_content(self, code: str) -> List[ExpenditureReport]:
        """_summary_
        """
        print('🗃️  Retrieving expenditure report content...')
        reports: List[ExpenditureReport] = []
        report_row = self.get_summary_report_row(1)
        
        for row in report_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            report = self.add_report_summary_content(row_data)
            reports.append(report)
        
        print('🟢 Expenditure report content retrieved!')
        return reports

    
    def retrieve_expenditure_report_detail(self, code: str, category: str) -> List[ExpenditureReportDetail]:
        """_summary_
        """
        reports: List[ExpenditureReportDetail] = []     
        category_content, _ = self.get_category_content(category)
            
        if category_content is None:
            raise NotFoundError('Category not found')
        
        category_content_body_row = self.get_detail_report_body_row(category_content)
        category_content_footer_row = self.get_detail_report_footer_row(category_content)
        
        for row in category_content_body_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            report = self.add_report_body_content(row_data)
            reports.append(report)
            
        row_data_total = category_content_footer_row.find_elements(By.TAG_NAME, 'td')
        report_total = self.add_report_footer_content(row_data_total)
        reports.append(report_total)

        return reports
    
    def retrieve_expenditure_report_data(self, code: str, category: str) -> Dict[str, List[str]]:
        """_summary_

        Args:
            code (str): grant code
            category (str): category name

        Returns:
            List[Any]: List of expenditure report data
        """
        expenditure_report = dict()
        category_content, category_name = self.get_category_content(category)
        
        if category_content is None:
            raise NotFoundError('Category not found')

        expenditure_report[category_name] = []
        category_content_body_row = self.get_detail_report_body_row(category_content)
        
        for row in category_content_body_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            report_name = self.add_report_body_content_name(row_data)
            report_row_data = self.add_report_body_content(row_data)
            # dct = {i: i.value for i in report_row_data}
            # print(dct)
            expenditure_report[category_name].append({report_name: report_row_data})

        print("🟢 Expenditure report data retrieved!")
        print(expenditure_report)

        return expenditure_report

    
    
    # Edit summary report for all category
    def edit_summary_report(self, category: str, category_value: str, exch_rate: str) -> None:
        print(f"📩 Defined summary report for <{category}> category")
        total_value_usd = 0
        report_row = self.get_summary_report_row(1, -2)
                
        for row in report_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            category_text = row_data[0].text
            
            if  category.lower() in category_text.lower() and self._REPORT_SUMMARY_TOTAL_ITEM not in category_text.lower():
                category_report_summary_spend_to_date_lc = row_data[5].find_element(By.TAG_NAME, 'input')
                category_report_summary_spend_to_date_lc.clear()
                category_report_summary_spend_to_date_lc.send_keys(category_value.format('{:.2f}'))
                
                total_value_usd = float(category_value) / float(exch_rate.replace(',', ''))
                category_report_summary_spend_to_date_usd = row_data[6].find_element(By.TAG_NAME, 'input')
                category_report_summary_spend_to_date_usd.clear()
                category_report_summary_spend_to_date_usd.send_keys(str(total_value_usd).format('{:.2f}'))
                break
        
        print(f"🟢 Summary report for <{category}> category edited")
        
    
    # Set category details values
    def set_category_value(self, category_content: Any, values: List[Dict[str, str]]) -> Tuple[str, str]:
        total_lc, rate = 0, 1
        category_content_body = category_content.find_element(By.TAG_NAME, 'tbody')
        category_content_body_tr = category_content_body.find_elements(By.TAG_NAME, 'tr')
        
        for row in category_content_body_tr:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            category_text = row_data[0].find_element(By.TAG_NAME, 'textarea').get_attribute('value')
            rate = row_data[8].find_element(By.TAG_NAME, 'input').get_attribute('value')
        
            for value in values:
                if value['description'].lower() in category_text.lower():
                    row_data[6].find_element(By.TAG_NAME, 'input').clear()
                    row_data[6].find_element(By.TAG_NAME, 'input').send_keys(value['current_spend_lc'])
                    
                    row_data[7].find_element(By.TAG_NAME, 'input').clear()
                    row_data[7].find_element(By.TAG_NAME, 'input').send_keys(value['spend_to_date'])
                    
                    total_lc += float(value['spend_to_date'].replace(',', ''))
        
        return str(total_lc), rate
    
    
    def get_category_header_list(self) -> List[str]:
        categories = self.browser.find_elements(By.CLASS_NAME, 'headerTable')
        category_list = []
        for cat in categories:
            category_name = cat.find_element(By.TAG_NAME, 'h3').text.lower().strip()
            category_format = " ".join(category_name.split(' ')[1:]).replace(":", "")
            category_list.append(category_format)
            
        return category_list
        
    
    # Get category content
    def get_category_content(self, category: str) -> Tuple[Union[Any, None], Union[str, None]]:
        categories = self.browser.find_elements(By.CLASS_NAME, 'headerTable')
        category_content = None
        category_name = None

        for cat in categories:
            category_name = cat.find_element(By.TAG_NAME, 'h3').text
            if category.lower() in category_name.lower():
                category_content = self.browser.execute_script("""return arguments[0].nextElementSibling""", cat)
                break
        
        category_name_format = " ".join(str(category_name).split(' ')[1:]).replace(":", '').lower() if category_name is not None else None
        return category_content, category_name_format


    # Set summary report total value
    def set_summary_report_total_value(self):
        """_summary_
        """
        
        total_spend_to_date_lc = 0
        total_spend_to_date_usd = 0
        
        report_row = self.get_summary_report_row(1)
        for row in report_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            
            if self._REPORT_SUMMARY_TOTAL_ITEM not in row_data[0].text:
                total_spend_to_date_lc += float(row_data[5].find_element(By.TAG_NAME, 'input').get_attribute('value').replace(',', ''))
                total_spend_to_date_usd += float(row_data[6].find_element(By.TAG_NAME, 'input').get_attribute('value').replace('$', '').replace(',', ''))
            
        total_row = report_row[-1].find_elements(By.TAG_NAME, 'td')[1:]
        total_row_lc = total_row[5].find_element(By.TAG_NAME, 'input')
        total_row_usd= total_row[6].find_element(By.TAG_NAME, 'input')
        
        total_row_lc.clear()
        total_row_lc.send_keys(str(total_spend_to_date_lc))
        
        total_row_usd.clear()
        total_row_usd.send_keys(str(total_spend_to_date_usd))
            
            
                


    # Edit grant report values
    def edit_report(self, category_list: List[str], values: List[Dict[str, Any]]) -> None:
        """_summary_
        """
        for category in category_list:
            category_content, _ = self.get_category_content(category)
            
            if category_content is None:
                raise NotFoundError('Category not found')
            
            for value in values:
                if value['name'].lower() == category.lower():
                    
                    _, rate = self.set_category_value(category_content, value['details'])
                    
                    self.edit_summary_report(category, str(value['spend_to_date']), rate)
            
        self.set_summary_report_total_value()
        self.save_change()
        print("🎉 Report edited 🎉")
    

        
    # Save all changes
    def save_change(self) -> None:
        footer_actions = self.browser.find_element(By.ID, 'v-footer')
        cmd_save = footer_actions.find_element(By.ID, 'cmd_save')
        self.browser.execute_script("arguments[0].click();", cmd_save)
        
    #Return current url
    def current_url(self):
        return self.browser.current_url

