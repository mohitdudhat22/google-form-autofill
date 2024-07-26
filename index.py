from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def fill_google_form(form_url):
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Open the form
        driver.get(form_url)

        # Wait for the form to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )

        # Print all questions
        questions = driver.find_elements(By.CSS_SELECTOR, "span.M7eMe")
        print(questions)
        for idx, question in enumerate(questions):
            print(f"Question {idx+1}: {question.text}")

        # Fill out text fields
        text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        for i, input_field in enumerate(text_inputs):
            input_field.send_keys(f"Answer {i+1}")

        # Fill out text areas
        text_areas = driver.find_elements(By.CSS_SELECTOR, "textarea")
        for i, text_area in enumerate(text_areas):
            text_area.send_keys(f"Long Answer {i+1}")

        # Select radio buttons (selects the first option for each question)
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        for button in radio_buttons:
            if button.get_attribute("name") not in [rb.get_attribute("name") for rb in radio_buttons[:radio_buttons.index(button)]]:
                button.click()

        # Select checkboxes (selects the first option for each question)
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        for checkbox in checkboxes:
            if checkbox.get_attribute("name") not in [cb.get_attribute("name") for cb in checkboxes[:checkboxes.index(checkbox)]]:
                checkbox.click()

        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
        submit_button.click()

        print("Form submitted successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

# Usage
# form_url = input("Please enter the Google Form URL: ")
fill_google_form("https://forms.gle/jXN6mFwsGyie9qGL9")
