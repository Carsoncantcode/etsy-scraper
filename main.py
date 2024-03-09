import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()

driver = webdriver.Chrome(options=chrome_options)

with open("etsy_bestsellers.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Product Link", "Star Rating", "Review Count"])
    num_pages = 10
    for page in range(1, num_pages + 1):
        url = f"https://www.etsy.com/search?q=toys&ref=pagination&page={page}"
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        bestseller_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.v2-listing-card")))

        for card in bestseller_cards:
            try:
                card.find_element(By.CSS_SELECTOR, "span.wt-badge--promoted")
                product_name = card.find_element(By.CSS_SELECTOR, "h3.v2-listing-card__title").text.strip()

                product_link = card.find_element(By.CSS_SELECTOR, "a.listing-link").get_attribute("href")

                star_rating_element = card.find_element(By.CSS_SELECTOR, "div[role='img']")
                star_rating = star_rating_element.get_attribute("aria-label")

                review_count_element = card.find_element(By.CSS_SELECTOR, "p.wt-text-body-smaller")
                review_count = review_count_element.text.strip("()")

                writer.writerow([product_name, product_link, star_rating, review_count])
            except:
                pass

# Close the browser
driver.quit()