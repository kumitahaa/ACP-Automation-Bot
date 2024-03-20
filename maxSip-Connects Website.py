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
person = []
line_break = "=" * 60

def get_data_from_csv():
    global person
    person = pd.read_csv("person.csv", index_col= None)


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
def start(input_names, state_name=""):
    pass
    

# --------------------------------- Open WebPage -------------------------------------
def open_page():
    print("Start of OPEN_PAGE Fucntion...")
    search_url = f"https://maxsipconnects-web.telgoo5.com/BUYFLOW/?wy4eJo0upYNGlirge3PUgBw2rS90yAf1aR90o2QmtzI"
    driver.get(search_url)
    print("Opened WebPage...")


# --------------------------------- Login -------------------------------------
def login():
    print("Start of LOGIN Fucntion...")
    try:
        zip_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.ID, "enrollment_zipcode_popup")))
        email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.ID, "enrollment_email_id_step_1_popup")))
        submit_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[6]/div[1]/div/div/div/div[2]/div/div[4]/p/button")))
        zip_code="19720"
        zip_field.send_keys(zip_code)
        email_addrs="Edith@gmail.com"
        email_field.send_keys(email_addrs)
        time.sleep(1)
        submit_btn.click()
    except TimeoutException:
        print("Fields not there... Trying again.")
        login()

def page_1():
    print("Start of PAGE # 1 Fucntion...")
    try:
        first_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "first_name")))
        last_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "last_name")))
        ssn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "enroll_ssn")))
        dob_month = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "enroll_month")))
        dob_day = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "dob_day")))
        dob_year = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "dob_year")))
        personal_contact_number = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "personal_contact_number")))
        
        submit_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/form/fieldset/div/div[2]/div[1]/div[1]/div/button")))

        check_boxes = driver.find_elements(By.CLASS_NAME, "checkmark")
        email_check = check_boxes[0]
        phone_check = check_boxes[1]

        first_name.send_keys("Edith")
        print("First Name entered...")
        last_name.send_keys("Chewning")
        print("Last Name entered...")
        ssn.send_keys("6830")
        print("SSN entered...")
        month = "06"
        driver.execute_script(f"""
    var a = document.getElementById("enroll_month");
    a.value = "{month}"
    console.log('Month value set to: {month}');
""")
        print("DOB_Month entered...")
        dob_day.send_keys("20")
        dob_year.send_keys("1950")
        personal_contact_number.send_keys("3028579818")
        time.sleep(1)
        email_check.click()
        time.sleep(1)
        phone_check.click()
        time.sleep(1)

        submit_btn.click()
    except TimeoutException:
        print("Objects not found, trying again...")
        page_1()


def page_2():
    print("Start of PAGE # 2 Fucntion...")
    try:
        address_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "enroll_address1")))
        
        submit_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/form/fieldset/div/div[2]/div[1]/div[1]/div/button[2]")))
        address = "20 Blyth"
        driver.execute_script(f"""
    var a = document.getElementById("enroll_address1");
    a.value = "{address}"
    console.log('Month value set to: {address}');
""")
        time.sleep(1)
        submit_btn.click()
        address_popup()
    except TimeoutException:
        print("Elements not Found, trying again...")
        page_2()


def address_popup():
    print("Start of ADRESS_POPUP for page# 2 Fucntion...")
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "box-upsp")))
        
        buttons = driver.find_elements(By.CLASS_NAME, "swal-button")
        submit_btn = buttons[1]
        time.sleep(1)
        submit_btn.click()
    except TimeoutException:
        print("Still waiting for Popup...")
        address_popup()
    

def living_with_18_q():
    print("Start of LIVING_WITH_Q for page # 2 Fucntion...")
    try:
        yes_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/form/fieldset/div/div[2]/div[2]/div/div/div[3]/p/button")))
        time.sleep(1)
        yes_button.click()
    except TimeoutException:
        print("No Objects, Trying again...")
        living_with_18_q()


def they_get_acp_q():
    print("Start of GET_ACP_Q for page # 2 Fucntion...")
    try:
        no_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/form/fieldset/div/div[2]/div[2]/div/div[2]/button")))
        time.sleep(1)
        no_button.click()
    except TimeoutException:
        print("No Objects, Trying again...")
        they_get_acp_q()


