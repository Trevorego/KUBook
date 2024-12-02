# Metin Ege Özdemir / Trevorego
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import psutil
import json
import threading
import sys

def terminate_process_by_name(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            pid = process.info['pid']
            try:
                p = psutil.Process(pid)
                p.terminate()  # Try terminating gracefully
                p.wait(3)  # Wait for the process to terminate (3 seconds)
            except psutil.NoSuchProcess:
                pass  # Process already terminated or doesn't exist
            except psutil.AccessDenied:
                print(f"Access Denied: Cannot terminate {process_name}")
                
def is_browser_open(driver):
    try:
        driver.title
        return True
    except:
        return False
                
def monitor_browser(driver):
    """
    Monitors if the browser is still open. If closed, exits the program.
    """
    try:
        while True:
            if not is_browser_open(driver):
                print("Browser closed. Exiting script.")
                driver.quit()
                terminate_process_by_name('KUBook.exe')
                sys.exit()
            time.sleep(1) 
    except Exception as e:
        print(f"Error in monitor thread: {e}")
        driver.quit()
        sys.exit()

def get_config():
    with open("config.json", "r") as file:
        config = json.load(file)
        
        return (config.get("date", {}).get("day"), config.get("date", {}).get("month"), config.get("date", {}).get("year")), config.get("room"), config.get("time")

def setup():
    terminate_process_by_name('chrome.exe')
    
    #create chromeoptions instance
    options = webdriver.ChromeOptions()     

    #provide location where chrome stores profiles
    user_data_dir = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    #provide the profile name with which we want to open browser
    options.add_argument(r"--profile-directory=Default")

    #specify where your chrome driver present in your pc
    driver = webdriver.Chrome(options=options)

    #provide website url here
    driver.get("https://ku.libcal.com/reserve/teamstudy")
    
    return driver

def check_available(driver, desired_date):
    time.sleep(0.3)
    while True:
        try:
            print(driver.find_element(By.XPATH, "//div[@id='s-lc-window-limit-warning']").get_attribute("style"))
            if driver.find_element(By.XPATH, "//div[@id='s-lc-window-limit-warning']").get_attribute("style") == "display: none;":
                print(driver.find_element(By.XPATH, "//div[@id='s-lc-window-limit-warning']").get_attribute("style"))
                break
            else:
                driver.get("https://ku.libcal.com/reserve/teamstudy")
                get_to_date(driver, desired_date=desired_date)
                time.sleep(0.3)
        except Exception:
            continue

def get_to_date(driver, desired_date):
    next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
    next_button.click()
 
    site_date = [int(x) if int(x) < 2000 else int(x[2:4]) for x in driver.find_element(By.XPATH, "//h2[@class='fc-toolbar-title']").text.split("/")]
    
    while site_date[0] != desired_date[0] or site_date[1] != desired_date[1] or site_date[2] != desired_date[2]:
        next_button.click()
        for e in site_date:
            print(e)
        for e in desired_date:
            print(e)
        site_date = [int(x) if int(x) < 2000 else int(x[2:4]) for x in driver.find_element(By.XPATH, "//h2[@class='fc-toolbar-title']").text.split("/")]

def select_slots(driver, room, desired_date, starting_time):
    print("2")
    while True:
        try:
            a_element = driver.find_element(By.XPATH, f"//a[@title='{str(starting_time).zfill(2)}:00 {str(desired_date[0])}/{str(desired_date[1]).zfill(2)}/20{desired_date[2]} - {room} - Available']")
            print(a_element.text)
            select_button = a_element.find_element(By.XPATH, "./div")
            driver.execute_script("arguments[0].scrollIntoView(true);", select_button)
            select_button.click()
            time.sleep(0.3)
            break
        except Exception:
            continue
    while True:
        try:
            a_element = driver.find_element(By.XPATH, f"//a[@title='{str(starting_time + 1).zfill(2)}:00 {str(desired_date[0])}/{str(desired_date[1]).zfill(2)}/20{desired_date[2]} - {room} - Available']")
            select_button = a_element.find_element(By.XPATH, "./div")
            driver.execute_script("arguments[0].scrollIntoView(true);", select_button)
            select_button.click()
            time.sleep(0.3)
            break
        except Exception:
            continue
        
def confirmation(driver):
    while True:
        try:
            submit_button = driver.find_element(By.XPATH, "//button[text()='Submit Times']")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            submit_button.click()
            break
        except Exception:
            continue
    while True:
        try:
            submit_button = driver.find_element(By.XPATH, "//button[text()='Continue']")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            submit_button.click()
            break
        except Exception:
            continue
    while True:
        try:
            submit_button = driver.find_element(By.XPATH, "//button[@id='btn-form-submit']")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            submit_button.click()
            break
        except Exception:
            continue
    time.sleep(1000)

def book(driver, desired_date, room, starting_time):
    get_to_date(driver, desired_date)
    
    check_available(driver, desired_date=desired_date)
    
    select_slots(driver, room=room, desired_date=desired_date, starting_time=starting_time)
    
    confirmation(driver)

def main():
    desired_date, room, starting_time = get_config()
    
    driver = setup()
    
    monitor_thread = threading.Thread(target=monitor_browser, args=(driver,))
    monitor_thread.daemon = True  # Ensures the thread closes if the main program exits
    monitor_thread.start()
    
    book(driver, desired_date=desired_date, room=room, starting_time=starting_time)

if __name__ == "__main__":
    main()