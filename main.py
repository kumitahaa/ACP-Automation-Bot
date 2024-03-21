# --------------------------------- Import -------------------------------------
import time, yaml, pandas as pd, random, traceback
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
remaining_df = ""
line_break = "=" * 60
enroll_id = ""
error_appeared = False
def get_data_from_csv():
    global df, remaining_df
    df = pd.read_csv("filtered.csv", )
    remaining_df = df.copy()
    print(df.head())

# --------------------------------- Initialize -------------------------------------
def init():
    global driver
    driver = uc.Chrome()
    driver.maximize_window()
# --------------------------------- Starts from Here -------------------------------------
def start():
    global df
    coming_message = """Error
N/A
Ok"""
    for index, person in df.iterrows():
    # Process one row at a time
        print(f"========== Processing {index+1}th Record ==========")
        print(line_break)
        print("=="*50)
        print("=="*50)
        print(person)
        print("=="*50)
        print("=="*50)
        open_page()
        login(person)
        coming_enrollment_id = page_1(person)
        if coming_enrollment_id == False:
            print("Error Appeared in Details Page...")
            coming_message = error_message()
            message = coming_message.split("\n")[1]
            enrollment_id = enroll_id.split(": ")[-1]
            continue
        else:
            page_2()
            consent_form()
            consent_popup()
            digital_sign()
            coming_message = post_popup()
            if error_appeared:
                message = coming_message.split("\n")[1]
                enrollment_id = coming_enrollment_id.split(": ")[-1]
                continue
            else:
                device_type_page()
                success_page()
                message = coming_message.split("\n")[1]
                enrollment_id = coming_enrollment_id.split(": ")[-1]
                
        # Write to new Column
        df.loc[index, 'result_message'] = message
        print(df.loc[index, 'result_message'])
        df.loc[index, 'enrollment_id'] = enrollment_id
        print(df.loc[index, 'enrollment_id'])
        print("=="*50)
        print("=="*50)
        remaining_df.drop(index, inplace=True)
    # Save the csv at the FINALLY BLOCK

# --------------------------------- Open WebPage -------------------------------------
def open_page():
    driver.execute_script("window.open('about:blank', '_blank');")
    
    driver.switch_to.window(driver.window_handles[-1])
    
    search_url = f"https://maxsip.legendari.tech/enroll/mhaider1/start"
    driver.get(search_url)
    print("Opened WebPage in new tab...")
    print("="*70)
    
    # Close all other tabs except the new one
    for handle in driver.window_handles[:-1]:
        driver.switch_to.window(handle)
        driver.close()
    
    # Switch back to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    

