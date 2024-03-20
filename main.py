# --------------------------------- Import -------------------------------------
import time, yaml, pandas as pd, random
from selenium import webdriver as uc
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options


# --------------------------------- Initializing Variables -------------------------------------
final_text = ""
driver = ""
df = ""
line_break = "=" * 60

def get_data_from_csv():
    global df
    df = pd.read_csv("person.csv")
    print(df.head())


# --------------------------------- Initialize if not VPN -------------------------------------
def init():
    print("Start of INIT Fucntion...")
    print(line_break)
    global driver
    driver = uc.Chrome()
    driver.maximize_window()
    print("End of INIT Fucntion...")
    print(line_break)

# --------------------------------- Starts from Here -------------------------------------
def start():
    global df
    for index, person in df.iterrows():
    # Process one row at a time
        print(f"Processin {index+1}th Record")
        print(person)
        open_page()
        login(person)
        page_1(person)
        page_2()
        consent_form()
        consent_popup()
        digital_sign(person)
        message = post_popup()
        # Write to new Column
        df.loc[index, 'result_message'] = message
    # Save the csv at the FINALLY BLOCK

# --------------------------------- Open WebPage -------------------------------------
def open_page():
    print("Start of OPEN_PAGE Fucntion...")
    print("="*70)

    driver.execute_script("window.open('about:blank', '_blank');")
    
    driver.switch_to.window(driver.window_handles[-1])
    
    search_url = f"https://maxsip.legendari.tech/enroll/mhaider1/start"
    driver.get(search_url)
    print("Opened WebPage in new tab...")
    
    # Close all other tabs except the new one
    for handle in driver.window_handles[:-1]:
        driver.switch_to.window(handle)
        driver.close()
    
    # Switch back to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    print("="*70)

# --------------------------------- Login -------------------------------------
def login(person):
    print("Start of LOGIN Fucntion...")
    print("="*70)
    try:
        zip_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.ID, "mat-input-0")))
        email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.ID, "mat-input-1")))
        
        zip_code = person["zip"]
        zip_field.send_keys("")
        zip_field.send_keys(zip_code)
        email_addrs = person["email"]
        email_field.send_keys("")
        email_field.send_keys(email_addrs)
        time.sleep(5)
        submit_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/base-info/div/div[2]/mat-card/mat-card-content/div[2]/button")))
        submit_btn.click()
    except TimeoutException:
        print("Fields not there... Trying again.")
        login(person)
    
    # Check if next page appeared
    try:
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.ID, "mat-input-0"))).send_keys("test")
        print("Calling Login Again, still on start page.")
        email_field.clear()
        login(person)
    except:
        pass
    print("End of LOGIN Fucntion...")
    print("="*70)

# --------------------------------- Page 1 All Details -------------------------------------
def page_1(person):
    print("Start of PAGE # 1 Fucntion...")
    print("="*70)
    try:
        first_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-2")))
        last_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-4")))
        ssn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-10")))

        personal_contact_number = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-6")))
        
        address_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-11")))
        
        submit_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[4]/button")))
        first = person["first"]
        first_name.send_keys("")
        first_name.send_keys(first)
        print("First Name entered...")

        last = person["last"]
        last_name.send_keys("")
        last_name.send_keys(last)
        print("Last Name entered...")

        ssn_num = person["ssn"]
        ssn.send_keys("")
        ssn.send_keys(ssn_num)
        print("SSN entered...")

        phone = person["phone"]
        personal_contact_number.send_keys("")
        personal_contact_number.send_keys(phone)
        print("Entered Phone #.")

        address = person["address"]
        address_element.send_keys("")
        address_element.send_keys(address)
        time.sleep(1)
        print("Entered Address.")
        time.sleep(1)

        print("Waiting for date.")
        time.sleep(15)
        submit_btn.click()
        print("clicked submit")
        time.sleep(3)
        
        try:
            print("Checking if adrs bar is there.")
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "mat-input-11")))
            valid = validate_address()
            if not valid:
                submit_btn.click()
                print("Submitted...")
        except TimeoutError:
            # print("Submitted...")
            print("Address perfectly validated.")
            valid = False
        print("almost starting While Loop.")
        while valid:
            print("Inside the While Loop")
            try:
                time.sleep(5)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "mat-input-11")))
                print("Address not Validated... Clicking DON'T VALIDATE...")
                valid = validate_address()
            except:
                print("Submitted...")
                print("Address perfectly validated.")
                valid = False
    except TimeoutException:
        print("Objects not found, trying again...")
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-program/div/div[2]/div[2]/button[1]/span[1]")))
            print("We are on Page 2...")
            return 0
        except:
            pass
        page_1(person)
    
    # Check if next page is appeared
    try:
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-2"))).click()
        print("Still on Page 1... Calling Page#1 Again...")
        page_1(person)
    except:
        pass
    print("End of PAGE_1 Fucntion...")
    print("="*70)

