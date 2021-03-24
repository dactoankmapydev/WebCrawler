#Import the packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

import requests
from bs4 import BeautifulSoup
import array as arr
import pandas
#The first line import the Web Driver, and the second import Chrome Options
#-----------------------------------#
#Chrome Options
all_link = []
content = []
name_job = []
name_company = []
name_location = []
salary = []
all_salary = []
expiry = []
upload_date = []
position = []
career = []
skill = []
language_of_cv = []
detail_address = []
number_employees = []



chrome_options = Options()
chrome_options.add_argument ('--ignore-certificate-errors')
chrome_options.add_argument ("--igcognito")
chrome_options.add_argument ("--window-size=1920x1080")
chrome_options.add_argument ('--headless')
#-----------------------------------#

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/webdriver/chromedriver.exe")

#Open log-in url
driver.get("https://secure.vietnamworks.com/login/vi?client_id=3") 
driver.maximize_window()

#Time-wait
time.sleep(5)

#Fill the log-in information
driver.find_element_by_id("email").send_keys("luongdg.bi9159@st.usth.edu.vn") #PUT YOUR EMAIL HERE
driver.find_element_by_id('login__password').send_keys('Conanpro123')         #PUT YOUR PASSWORD HERE
driver.find_element_by_id("button-login").click()


#Open url




url = 'https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam'
driver.get(url)


page_source = driver.page_source
soup = BeautifulSoup(page_source,"html.parser")

page_num = 1

while True:

    #insert the scrapping code to scrape this page
    #.....
    #.....
    

    block_job_list = soup.find_all("div",{"class":"block-job-list"})
    for i in block_job_list:
        link_catalogue = i.find_all("div",{"class":"col-12 col-lg-8 col-xl-8 p-0 wrap-new"})
        for j in link_catalogue:
            link = j.find("a")
            all_link.append("https://www.vietnamworks.com" + link.get("href"))
        salary_catalogue = i.find_all("div",{"class":"col-12 col-lg-4 col-xl-4 p-0 col-salary"})
        for j in salary_catalogue:
            salary = j.find("span")
            all_salary.append(salary.text.replace("\n","").strip())

    #moving to next page

    a = driver.find_elements_by_class_name('page-link')    #Finds the pages list in the bottom of the page

    if page_num ==1:
        a[2].click()
        page_num +=1

    elif page_num >=2 and page_num <=4:
        a[4].click()
        page_num+=1

    elif page_num >4 and len(a)<7:
        print('End of page')
        break

    else:
        print('yes')
        a[6].click()
        page_num+=1
    time.sleep(3)

driver.quit()

# print("\n".join(all_link))
# print(len(all_link))

for i in all_link:
    page = requests.get(i)
    soup = BeautifulSoup(page.content,"html.parser")
    name_job.append(soup.find("h1",{"class":"job-title"}).text.replace("\n","").strip())

    name_company.append(soup.find("div",{"class","company-name"}).text.replace("\n","").strip())

    name_location.append(soup.find("span",{"class":"company-location"}).text.replace("\n","").strip())

    expiry.append(soup.find("span",{"class":"expiry gray-light"}).text.replace("\n","").strip())

    information = soup.find_all("div",{"class":"row summary-item"})
    for i in information:
        content.append(i.find("span",{"class":"content"}).text.replace('\xa0','').replace('\n', '').replace('  ',"").strip())

    upload_date.append(content[0])
    position.append(content[1])
    career.append(content[2])
    skill.append(content[3])
    language_of_cv.append(content[4])
    detail_address.append(content[5])
    number_employees.append(content[6])
    
    content =[]


data = {
   "Name": name_job,
   "Salary": all_salary,
   "Upload date": upload_date,
   "Locations": name_location,
   "Skill": skill,
   "Career": career,
   "Company": name_company,
   "Job position": position,
   "Number employees": number_employees,
   "Detail address": detail_address,
   "Language of cv": language_of_cv,
   "Link job" : all_link,   
}
df = pandas.DataFrame(data)
df.to_csv( r'Vietnamworks.csv', index = False)
