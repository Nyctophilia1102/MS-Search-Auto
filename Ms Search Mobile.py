import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import nltk
from nltk.corpus import words, brown

# Download required NLTK corpora
nltk.download("words")
nltk.download("brown")

# Setup Edge WebDriver for mobile emulation
def setup_driver():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")

    # Mobile emulation settings
    mobile_emulation = {
        "deviceName": "Pixel 2"  # Simulate a specific mobile device
    }
    edge_options.add_experimental_option("mobileEmulation", mobile_emulation)

    service = Service("D:\msedgedriver.exe")  # Replace with your WebDriver path
    return webdriver.Edge(service=service, options=edge_options)

# Generate random sentences with a random number of words between 4 and 10
def random_sentence(min_words=4, max_words=10):
    # Get a list of words from the Brown corpus
    word_list = brown.words()
    sentence = []
    
    # Randomize the sentence length between min_words and max_words
    sentence_length = random.randint(min_words, max_words)
    
    while len(sentence) < sentence_length:
        word = random.choice(word_list)
        if word.isalpha():  # Only use alphabetic words
            sentence.append(word.lower())
    
    # Capitalize the first word and join the words into a sentence
    return " ".join(sentence).capitalize()

# Perform searches
def perform_search(driver, num_searches=5):
    driver.get("https://www.bing.com")  # Default Edge search engine
    for _ in range(num_searches):
        sentence = random_sentence()
        print(f"Performing search: '{sentence}'")
        search_box = driver.find_element("name", "q")  # Search box element
        search_box.clear()
        search_box.send_keys(sentence + Keys.RETURN)
        
        # Random delay between  and  seconds
        delay = random.uniform(10, 15)
        print(f"Waiting for {delay:.2f} seconds before the next search...")
        time.sleep(delay)

# Main Function
if __name__ == "__main__":
    driver = None
    try:
        driver = setup_driver()
        perform_search(driver, num_searches=30)  # Number of searches
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Quit driver only if it was successfully initialized
        if driver:
            driver.quit()
