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

# Setup Edge WebDriver
def setup_driver():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
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

# Scroll the page down and up randomly between 3 and 5 times
def scroll_page(driver):
    num_scrolls = random.randint(3, 5)  # Random number of scrolls (3 to 5)
    for _ in range(num_scrolls):
        # Randomize the scroll down and up distances
        scroll_down_distance = random.randint(200, 800)  # Scroll down distance
        scroll_up_distance = random.randint(200, 800)    # Scroll up distance
        
        # Scroll down
        driver.execute_script(f"window.scrollBy(0, {scroll_down_distance});")
        time.sleep(random.uniform(1.5, 3))  # Random pause after scrolling down
        
        # Scroll up
        driver.execute_script(f"window.scrollBy(0, -{scroll_up_distance});")
        time.sleep(random.uniform(1.5, 3))  # Random pause after scrolling up
    
    print(f"Scrolled the page {num_scrolls} times with random distances.")

# Perform searches
def perform_search(driver, num_searches=10):
    driver.get("https://www.bing.com")  # Default Edge search engine
    
    # Define the threshold for reload
    reload_after = random.randint(5, 10)
    search_count = 0

    for i in range(num_searches):
        sentence = random_sentence()
        print(f"Performing search: '{sentence}'")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )  # Wait for the search box to appear
        search_box.clear()
        search_box.send_keys(sentence + Keys.RETURN)
        
        # Wait for search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "b_results"))
        )  # Adjust selector based on Bing's search results container
        
        # Scroll the page after results are loaded
        scroll_page(driver)
        
        # Increment search counter
        search_count += 1

        # Check if it's time to reload the page
        if search_count >= reload_after:
            print(f"Reloading Bing search page after {search_count} searches...")
            driver.get("https://www.bing.com")
            search_count = 0  # Reset counter
            reload_after = random.randint(5, 10)  # Set a new random threshold
        
        # Random delay between 10 and 15 seconds
        delay = random.uniform(10, 15)
        print(f"Waiting for {delay:.2f} seconds before the next search...")
        time.sleep(delay)


# Main Function
if __name__ == "__main__":
    try:
        driver = setup_driver()
        perform_search(driver, num_searches=30)  # Number of searches
    finally:
        driver.quit()