# --------------------------------- Login -------------------------------------
def login(person):
    print("Start of LOGIN Fucntion...")
    print("="*70)
    try:
        zip_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/base-info/div/div[2]/mat-card/mat-card-content/div[1]/div[2]/mat-form-field[1]/div[1]/div/div[2]/input")))
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/base-info/div/div[2]/mat-card/mat-card-content/div[1]/div[2]/mat-form-field[2]/div[1]/div/div[2]/input")))
        
        zip_code = person["zip"]
        zip_field.send_keys("")
        zip_field.send_keys(zip_code)
        email_addrs = person["email"]
        email_field.send_keys("")
        email_field.send_keys(email_addrs)
        time.sleep(3)
        submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/base-info/div/div[2]/mat-card/mat-card-content/div[2]/button")))
        # Check if plans are clickable.
        driver.execute_script("""
document.getElementsByClassName("mat-mdc-radio-touch-target")[1].click();
""")
        print("Clicked on 2nd button if possible.")
        time.sleep(2)
        submit_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/base-info/div/div[2]/mat-card/mat-card-content/div[2]/button")))
        # if submit_btn.is_enabled():
        #     time.sleep(2)
        submit_btn.click()
    except TimeoutException:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[2]/div/mat-card/mat-card-content/personal-info/div/div[1]/div[1]/mat-form-field/div[1]/div/div[2]/input")))
            print("We are already on Page 1. Ending Login Here...")
            return 0
        except:
            print("Login Fields not there... Trying again.")
            login(person)
    
    # Check if next page appeared
    try:
        time.sleep(3)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/base-info/div/div[2]/mat-card/mat-card-content/div[1]/div[2]/mat-form-field[2]/div[1]/div/div[2]/input"))).send_keys("test")
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
    global enroll_id
    enrollment_id = "Your Enrollment ID: N/A"
    try:
        first_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[2]/div/mat-card/mat-card-content/personal-info/div/div[1]/div[1]/mat-form-field/div[1]/div/div[2]/input")))
        last_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[2]/div/mat-card/mat-card-content/personal-info/div/div[1]/div[3]/mat-form-field/div[1]/div/div[2]/input")))
        ssn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[2]/div/mat-card/mat-card-content/personal-info/div/div[2]/div[3]/mat-form-field/div[1]/div/div[2]/input")))

        personal_contact_number = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[3]/mat-card[1]/mat-card-content/contact-info/div/mat-form-field/div[1]/div/div[2]/input")))
        
        address_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[3]/mat-card[2]/mat-card-content/address-info/address-inputs/div/div[1]/div/address-select/mat-form-field/div[1]/div/div[2]/input")))
        submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[4]/button")))
        enrollment_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/div/span"))).text
        enroll_id = enrollment_id

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
        print("Entered Address.")

        dob_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[2]/div/mat-card/mat-card-content/personal-info/div/div[2]/div[1]/mat-form-field/div[1]/div/div[2]/input")))
        dob_field_id = dob_field.get_attribute("id")
        driver.execute_script(f"""
            var dobField = document.getElementById("{dob_field_id}");
            dobField.readOnly = false;
            console.log("DOB now accepts Input..");
""")
        time.sleep(1)
        dob = person.dob
        dob_field.send_keys(dob)
        print("DOB entered.")

        time.sleep(1)
        submit_btn.click()
        print("clicked submit")
        time.sleep(1)
        
        # Check for Error
        try:
            print("Checking for Duplicate Error")
            popup = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                    By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container")))
            print("PopUp appeared.")
            return False
        except TimeoutException:
            print("Duplicate Error Not Found.")  

        # Check Address Validaton
        try:
            print("Checking if adrs bar is there.")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[3]/mat-card[2]/mat-card-content/address-info/address-inputs/div/div[1]/div/address-select/mat-form-field/div[1]/div/div[2]/input")))
            valid = validate_address()
            if not valid:
                time.sleep(1)
                submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[4]/button")))
                submit_btn.click()
        except TimeoutException:
            # print("Submitted...")
            print("Address perfectly validated.")
            valid = False
        while valid:
            print("Inside the While Loop")
            try:
                time.sleep(1)
                WebDriverWait(driver, 4).until(EC.presence_of_element_located((
                    By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[3]/mat-card[2]/mat-card-content/address-info/address-inputs/div/div[1]/div/address-select/mat-form-field/div[1]/div/div[2]/input")))
                print("Clicking DON'T VALIDATE...")
                valid = validate_address()
            except:
                print("Address perfectly validated.")
                valid = False
    except TimeoutException:
        try:
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-program/div/div[2]/div[1]/mat-card/mat-card-content/div/mat-radio-group/mat-radio-button[2]")))
            print("We are already on Page 2. Ending Page_1 Function.")
            return enrollment_id
        except:
            print("Objects not found, trying again...")
            page_1(person)
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-program/div/div[2]/div[2]/button[1]/span[1]")))
            print("We are on Page 2...")
            return enrollment_id
        except:
            pass
        page_1(person)
    
    # Check if next page is appeared
    try:
        time.sleep(3)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/customer-info/div/div/div[2]/div/mat-card/mat-card-content/personal-info/div/div[1]/div[1]/mat-form-field/div[1]/div/div[2]/input"))).click()
        print("Still on Page 1... Calling Page#1 Again...")
        page_1(person)
    except:
        pass
    print("End of PAGE_1 Fucntion...")
    print("="*70)
    return enrollment_id

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
        time.sleep(2)
        try:
                yes_btn = WebDriverWait(driver, 7).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-confirmation-dialog/div[2]/button[2]")))
                yes_btn.click()
                print("Warning dismissed...")
                time.sleep(1)
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
        medicaid = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-program/div/div[2]/div[1]/mat-card/mat-card-content/div/mat-radio-group/mat-radio-button[1]")))
        income_based = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-program/div/div[2]/div[1]/mat-card/mat-card-content/div/mat-radio-group/mat-radio-button[2]")))
        
        
        # If income based...
        if True:
            print("Choosing Income Based Program.")
            time.sleep(1)
            income_based.click()
            time.sleep(1)

            people_in_house = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-12")))
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

        #     eligible_program = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-select-2")))
        #     time.sleep(1)
        #     eligible_program.click()
        #     time.sleep(1)

        #     medicaid_drop_down = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-option-4")))
        #     medicaid_drop_down.click()
        #     print("Medicaid Selected from Drop Down...")

        try:
            submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-program/div/div[2]/div[2]/button[2]")))
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
        time.sleep(2)
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "mat-radio-7-input"))).click()
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
        submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.XPATH, "/html/body/app-root/new-self-enrollment/div/div/app-review/div/div/div[2]/self-enrollment-consent/div/mat-card/mat-card-content/button")))
        submit_btn.click()
        time.sleep(2)
    except TimeoutException:
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
        consent_pop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[1]")))
        try:
            if consent_pop.is_displayed():
                consent_check_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[1]/mat-checkbox")))
                consent_check_2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[7]/div[1]/mat-checkbox")))
                consent_check_3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[7]/div[2]/mat-checkbox")))
                consent_check_4 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[7]/div[3]")))
                consent_check_5 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[7]/div[4]/mat-checkbox")))
                print("Got all checkBoxes")
                
                submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[3]/button[2]")))
                
                submit_btn.click()
                
                time.sleep(2)
                print("Checking boxes...")

                if not consent_check_1.is_selected():
                    consent_check_1.click()
                if not consent_check_2.is_selected():
                    consent_check_2.click()
                if not consent_check_3.is_selected():
                    consent_check_3.click()
                if not consent_check_4.is_selected():
                    consent_check_4.click()
                if not consent_check_5.is_selected():
                    consent_check_5.click()
                
                time.sleep(2)
                submit_btn.click()
                print("Submitted.")
            else:
                print("Consent for is NOT Displayed yet. Waiting...")
                # time.sleep(10)
                consent_popup()
        except Exception as e:
            print(f"Error: {e}")
            consent_popup()
    except TimeoutException:
        print("Form not appeared, trying again.")
        consent_popup()
    # Check if still on Consent PopUp Page
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-consent-dialog/div[2]/div/div[1]/mat-checkbox")))
        print("Consent Popup still appeared, Calling CONSENT_POPUP again")
        consent_popup()
    except:
        pass
    print("End of CONSENT_POPUP Fucntion...")
    print("="*70)

