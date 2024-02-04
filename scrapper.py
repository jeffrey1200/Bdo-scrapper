import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with

WEAPONS_CACHE_PATH = "cached_data/weapon_list.json"
ARMOR_CACHE_PATH = "cached_data/armor_list.json"
SUB_WEAPON_CACHE_PATH = "cached_data/sub_weapon_list.json"
CACHE_EXPIRY = 24 * 3600


def cache_needs_update(new_data, cache_file_path):
    if not os.path.exists(cache_file_path):
        return True
    with open(cache_file_path, "r") as file:
        old_data = json.load(file)
    return new_data != old_data


def save_cache(data, cache_file_path):
    with open(cache_file_path, "w") as file:
        json.dump(data, file, indent=4)


def load_cache(cache_file_path):
    if not os.path.exists(cache_file_path):
        return None
    current_time = time.time()
    file_time = os.path.getmtime(cache_file_path)
    if current_time - file_time < CACHE_EXPIRY:
        with open(cache_file_path, "r") as file:

            return json.load(file)
    else:
        return None


def scrapeAllItemsPage(driver):
    allData = []
    table_data = driver.find_elements(By.CSS_SELECTOR, "tbody > tr")
    for row in table_data:
        item_id = row.find_element(By.CSS_SELECTOR, "td.dt-id").text

        item_link = row.find_element(
            By.CSS_SELECTOR, "td.dt-icon a")
        href = item_link.get_attribute("href")
        # item_quality = item_link.get_attribute("class")
        item_name = row.find_element(
            By.CSS_SELECTOR, "td.dt-title b").text

        # print(f"ID: {item_id}, Link: {item_link}, Name: {item_name}")
        allData.append({"id": item_id, "name": item_name,
                        "item_link": href})
    # filtered_data = [objs for objs in allData if objs.name.startswith("")]
    # for data in allData:
    #     if data.name.startswith("[Hunting]"):
    #         del data
    return allData


def scrapeTableData(driver):

    sellable_item_checkbox = driver.find_element(
        by=By.ID, value="WeaponTable_misc_0")
    sellable_item_checkbox.click()
    item_quantity_select = driver.find_element(
        by=By.NAME, value="WeaponTable_length")
    select = Select(item_quantity_select)
    select.select_by_visible_text("100")
    wait_for_table_data = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "even"))
    )
    allData = []
    while True:
        allData += scrapeAllItemsPage(driver)
        # table_data = driver.find_elements(By.CSS_SELECTOR, "tbody > tr")
        # for row in table_data:
        #     item_id = row.find_element(By.CSS_SELECTOR, "td.dt-id").text

        #     item_link = row.find_element(
        #         By.CSS_SELECTOR, "td.dt-icon a")
        #     href = item_link.get_attribute("href")
        #     # item_quality = item_link.get_attribute("class")
        #     item_name = row.find_element(
        #         By.CSS_SELECTOR, "td.dt-title b").text

        #     # print(f"ID: {item_id}, Link: {item_link}, Name: {item_name}")
        #     allData.append({"id": item_id, "name": item_name,
        #                     "item_link": href})
        # print(allData)
        next_button = driver.find_element(
            By.CSS_SELECTOR, "#WeaponTable_next")
        if "disabled" in next_button.get_attribute("class"):
            break

        else:
            # print(next_button.is_enabled(), "inside if")
            driver.execute_script(
                """document.querySelector("#WeaponTable_next").click()""")
        # allData = list({"id": item_id, "name": item_name,
        #                 "item_link": href})
    # print(allData)
    return allData


