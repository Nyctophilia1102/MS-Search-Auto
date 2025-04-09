import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Import EC for expected conditions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import nltk
from nltk.corpus import words, brown

# Download required NLTK corpora
nltk.download("words")
nltk.download("brown")

# List of random mobile devices for emulation
MOBILE_DEVICES = [
    "Pixel 3",
    "Samsung Galaxy S20 Ultra",
    "Samsung Galaxy A51/71",
]

def setup_driver():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    
    # Select a random mobile device
    random_device = random.choice(MOBILE_DEVICES)
    print(f"Emulating device: {random_device}")
    
    # Mobile emulation settings
    mobile_emulation = {"deviceName": random_device}
    edge_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    service = Service("D:\\msedgedriver.exe")  # Replace with your WebDriver path
    return webdriver.Edge(service=service, options=edge_options)

def random_sentence(min_words=4, max_words=10):
    word_list = brown.words()
    sentence = []
    sentence_length = random.randint(min_words, max_words)

    while len(sentence) < sentence_length:
        word = random.choice(word_list)
        if word.isalpha():
            sentence.append(word.lower())

    return " ".join(sentence).capitalize()

def scroll_page(driver):
    num_scrolls = random.randint(3, 5)
    for _ in range(num_scrolls):
        down = random.randint(200, 800)
        up = random.randint(200, 800)

        driver.execute_script(f"window.scrollBy(0, {down});")
        time.sleep(random.uniform(1.5, 3))
        driver.execute_script(f"window.scrollBy(0, -{up});")
        time.sleep(random.uniform(1.5, 3))

    print(f"🖱️ Scrolled {num_scrolls} times.")

def countdown(seconds):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        print(f"⏳ Waiting: {mins:02d}:{secs:02d} remaining", end='\r')
        time.sleep(1)
    print("⏰ Break finished! Continuing...\n")

def perform_search(driver, total_searches=35, batch_size=5, pause_duration=960):
    driver.get("https://www.bing.com")
    for i in range(1, total_searches + 1):
        sentence = random_sentence()
        print(f"🔍 Search {i}/{total_searches}: '{sentence}'")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(sentence + Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "b_results"))
        )

        scroll_page(driver)

        delay = random.uniform(6, 8)
        print(f"⏳ Waiting {delay:.2f} seconds before next search...\n")
        time.sleep(delay)

        if i % batch_size == 0 and i < total_searches:
            print(f"🔁 Returning to Bing homepage before 16-minute break...")
            driver.get("https://www.bing.com")
            time.sleep(2)
            print(f"🛑 Pausing for 16 minutes...\n")
            countdown(pause_duration)

if __name__ == "__main__":
    driver = setup_driver()
    try:
        perform_search(driver, total_searches=35, batch_size=5, pause_duration=960)
    finally:
        driver.quit()
