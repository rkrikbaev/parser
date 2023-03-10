from time import sleep
from random import uniform
import argparse
import csv


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


"""Sets chrome options for Selenium.
Chrome options for headless browser is enabled.
"""

chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')    
chrome_prefs = {}
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_options.experimental_options["prefs"] = chrome_prefs


def login(url, password, login)->None:
    
    driver.get(url)
    ###
    # test on github.com
    #login = driver.find_element(By.ID, "login_field")
    #password = driver.find_element(By.ID, "password")

    #password.send_keys("Zeinet8sse")
    #login.send_keys("rkrikbaev")

    #driver.find_element(By.NAME, "commit").click()
    ###
    
    password = driver.find_element(By.ID, "gwt-debug-userPasswordTextBox")
    login = driver.find_element(By.ID, "gwt-debug-userNameTextBox")
    
    password.send_keys("admin")
    login.send_keys("administrator")

    driver.find_element(By.ID, "gwt-debug-signInButton").click()
    
    return True

def get_data(item):
    
    def convert_to_int(element):

        if isinstance(element, str):
        
            try:
                element = float(element)
            except ValueError:
                element = element.strip()
            
            return element

    def convert_to_dict(a):

        it = iter(a)
        res_dct = dict(zip(it, it))
        
        return res_dct
    
    try:

        text = driver.find_element(By.ID, str(item)).text

        list_of = text.split('\n')

        list_of_values = [convert_to_int(x) for x in list_of if x!='' and x.strip() != 'View']
        
        label = list_of_values.pop(0)

        values = convert_to_dict(list_of_values)
        
        print(label)
        print(values)
        
        return label, values
    except Exception as exc:
        print(exc)

if __name__ == "__main__":

    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='localhost', help='Host (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=11502, help='TCP port (default: 11502)')
    args = parser.parse_args()

    url_login = "https://192.168.1.251"
    url_data = "https://192.168.1.251/#TankOverView"

    list_of_objects = ["gwt-debug-tankItem1", "gwt-debug-tankItem2"]

    # uncomment to test    
    # url_data = "http://127.0.0.1:5500/samples/Veeder-Root%20Web%20Interface/Veeder-Root%20Web%20Interface.html"

    driver = webdriver.Chrome(options=chrome_options)
    
    login_passed = login(url_login, password='administrator', login='admin')
    # login_passed=1
    if login_passed:

        driver.get(url=url_data)

        sleep(10)
        try:
            print("Start grabering...")

            while True:

                for index, item in enumerate(list_of_objects): 

                    _, d = get_data(item)

                    order = ['Fuel Volume','Fuel Height','100% Ullage','Density','Temperature']
                    
                    word_list = [ d[value]*10 for value in order ]
                    
                    data_list = [int(w) & 0xffff for w in word_list]
                    print(data_list)

                    with open(f'data_{index+1}.csv', 'w') as file:
                        csv_writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(data_list)

                    sleep(10)

        except Exception as exc:
            print(exc)
            print("Shutdown graber ...")
            sleep(2)
            print("Graber is offline")  

    else:
        print('login failed')

    driver.close()
