# Like WebDriverWait - visibility_of_element_located, but much easier

## pip install selenium2df-locate-element


#### Tested against Windows 10 / Python 3.10 / Anaconda 3

This module simplifies the process of locating and extracting elements from web pages using Selenium, 
while leveraging the power and flexibility of Pandas DataFrames. 
It saves time and effort by providing a streamlined approach to web data
 extraction and facilitates further data processing and analysis tasks.

### Advantages of using the locate_element function

#### Simplified element location: 

The function abstracts away the complexities of locating elements using CSS selectors in Selenium. You can specify a CSS selector query to target the desired elements without dealing with low-level Selenium operations.


#### Conversion to Pandas DataFrame: 

The located elements are converted into a Pandas DataFrame, providing a convenient data structure for data manipulation and analysis. 
This allows you to leverage Pandas' extensive functionality for working with tabular data.

#### Support for conditional modification: 

The function accepts a checkdf parameter, which allows you to provide a callable function for modifying the DataFrame 
based on specific conditions. This can be useful when you want 
to filter or transform the located elements based on custom criteria.

#### Timeout handling: 

The function includes a timeout mechanism to wait for the desired
 elements to appear on the page. You can specify the maximum time to 
 wait, and the function will 
 continue to retry until the timeout is reached or the elements are located. 
 This helps handle scenarios where elements may take some 
 time to load or appear dynamically on the page.



```python
    Locates elements on a web page using Selenium and converts them into a Pandas DataFrame.

    Args:
        checkdf: A callable function that takes a Pandas DataFrame as input and returns a modified DataFrame based on certain conditions. Defaults to None.
        query: A string representing the CSS selector query for the desired elements. Defaults to "*".
        timeout: The maximum time in seconds to wait for the desired elements. Defaults to 30.
        withmethods: A boolean indicating whether to include methods for interacting with the elements in the resulting DataFrame. Defaults to True.

    Returns:
        If checkdf is None, returns a single Pandas DataFrame containing the located elements.
        If checkdf is provided, returns a tuple of two Pandas DataFrames: the first one contains all located elements, and the second one contains the modified DataFrame returned by checkdf.

import undetected_chromedriver as uc
from selenium2df_locate_element import selenium2dfwait, locate_element

if __name__ == "__main__":
	driver = uc.Chrome()
	selenium2dfwait.driver = driver
	driver.get(r"https://testpages.herokuapp.com/styled/index.html")
	df3 = locate_element()
	df_all, df = locate_element(checkdf=lambda df:df.loc[df.aa_localName == 'a'], query='*', timeout=30, withmethods=True)
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
```	