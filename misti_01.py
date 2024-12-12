from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Automatically downloads the correct chromedriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time
import re
import os
import glob

download_path = "C:/Users/PC/Downloads"
# Set up WebDriver with Service
service = Service(ChromeDriverManager().install())  # This line automatically installs the chromedriver
driver = webdriver.Chrome(service=service)  # Use the new WebDriver initialization with the service

def login(username, password):
    
    driver.get("https://mistiendas.ddysdigital.com/listaCompras")
    
    username_field = driver.find_element(By.ID, "usuario" )
    password_field = driver.find_element(By.ID, "password")
    
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)  

def open_new_tab(url):
    # Open a new tab
    driver.execute_script("window.open('');")
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(3) 

def increment_month(date_str):
    # Convert the string to a datetime object
    #date_obj = datetime.strptime(date_str, "%m-%d-%Y") #for ender
    date_obj = datetime.strptime(date_str, "%d-%m-%Y") #for misti

    # Calculate the new month
    new_month = date_obj.month + 1
    new_year = date_obj.year

    if new_month > 12:
        new_month = 1
        new_year += 1

    # Create a new date string with the incremented month
    new_date_obj = date_obj.replace(year=new_year, month=new_month, day=1)

    #initial_date = new_date_obj.strftime("%m-%d-%Y") #for ender
    initial_date = new_date_obj.strftime("%d-%m-%Y") #for misti

    print(new_date_obj)
    return initial_date
    # Return the new date in 'DD-MM-YYYY' format
    #return new_date_obj.strftime("%d-%m-%Y")

def set_date(date):
    # Locate the date input field
    date_field = driver.find_element(By.NAME, "fecha_inicio")
    
    date_field.clear()
    date_field.send_keys(date)
    date_field.send_keys(Keys.RETURN)
    time.sleep(1)

def search_barcode(barcode):
    
    initial_date = "01-01-2024"

    try:
        # Locate the search input field (assuming there's a field for barcode input)
        search_field = driver.find_element(By.CSS_SELECTOR, "input.rbt-input-main.form-control.rbt-input.form-control-sm")  # Adjust the element selector as needed
    
        search_field.clear()
        search_field.send_keys(barcode)
        search_field.send_keys(Keys.ARROW_DOWN)
        search_field.send_keys(Keys.RETURN)
        '''
        target_selector = "div.sc-fPXMVe.idQiur.rdt_TableHeader"
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, target_selector)))
        target_element = driver.find_element(By.CSS_SELECTOR, target_selector)
        '''
    except Exception as e:
        print(f"An error occurred during search: {e}")

def refresh_page():
    # Locate and click the refresh button (adjust the selector)
    refresh_button = driver.find_element( By.XPATH, "//button[contains(@class, 'btn-danger') and contains(text(), 'Recargar')]")  # Replace with the actual refresh button ID
    refresh_button.click()
    
    time.sleep(6)  # Wait for the page to refresh
    print("REFRESHED")

def download_pdf(product_name):
    
    download_button = driver.find_element(By.XPATH, "//button[text()='Descargar']")
    download_button.click()
    time.sleep(5) 

    #check file 
    downloaded_file = wait_for_download_to_complete()
    if downloaded_file:
        print(f"File downloaded: {downloaded_file}")

        # Rename the downloaded file to the barcode as filename
        new_filename = os.path.join(download_path, f"{barcode}.xlsx")
        os.rename(downloaded_file, new_filename)
        print(f"File renamed to: {new_filename}")

'''
        while not is_file_fully_downloaded(downloaded_file):
            print("Waiting for file to fully download...")
            time.sleep(1)
'''

def wait_for_download_to_complete():
    """Wait until the file is fully downloaded (no partial .crdownload file)."""
    while True:
        downloaded_files = glob.glob(f"{download_path}/*.xlsx")
        if downloaded_files:
            # Get the most recent file
            downloaded_file = downloaded_files[-1]
            if not downloaded_file.endswith(".crdownload"):
                return downloaded_file
        time.sleep(1)  # Wait a second before checking again

if __name__ == "__main__":
    '''
    The programs starts getting the username and the password to call the "login" function, then a new url is created to open a new tab with a especific url so we avoid navigating through multiple sections of the webpage.
    Then a barcode is set with an initial date
    Now we call all the functions in order... starting with set_date(date) to put the initial date, then we refresh the page to search the product with the new date parameter, we enter in a loop where the date actualize until find the product.
    '''
    username = "administrador"  
    password = "administrador1"

    barcode = "7506195195468"
    date = "01-01-2024"
    new_url = "https://mistiendas.ddysdigital.com/kardexFisico" 
    
    login(username, password)
    open_new_tab(new_url)
    set_date(date)
    refresh_page()           

    barcode_file = "D:/ARTICULOS.xlsx"
    df = pd.read_excel(barcode_file)
    barcodes = df['nombre_marca'].tolist()
    product_name = df['nombre'].tolist()

    for barcode, product_name in zip(barcodes, product_name):
        
        if pd.isna(barcode):
            print("Skipping black barcode cell.")
            continue       
        
    
        try:
            print(f"Processing barcode: {barcode}")
            search_barcode(barcode)
            download_pdf(product_name)
            time.sleep(3)
        except Exception as e:
            print(f"Error processing barcode {barcode}: {e}")           
    
    driver.quit()