def main(page_category, cache_file_path):

    data = load_cache(cache_file_path)

    print(data)
    if data is None or cache_needs_update(data, cache_file_path):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = "eager"

        driver = webdriver.Chrome(options=options)
        weapons_url = f"https://bdocodex.com/us/{page_category}/"
        driver.get(weapons_url)
        driver.implicitly_wait(2)

        try:

            new_data = scrapeTableData(driver)
            save_cache(new_data, cache_file_path)
            data = new_data

        finally:
            driver.quit()

            # sellable_item_checkbox = driver.find_element(
            #     by=By.ID, value="WeaponTable_misc_0")
            # sellable_item_checkbox.click()
            # item_quantity_select = driver.find_element(
            #     by=By.NAME, value="WeaponTable_length")
            # select = Select(item_quantity_select)
            # select.select_by_visible_text("100")
            # wait_for_table_data = WebDriverWait(driver, 5).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "even"))
            # )

            # allData = scrapeTableData(driver)
            # print(allData)
            # while True:
            # scrapeTableData(driver)
            # table_data = driver.find_elements(By.CSS_SELECTOR, "tbody > tr")
            # for row in table_data:
            #     item_id = row.find_element(By.CSS_SELECTOR, "td.dt-id").text

            #     item_link = row.find_element(
            #         By.CSS_SELECTOR, "td.dt-icon a")
            #     href = item_link.get_attribute("href")
            #     # item_quality = item_link.get_attribute("class")
            #     item_name = row.find_element(
            #         By.CSS_SELECTOR, "td.dt-title b").text

            #     # print(f"ID: {item_id}, Link: {item_link}, Name: {item_name}")
            #     allData.append({"id": item_id, "name": item_name,
            #                     "item_link": href})
            #     print(allData)
            # next_button = driver.find_element(
            #     By.CSS_SELECTOR, "#WeaponTable_next")
            # if "disabled" in next_button.get_attribute("class"):
            #     break

            # else:
            #     print(next_button.is_enabled(), "inside if")
            #     driver.execute_script("""
            #  document.querySelector("#WeaponTable_next").click()""")
            # print(allData)


# main("weapon", WEAPONS_CACHE_PATH)