# --------------------------------- Digital Sign Page -------------------------------------
def digital_sign():
    print("Start of DIGITAL_SIGN Fucntion...")
    print("="*70)
    try:
        time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.ID,"mat-select-4")))
        time.sleep(1)
        time_zone_drop.click()
        print("Drop Down Clicked.")
        
        utc_zone = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[1]")))
        atlantic = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[2]")))
        eastern = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[3]")))
        indiana = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[4]")))
        central = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[5]")))
        mountain = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[6]")))
        arizona = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[7]")))
        pacific = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[8]")))
        alaska = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[9]")))
        hawai = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[10]")))
        midway = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[11]")))
        port_mor = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[12]")))
        samoa = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[13]")))
    except Exception as e:
        print(f"Error:    {e}...")
        traceback.print_exc()
        digital_sign()
    
    print("Selecting Eastern Time Zone.")
    eastern.click()
    # print("Selecting a time zone.")
    # If eastern daylight

    # timezone = person["timezone"]
    # print(f"Our Time zone is {timezone}")
    # if timezone == "eastern":
        # print("Selecting Eastern Time Zone.")
    #     eastern.click()
    # else:
    #     print("Not eastern.")
        # eastern.click()

    
    # After time zone:
    try:
        check_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/app-review/div/div/div[2]/self-enrollment-consent/div/mat-card[2]/mat-card-content/div[4]")))
        submit_btn = time_zone_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/app-review/div/div/div[3]/div[3]/button")))
        check_box.click()
        print("Checked Sign Box.")
        time.sleep(1)
        submit_btn.click()
        print("Submitted.")
    except TimeoutException:
        print("Digitial Sign Check Box Not found... trying again...")
        digital_sign()
    
    print("End of DIGITAL_SIGN Fucntion...")
    print("="*70)

