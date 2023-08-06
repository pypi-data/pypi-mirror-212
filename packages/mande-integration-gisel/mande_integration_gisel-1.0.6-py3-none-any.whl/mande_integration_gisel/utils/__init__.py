import csv
import os
from bs4 import BeautifulSoup
from typing import List
from mande_integration_gisel.config import __DIR__
from mande_integration_gisel.config.types import ExpenditureReport

def generate_report(code: str):
    report_file = __DIR__ / 'reports' / f"{code}_expenditure_report.html"
    with open(report_file, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    summary = soup.find_all('p')
    data_wrapper = soup.find('table')
    data_container = data_wrapper.find('tbody')
    data_row = data_container.find_all('tr')
    rows = [item.get_text() for item in data_row[1:]]
    data_headers =  [item.get_text() for item in data_row[0]][1:]
    data_content = data_row[1:]

    result = {'summary': [item.get_text() for item in summary]}
    for key, value in enumerate(data_content):
        element = value.find_all('td')[1:]
        result[rows[key]] = {}

        for el in element:

            if el.attrs.get('class') is not None and el.attrs.get('class')[0] == ['row-hdr'][0]:
                result[rows[key]][data_headers[element.index(el)]] = el.get_text()

            elif el.attrs.get('class') is not None and el.attrs.get('class')[0] == ['subTotal'][0]:
                result[rows[key]][data_headers[element.index(el)]] = el.find('input').value

            else:
                result[rows[key]][data_headers[element.index(el)]] = ""


    return result
    

def to_csv(code: str, header: List[str], data: List[ExpenditureReport], file: str) -> None:
    """_summary_

    Args:
        code (str): Grant code
        header (List[str]): Table header
        data (List[ExpenditureReport]): list of ExpenditureReport
    """
    
    report_dir = __DIR__ / 'reports' / f"{code}"
    
    if not report_dir.exists():
        os.makedirs(report_dir)

    filename = report_dir / f"{file}.csv"
    
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)

        for report in data:
            csv_writer.writerow(report.to_list())