def scrape_item_data():
    test_links = ['https://bdocodex.com/us/item/730706/',
                  'https://bdocodex.com/us/item/13104/', 'https://bdocodex.com/us/item/13105/']
    options = webdriver.ChromeOptions()
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(2)
    driver.get("https://bdocodex.com/us/item/730706/")
    scripts_content = []
    current_enchantment_level = driver.find_element(
        By.CSS_SELECTOR, ".item_info > .card-header > .clearfix > .enchantment_cell > #en_value").text
    increase_enchantment_level_button = driver.find_element(
        By.CSS_SELECTOR, ".item_info > .card-header > .clearfix > .enchantment_cell > .enh_plus")

    icon_image = driver.find_element(
        By.CSS_SELECTOR, ".card-body > table > tbody > tr > td.icon_cell > img")
    image_source = icon_image.get_attribute("src")
    item_grade = icon_image.get_attribute("className").split(" ")[1]

    item_ap = driver.find_element(
        By.CSS_SELECTOR, "span#damage").get_attribute("innerHTML")
    item_defense = driver.find_element(
        By.CSS_SELECTOR, "span#defense").get_attribute("innerHTML")
    item_accuracy = driver.find_element(
        By.CSS_SELECTOR, "span#accuracy").get_attribute("innerHTML")
    item_evasion = driver.find_element(
        By.CSS_SELECTOR, "span#evasion").get_attribute("innerHTML")
    item_hevasion = driver.find_element(
        By.CSS_SELECTOR, "span#hevasion").get_attribute("innerHTML")
    item_dreduction = driver.find_element(
        By.CSS_SELECTOR, "span#dreduction").get_attribute("innerHTML")
    item_hreduction = driver.find_element(
        By.CSS_SELECTOR, "span#hdreduction").get_attribute("innerHTML")
    titles_cell = driver.find_element(
        By.CSS_SELECTOR, ".card-body table tbody tr td.titles_cell")
    titles_cell_text = titles_cell.text
    lines = titles_cell_text.split("\n")
    item_weight = ""
    item_warehouse_capacity = ""
    print(titles_cell_text)
    print(lines)
    for line in lines:
        if "Weight" in line:
            # print(line)
            item_weight = line.split("Weight:")[1].strip()
        elif "Warehouse Capacity:" in line:
            item_warehouse_capacity = line.split(
                "Warehouse Capacity:")[1].strip()

    caphras_enhancement_div = driver.find_element(
        By.CSS_SELECTOR, "#caphras_enhancement")
    table_body_tr_item_effects = driver.find_elements(
        By.CSS_SELECTOR, ".item_info .card-body table tbody tr")[2].text
    effects_line = table_body_tr_item_effects.split("\n")
    # print(effects_line)
    caphras_total = ""
    if caphras_enhancement_div.get_attribute("innerHTML") == "":
        return
    else:

        increase_caphras_button = caphras_enhancement_div.find_element(
            By.CSS_SELECTOR, "#caphras_enhancement .noselect .cenh_plus")
        current_caphras_level = driver.find_element(
            By.ID, "cen_value").get_attribute("innerText")
        # for description in effects_line:
        #     if "Total:" and "- Caphras Stone x" in description:
        #         caphras_total = description.split(" ")
        #         print(description)
        caphras_next_level_value = driver.find_element(
            By.CSS_SELECTOR, "#caphras_value").get_attribute("innerText")
        total_caphras_value = driver.find_element(
            By.CSS_SELECTOR, "#caphras_tvalue").get_attribute("innerText")
        caphras_link = driver.find_element(
            By.CSS_SELECTOR, "#caphras_enhancement .iconset_wrapper_medium a").get_attribute("href")
    item_class = ""
    for i, rows in enumerate(effects_line):
        if "Exclusive:" in rows:
            item_class = rows.split("Exclusive:")[1].strip()
            # print(rows[i+1])
    # print(table_body_tr_item_effects)

    # equipment_spans = driver.find_elements(
    #     By.CSS_SELECTOR, ".card-body > table > tbody > tr > .titles_cell > span")
    # for spans in equipment_spans:
    #     item_attack = spans.find_element(
    #         By.CSS_SELECTOR, ".main_stat > #damage")
    #     print(spans.text, item_attack)

    # script_tags = item_info_header.find_elements(By.TAG_NAME, "script")
    # scripts_content.append(script_tags[0].get_attribute("innerHTML"))
    # for content in script_tags:
    #     scripts_content.append(content.get_attribute("innerHTML"))
    #     # print(content.get_attribute("innerHTML"))
    # t = script_tags[0].get_attribute(
    #     "innerHTML").replace("\\u003C", "<").replace("\\u003E", ">").replace("\\n", "").replace("\\t", "").replace("<br>", "\n").replace("<span style=\"color: #e9bd23\">", "").replace("</span>", "")
    # print(t.split("enchantment_array = "))
    # cleaned_data = clean_enchantment_array(t.split("enchantment_array = "))
    #     script_tags[0].get_attribute("innerHTML"))
    # print(cleaned_data)


# def clean_enchantment_array(enchantment_array):
#     cleaned_array = {}

#     for key, value in enumerate(enchantment_array):
#         print(key, value[10], "inside first loop")


scrape_item_data()
# driver.implicitly_wait(2)
# clicks the Sellable at central market in order to see unique items, and not repeated ones that could be bound, etc.
# print(sellable_item_checkbox.is_selected())
# # text_box = driver.find_element(by=By.NAME, value="my-text")
# # submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

# # first_checkbox = driver.find_element(
# #     by=By.CSS_SELECTOR, value="#my-check-1")
# # first_checkbox.click()
# # c = first_checkbox.is_selected()

# # text_box.send_keys("Selenium")
# # submit_button.click()

# # message = driver.find_element(by=By.ID, value="message")
# # text = message.text

# # print(c)
# driver.quit()