# --------------------------------- Store Final Message -------------------------------------
def post_popup():
    message = """Error
N/A
Ok"""
    print("Start of FINAL_MESSAGE Fucntion...")
    print("="*70)
    try:
        popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container")))
        print("A PopUp has appeared.")
        time.sleep(2)
        print("Checking if Service Transfer Exception")
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/transfer-exception/div[2]/div/div/mat-radio-group/mat-radio-button[1]")))
            service_transfer_exception()
        except TimeoutException:
            print("Transfer Service Not Found...")
        time.sleep(2)
        print("Checking if Error Message")
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-confirmation-dialog/div[2]/button")))
            message = error_message()
        except TimeoutException:
            print("No error appeared...")
    except TimeoutException:
        print("No PopUp Appeared.")  
    
    try:
        print("Trying to submit.")
        submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/app-review/div/div/div[3]/div[3]/button")))
        time.sleep(1)
        submit_btn.click()
    except Exception as e:
        print(f"Submit Button can't be clicked, Error: {e}")

    print("End of FINAL_MESSAGE Fucntion...")
    print("="*70)
    return message

# --------------------------------- Check if error occured -------------------------------------
def service_transfer_exception():
    print("Start of SERVICE_TRANSFER Fucntion...")
    print("="*70)
    try:
        transfer_without = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/transfer-exception/div[2]/div/div/mat-radio-group/mat-radio-button[1]")))
        print("Service Transfer options found.")
        submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/transfer-exception/div[3]/button[2]")))
        transfer_without.click()
        time.sleep(1)
        submit_btn.click()
    except TimeoutException:
        print("Transfer Service Not Appeared...")
    print("End of SERVICE_TRANSFER Fucntion...")
    print("="*70)

# --------------------------------- Check if error occured -------------------------------------
def error_message():
    print("Start of ERROR_MESSAGE Fucntion...")
    print("="*70)
    global final_text
    global error_appeared
    error_appeared = False
    try:
        ok_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-confirmation-dialog/div[2]/button")))
        print("Error is stored....")
        final_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/mat-dialog-container"))).text
        print("="*60)
        print(final_text)
        print("="* 60)
        time.sleep(1)
        ok_btn.click()
        error_appeared = True
        return final_text
    except TimeoutException:
        print("No error appeared...")
        final_text = "No PopUp Appeared. Hope its Fine."

    print("Start of ERROR_MESSAGE Fucntion...")
    print("="*70)

# --------------------------------- Driver function for program -------------------------------------
def device_type_page():
    print("Start of DEVICE_TYPE_PAGE Fucntion...")
    print("="*70)
    try:
        time.sleep(1)
        drop_down = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/web-enrollment-plan/div/div[2]/div[1]/mat-card/mat-card-content/div/mat-form-field/div[1]/div/div[2]/mat-select")))
        drop_down.click()
        time.sleep(1)
        sim =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/div[3]/div[2]/div/div/mat-option[1]")))
        sim.click()
        time.sleep(1)
        submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/web-enrollment-plan/div/div[2]/div[2]/button[2]")))
        submit_btn.click()
    except TimeoutException:
        print("Device Type elements not found.")
        try:
            check_box = time_zone_drop = WebDriverWait(driver, 4).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/app-review/div/div/div[2]/self-enrollment-consent/div/mat-card[2]/mat-card-content/div[4]")))
            print("Still on Consent Page. It means we are not having Deivce Type.")
        except TimeoutException:
            print("Not on Consent Page, look for Device Options again.")
            device_type_page()
    print("Start of DEVICE_TYPE_PAGE Fucntion...")
    print("="*70)


def success_page():
    try:
        enroll_id =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.XPATH,"/html/body/app-root/new-self-enrollment/div/div/web-enrollment-thanks/div/div/p[1]"))).text
        return enroll_id
    except TimeoutException:
        print("Enrollment ID not found. Try again...")

# --------------------------------- Driver function for program -------------------------------------
def driver():
    init()
    get_data_from_csv()
    start()

# --------------------------------- Running the program -------------------------------------
try:
    driver()
except Exception as e:
    print("==="*30)
    print("==="*30)
    print("ENDING.... EXCEPTION...")
    print("==="*30)
    print("==="*30)
    print(f"Exception occured: {e}")
    traceback.print_exc()
else:
    pass
finally:
    print("==="*30)
    print("==="*30)
    print("ENDING.... FINALLY...")
    print("==="*30)
    print("==="*30)
    driver.quit()
    df.to_csv("completed_records_with_results.csv", index=False)
    remaining_df.to_csv("filtered_remain.csv", index=False)
    print("Created Remaining File..")
    print("Created output file.")
    print("100 Seconds wait...")
    time.sleep(100)