def choose_plan():
    print("Start of CHOOSE_PLAN Fucntion...")
    try:
        medicaid = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_0")))
        nutrition_program = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_1")))
        security_income = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_2")))
        fed_housing = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_3")))
        vet_pension = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_4")))
        wic_nutrition = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_5")))
        fed_pell_grant = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_6")))
        school_lunch = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_7")))
        income_based = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "program_list_1000")))
        submit_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/form/fieldset/div/div[2]/div/div[3]/div/button[2]")))
    except TimeoutException:
        print("Elements not found... Trying agiain...")
        choose_plan()

    time.sleep(1)
    income_based.click()
    income_based_detail()
    print("Back in Choose Plan to get Popup.")

    time.sleep(1)
    submit_btn.click()

    time.sleep(1)
    device_warning_pop()

    time.sleep(1)
    complete_popup()

def device_warning_pop():
    try:
        pop_list = driver.find_elements(By.CLASS_NAME, "modal-content")
        popup = pop_list[6]
        if popup.isDisplayed():
           print("Devic Warning Popup Displayer")
           yes_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "done-house-hold")))
           yes_btn.click()
           select_plan_for_SIM()
        else:
            print("No Device Warning")
    except Exception as e:
        print(e)


def select_plan_for_SIM():
    try:
        submit_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/form/fieldset/div/div[2]/div/div[6]/div/button[2]")))
        time.sleep()
        submit_btn.click()

        select_plan_for_SIM()
    except TimeoutError:
        print("SIM service not found... Trying again...")
        select_plan_for_SIM()


def select_plan_for_SIM():
    try:
        sim_card = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.ID, "tickDIV_00")))
        submit_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/form/fieldset/div/div[2]/div/div[2]/div[4]/div/button[2]")))
        
        time.sleep(1)
        sim_card.click()
        time.sleep(1)
        submit_btn.click()
    except TimeoutError:
        print("SIM service not found... Trying again...")
        select_plan_for_SIM()

def consent_form():
    try:
        check_all = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.ID, "checkAll")))
        q1_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.ID, "acp_benefit_transfer_question1")))
        q2_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.ID, "acp_benefit_transfer_question2")))
        
        time.sleep(1)
        check_all.click()
        time.sleep(1)
        q2_btn.click()
    except TimeoutError:
        print("Consent not appeared. trying again.")
        consent_form()

def complete_popup():
    time.sleep(5)
    print("Start of COMPLETE_POPUP Fucntion...")
    try:
        global final_text
        popup = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CLASS_NAME, "swal-modal")))
        ok_btn = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CLASS_NAME, "swal-button")))
        final_text = popup.text
        print(final_text)
        time.sleep(1)
        ok_btn.click()
    except TimeoutException:
        print("Popup not found... Trying agiain...")
        complete_popup()


def income_based_detail():
    print("Start of ICOME_BASED Fucntion...")
    time.sleep(5)
    try:
        people_in_house = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "house_hold_input")))
        acknow_check = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "checkmark")))
        submit_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/form/fieldset/div/div[7]/div/div/div[3]/button")))
        
        people = str(random.randint(2, 5))
        people_in_house.send_keys(people)
        time.sleep(1)
        acknow_check.click()
        time.sleep(1)
        submit_btn.click()
    except TimeoutException:
        print("Elements not found... Trying agiain...")
        income_based_detail()
    print("End of ICOME_BASED Fucntion...")
    
    
    
def driver():
    init()
    time.sleep(1)
    print("INIT compelte")
    open_page()
    print("OPEN_PAGE compelte")
    time.sleep(1)
    login()
    print("LOGIN compelte")
    time.sleep(1)
    page_1()
    print("PAGE # 1 compelte")
    time.sleep(1)
    page_2()
    print("PAGE # 2 compelte")
    time.sleep(1)
    living_with_18_q()
    print("LIVING 18 yr/0 compelte")
    time.sleep(1)
    they_get_acp_q()
    print("THEY GET ACP compelte")
    time.sleep(1)
    choose_plan()
    print("CHOOSE PLAN compelte")

try:
    driver()
except:
    pass
else:
    pass
finally:
    print("Finally Block...")
    driver.quit()