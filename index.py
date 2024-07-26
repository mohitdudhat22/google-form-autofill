from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def fill_google_form(form_url, data_dict):
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

        # Print all questions and map fields
        questions = driver.find_elements(By.CSS_SELECTOR, "span.M7eMe")
        print("Questions:")
        question_texts = [question.text for question in questions]
        for idx, text in enumerate(question_texts):
            print(f"Question {idx+1}: {text}")

        # Fill out fields based on the dictionary
        for field_name, field_value in data_dict.items():
            found = False
            for question in questions:
                if field_name.lower() in question.text.lower():
                    found = True
                    if "position" in field_name.lower():  # Handle MCQ
                        # Find radio buttons
                        radio_buttons = driver.find_elements(By.CSS_SELECTOR, "div[role='radio']")
                        print(f"Radio Buttons for '{field_name}': {len(radio_buttons)}")
                        for button in radio_buttons:
                            aria_label = button.get_attribute("aria-label")
                            if field_value.lower() in aria_label.lower():
                                # Scroll into view and click the option
                                driver.execute_script("arguments[0].scrollIntoView();", button)
                                button.click()
                                break
                    else:
                        input_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                        for field in input_fields:
                            if not field.get_attribute("value"):  # Fill only empty fields
                                field.send_keys(field_value)
                                break
                    break

            if not found:
                print(f"Field '{field_name}' not found in the form.")

        # Submit the form
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button']"))
        )
        submit_button.click()

        print("Form submitted successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

# Usage
form_url = "https://forms.gle/jXN6mFwsGyie9qGL9"
data_dict = {
    "Name": "Mohit Dudhat",
    "Phone Number": "9913239031",
    "Position": "Full Stack Developer"  # MCQ field
}
fill_google_form(form_url, data_dict)
