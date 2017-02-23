from selenium import webdriver

driver = webdriver.Firefox()

def login():
    login_info = open("./login.txt").read()
    login_info = login_info.strip()
    base_url = 'https://' + login_info + '@itp.nyu.edu/projects/thesisProjects.php?venue_id=73&list=quick&instructor='
    driver.get(base_url)
    alert = driver.switch_to_alert()
    alert.accept()

login()