# --------------------------------- Remove Adress Validation -------------------------------------
def validate_address():
        print("START of VALIDATE_ADDRESS Fucntion...")
        print("="*70)
        try:
            validate_adrs = WebDriverWait(driver, 3).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[3]/mat-card[2]/mat-card-content/address-info/div/div[2]/mat-slide-toggle/div/button")))
            validate_adrs.click()
            print("Validate Button clicked...")
        except:
            print("Validate address button not found")
            # To repeat the check
            return True
        time.sleep(3)
        try:
            yes_btn = WebDriverWait(driver, 13).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-confirmation-dialog/div[2]/button[2]")))
            yes_btn.click()
            print("Warning dismissed...")
        except:
            print("Validate address confirmation not appeared, trying again...")
            return True
        
        print("END of VALIDATE_ADDRESS Fucntion...")
        print("="*70)
        return False

# --------------------------------- Page 2 Program Select -------------------------------------
def page_2():
    print("Start of Page # 2 Fucntion...")
    print("="*70)
    try:
        medicaid = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "mat-radio-6-input")))
        income_based = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "mat-radio-7-input")))
        
        
        # If income based...
        if True:
            print("Choosing Income Based Program.")
            time.sleep(1)
            income_based.click()
            time.sleep(1)

            people_in_house = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "mat-input-12")))
            people = str(random.randint(2, 5))
            print(f"Entere {people} people in house hold.")
            people_in_house.send_keys("")
            people_in_house.send_keys(people)
        
        # If medicaid
        # else:
        #     print("Choosing Medicai Program.")
        #     time.sleep(1)
        #     medicaid.click()
        #     time.sleep(1)

        #     eligible_program = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "mat-select-2")))
        #     time.sleep(1)
        #     eligible_program.click()
        #     time.sleep(1)

        #     medicaid_drop_down = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "mat-option-4")))
        #     medicaid_drop_down.click()
        #     print("Medicaid Selected from Drop Down...")

        try:
            print("Submitting...")
            submit_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-program/div/div[2]/div[2]/button[2]")))
            time.sleep(1)
            submit_btn.click()            
            time.sleep(2)
            print("Submitted...")
        except:
            print("Error occured")
    except TimeoutException:
        print("Elements not found... Trying agiain...")
        page_2()
    # Check if next page appeared
    try:
        time.sleep(5)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "mat-radio-7-input"))).click()
        print("Still on page 2, calling PAGE_2 again.")
        page_2()
    except:
        pass
    print("End of Page # 2 Fucntion...")
    print("="*70)

# --------------------------------- Consent Form Page -------------------------------------
def consent_form():
    print("Start of CONSENT_FORM Fucntion...")
    print("="*70)
    try:
        submit_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-review/div/div/div[2]/self-enrollment-consent/div/mat-card/mat-card-content/button")))
        time.sleep(1)
        submit_btn.click()
        time.sleep(2)
    except TimeoutError:
        print("Form not appeared, trying again.")
        consent_form()
    print("End of CONSENT_FORM Fucntion...")
    print("="*70)

# --------------------------------- PopUp for Consent Form -------------------------------------
def consent_popup():
    print("Start of CONSENT_POPUP Fucntion...")
    print("="*70)
    try:
        print("Get Consent Form element.")
        consent_pop = WebDriverWait(driver, 25).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[1]")))
        try:
            print("Checking if consent form isDisplayed.")
            if consent_pop.is_displayed():
                print("Yes it is.")
                consent_check_1 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[1]/mat-checkbox")))
                consent_check_2 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[7]/div[1]/mat-checkbox")))
                consent_check_3 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[7]/div[2]/mat-checkbox")))
                consent_check_4 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[7]/div[3]")))
                consent_check_5 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[7]/div[4]/mat-checkbox")))
                print("Got all checkBoxes")
                
                submit_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[3]/button[2]")))
                print("Got Submit Btn")
                
                time.sleep(1)
                if not consent_check_1.is_selected():
                    print("1 Not selected already")
                    consent_check_1.click()
                else:
                    print("1 Already selected")
                time.sleep(1)
                if not consent_check_2.is_selected():
                    consent_check_2.click()
                time.sleep(1)
                if not consent_check_3.is_selected():
                    consent_check_3.click()
                time.sleep(1)
                if not consent_check_4.is_selected():
                    consent_check_4.click()
                time.sleep(1)
                if not consent_check_5.is_selected():
                    consent_check_5.click()
                time.sleep(1)
                submit_btn.click()
                print("Submitted.")
            else:
                print("Consent for is NOT Displayed yet. Waiting...")
                # time.sleep(10)
                consent_popup()
        except Exception as e:
            print(f"Error: {e}")
            consent_popup()
    except TimeoutError:
        print("Form not appeared, trying again.")
        consent_popup()
    # Check if still on Consent PopUp Page
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[1]/mat-checkbox")))
        print("Consent Popup still appeared, Calling CONSENT_POPUP again")
        consent_popup()
    except:
        pass
    print("End of CONSENT_POPUP Fucntion...")
    print("="*70)

