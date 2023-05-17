import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://dnevnik.ru/soc/tests/results.aspx?view=results&test=683136&context=school&page=1')

login_dnevnik = driver.find_element(By.CLASS_NAME, "login__body__input_login")
login_dnevnik.send_keys("login")

password_dnevnik = driver.find_element(By.CLASS_NAME, "login__body__input_password")
password_dnevnik.send_keys("password")

driver.find_element(By.CLASS_NAME, "login__submit").click()
time.sleep(1)
driver.find_element(By.CLASS_NAME, "login__pubservices-link_login").click()

login_gosuslugi = driver.find_element(By.NAME, "login")
login_gosuslugi.send_keys("phone")

password_gosuslugi = driver.find_element(By.NAME, "password")
password_gosuslugi.send_keys("password")

driver.find_element(By.CLASS_NAME, "ui-button-text").click()

time.sleep(5)
driver.find_element(By.NAME, "fmyschool").click()

participant_score = int(driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[4]/div[4]/div/table/tbody/tr[last()]/td[1]/span").get_attribute("innerHTML").replace(' ', '').replace('/n', ''))
m = []
pages = int(driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[4]/div[5]/div/div/ul/li[last()]/a").get_attribute("innerHTML")) + 1

for page in range(1, pages):
    link = f'https://dnevnik.ru/soc/tests/results.aspx?view=results&test=683136&context=school&page={page}'
    driver.get(link)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[3]/div/ul/li[2]/form/input").click()
    for i in range(2, participant_score + 2):
        try:
            a = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[4]/div[4]/div/table/tbody/tr[{i}]/td[7]/a").get_attribute("href")
            driver.get(a)
            b = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[4]/div[4]/div/table/tbody/tr[2]/td[4]/span").get_attribute("innerHTML")
            m.append(b)
            driver.get(link)
            driver.find_element(By.NAME, "fmyschool").click()
        except selenium.common.exceptions.NoSuchElementException:
            break

print(f'10а - {m.count("1")} г.\n'
      f'11а - {m.count("2")} г.\n'
      f'11б - {m.count("3")} г.\n'
      f'Всего голосов - {len(m)} шт.\n'
      f'Из них аннулировано за некорректный ответ: {len(m) - (m.count("1") + m.count("2") + m.count("3"))}')
