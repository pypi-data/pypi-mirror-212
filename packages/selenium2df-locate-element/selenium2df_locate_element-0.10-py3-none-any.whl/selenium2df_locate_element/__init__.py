import time
import sys

import pandas as pd
from a_selenium2df import get_df  # pip install a-selenium2df
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from typing import Callable

selenium2dfwait = sys.modules[__name__]
selenium2dfwait.driver = None


def locate_element(
    checkdf: None | Callable = None,
    query: str = "*",
    timeout: int | float = 30,
    withmethods: bool = True,
) -> pd.DataFrame | tuple[pd.DataFrame | pd.DataFrame]:
    r"""
    Locates elements on a web page using Selenium and converts them into a Pandas DataFrame.

    Args:
        checkdf: A callable function that takes a Pandas DataFrame as input and returns a modified DataFrame based on certain conditions. Defaults to None.
        query: A string representing the CSS selector query for the desired elements. Defaults to "*".
        timeout: The maximum time in seconds to wait for the desired elements. Defaults to 30.
        withmethods: A boolean indicating whether to include methods for interacting with the elements in the resulting DataFrame. Defaults to True.

    Returns:
        If checkdf is None, returns a single Pandas DataFrame containing the located elements.
        If checkdf is provided, returns a tuple of two Pandas DataFrames: the first one contains all located elements, and the second one contains the modified DataFrame returned by checkdf.

    Example usage:
        import undetected_chromedriver as uc
        from selenium2df_locate_element import selenium2dfwait, locate_element

        if __name__ == "__main__":
            driver = uc.Chrome()
            selenium2dfwait.driver = driver
            driver.get(r"https://testpages.herokuapp.com/styled/index.html")
            df3 = locate_element()
            df_all, df = locate_element(checkdf=lambda df: df.loc[df.aa_localName == 'a'], query='*', timeout=30, withmethods=True)
            print(df_all, df)

            print(df3)
                                                   element  ...                    aa_window_switch
    0    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    1    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    2    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    3    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    4    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    ..                                                 ...  ...                                 ...
    181  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    182  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    183  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    184  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    185  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    [186 rows x 136 columns]
    print(df)
                                                   element  ...                    aa_window_switch
    15   <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    17   <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    19   <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    23   <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    25   <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    ..                                                 ...  ...                                 ...
    171  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    173  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    179  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    180  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    185  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    [66 rows x 136 columns]
    print(df_all)
                                                   element  ...                    aa_window_switch
    0    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    1    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    2    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    3    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    4    <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    ..                                                 ...  ...                                 ...
    181  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    182  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    183  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    184  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    185  <undetected_chromedriver.webelement.WebElement...  ...  0A3ADC1FAEED9B036EB136728D29F595()
    [186 rows x 136 columns]

    """

    def _g():
        return get_df(
            selenium2dfwait.driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector=query,
            with_methods=withmethods,
        )

    dataframe = _g()
    if not checkdf:
        return dataframe
    timeoutfinal = time.time() + timeout
    co = 1
    while timeoutfinal > time.time() and checkdf(dataframe).empty:
        try:
            print(
                f"Getting dataframe: {co} - {int(timeoutfinal-time.time())} sec.",
                end="\r",
            )
            dataframe = _g()
            co = co + 1
        except Exception as fe:
            print(fe)
            continue
    return dataframe, checkdf(dataframe)