# --------------------------------- Digital Sign Page -------------------------------------
def digital_sign(person):
    print("Start of DIGITAL_SIGN Fucntion...")
    print("="*70)
    try:
        time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.ID,"mat-select-4")))
        time.sleep(1)
        time_zone_drop.click()
        print("Drop Down Clicked.")
        
        utc_zone = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[1]")))
        atlantic = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[2]")))
        eastern = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[3]")))
        indiana = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[4]")))
        central = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[5]")))
        mountain = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[6]")))
        arizona = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[7]")))
        pacific = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[8]")))
        alaska = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[9]")))
        hawai = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[10]")))
        midway = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[11]")))
        port_mor = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[12]")))
        samoa = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[13]")))
    except Exception as e:
        print(f"Error:    {e}...")
        digital_sign()
    
    print("Selecting a time zone.")
    # If eastern daylight

    timezone = person["timezone"]
    print(f"Our Time zone is {timezone}")
    if timezone == "eastern":
        print("Selecting Eastern Time Zone.")
        eastern.click()
    else:
        print("Not eastern.")
        eastern.click()

    
    # After time zone:
    try:
        check_box = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/app-review/div/div/div[2]/self-enrollment-consent/div/mat-card[2]/mat-card-content/div[4]")))
        submit_btn = time_zone_drop = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/app-review/div/div/div[3]/div[3]/button")))
        time.sleep(1)
        check_box.click()
        print("Checked Sign Box.")
        time.sleep(1)
        submit_btn.click()
        print("Submitted.")
    except TimeoutError:
        print("Digitial Sign Check Box Not found... trying again...")
        digital_sign(person)
    
    print("End of DIGITAL_SIGN Fucntion...")
    print("="*70)

# --------------------------------- Store Final Message -------------------------------------
def post_popup():
    print("Start of FINAL_MESSAGE Fucntion...")
    print("="*70)
    try:
        popup = WebDriverWait(driver, 25).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container")))
        print("PopUp appeared.")
        time.sleep(5)
        print("Checking if Service Transfer Exception")
        service_transfer_exception()
        time.sleep(5)
        print("Checking if Error Message")
        error_message()
        
    except TimeoutError:
        print("No PopUp Appeared.")
        final_text = "No PopUp Appeared. Hope its Fine."
    print("End of FINAL_MESSAGE Fucntion...")
    print("="*70)

# --------------------------------- Check if error occured -------------------------------------
def service_transfer_exception():
    print("Start of SERVICE_TRANSFER Fucntion...")
    print("="*70)
    try:
        transfer_without = WebDriverWait(driver, 25).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/transfer-exception/div[2]/div/div/mat-radio-group/mat-radio-button[1]")))
        stopped_operating = WebDriverWait(driver, 25).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/transfer-exception/div[2]/div/div/mat-radio-group/mat-radio-button[2]")))
        moved_to_loc = WebDriverWait(driver, 25).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/transfer-exception/div[2]/div/div/mat-radio-group/mat-radio-button[3]")))
        print("Service Transfer options found.")
        transfer_without.click()
    except TimeoutError:
        pass
    print("End of SERVICE_TRANSFER Fucntion...")
    print("="*70)

# --------------------------------- Check if error occured -------------------------------------
def error_message():
    print("Start of ERROR_MESSAGE Fucntion...")
    print("="*70)
    global final_text
    try:
        ok_btn = WebDriverWait(driver, 25).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-confirmation-dialog/div[2]/button")))
        time.sleep(1)
        ok_btn.click()
        print("Got error, stored....")
        final_text = WebDriverWait(driver, 25).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container"))).text
        print("="*60)
        print(final_text)
        print("="* 60)
        return final_text 
    except TimeoutError:
        pass
    print("Start of ERROR_MESSAGE Fucntion...")
    print("="*70)
    

# --------------------------------- Driver function for program -------------------------------------
def driver():
    init()
    get_data_from_csv()
    start()

# --------------------------------- Running the program -------------------------------------
try:
    driver()
except Exception as e:
    print(e)
else:
    pass
finally:
    time.sleep(100)
    driver.quit()
    print("Creating output file.")
    df.to_csv("completed_records_with_results.csv", index=False)