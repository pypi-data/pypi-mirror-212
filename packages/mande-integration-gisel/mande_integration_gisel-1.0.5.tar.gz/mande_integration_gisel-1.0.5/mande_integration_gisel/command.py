from ctypes import Union
import enum
from dataclasses import dataclass, field
from lib2to3.pgen2 import driver
from selenium.webdriver import Safari, Firefox, Chrome, Edge
from typing import Callable, Union, Any



class WebDriverEnum(enum.Enum):
  safari = Safari
  firefox = Firefox
  chrome = Chrome
  edge = Edge


@dataclass
class Command:
  """
    Commande class
  """
  driver: Union[Safari, Firefox, Chrome, Edge] = field(default=WebDriverEnum.safari, repr=False)  
  
  def run(self, selector: str):
      """_summary_

      Args:
          selector (str): Element to select
      """
      element = self.driver.find_element_by_css_selector(selector)
      element.click()
      