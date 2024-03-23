import time

from selenium import webdriver
from selenium.webdriver.common.by import By


browser = webdriver.Chrome(executable_path='../chromedriver')

homepage = "https://scholar.google.com/citations?hl=en&user=1kIvpVQAAAAJ&view_op=list_works&sortby=pubdate"

browser.get(homepage)
start = input('Please manually expand the publication list and press Enter to continue.')
# if start is a int, then it is the number of the publication to start with
try:
    start = int(start)
except ValueError:
    start = 0

# document.getElementsByClassName('gsc_a_tr')

publications = browser.find_elements(by=By.CLASS_NAME, value='gsc_a_tr')

for publication in publications[start:]:
    title_box = publication.find_element(by=By.CLASS_NAME, value='gsc_a_t')
    link = title_box.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
    # open link in new tab
    browser.execute_script(f"window.open('{link}', '_blank')")
    # switch to new tab
    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(1)

    # get title, authors, publication date, and venue
    title = browser.find_element(by=By.ID, value='gsc_oci_title').text
    print(title)

    fields = browser.find_elements(by=By.CLASS_NAME, value='gs_scl')
    for field in fields:
        field_name = field.find_element(by=By.CLASS_NAME, value='gsc_oci_field').text
        field_value = field.find_element(by=By.CLASS_NAME, value='gsc_oci_value').text
        if field_name in ['Authors', 'Publication date', 'Journal', 'Conference']:
            print(f'{field_name}: {field_value}')

    print()

    # close tab
    browser.close()
    # switch back to original tab
    browser.switch_to.window(browser.window_handles[0])


browser.quit()
