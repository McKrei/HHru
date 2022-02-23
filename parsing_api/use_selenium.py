from selenium import webdriver
import time

def update_ip_address():
    driver = webdriver.Firefox(executable_path='C:\\my\\Python_project\\hh\\geckodriver.exe')
    url = "http://192.168.1.1/quick_menu.htm"
    driver.get(url=url)
    time.sleep(5)

    try: 
        login_input = driver.find_element_by_name('login_name')
        login_input.clear()
        login_input.send_keys('admin')
        time.sleep(3)
        pasword_input = driver.find_element_by_name('login_pwd')
        pasword_input.clear()
        pasword_input.send_keys('admin')
        time.sleep(3)
        resume_click = driver.find_element_by_class_name('btn_auth_01').click()
    except Exception:
        pass

    tuch_setting = driver.find_element_by_id("id_index_btn").click()
    time.sleep(3)
    reset_button = driver.find_element_by_name("wan2_ppp_restart").click()
    time.sleep(1)
    unplug_button = driver.find_element_by_name("wan2_ppp_release").click()
    time.sleep(1)
    apply_button = driver.find_element_by_link_text('Применить').click()
    time.sleep(1)
    reset_button = driver.find_element_by_name("wan2_ppp_restart").click()
    time.sleep(60)
    driver.close()
    driver.quit()
    print('Сменил IP')