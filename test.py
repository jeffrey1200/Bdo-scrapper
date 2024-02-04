from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"

driver = webdriver.Chrome(options=options)

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(5)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

select_box = driver.find_element(by=By.NAME, value="my-select")
select = Select(select_box)
select.select_by_visible_text("Two")
# c = select.all_selected_options
print(select)

text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
text = message.text

driver.quit()
