from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
import os
import re

# ░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀
# ░█░░░█░█░█░█░█▀▀░░█░░█░█
# ░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀

# configuration options
# see valid config in the README/ bottom of this file
LIBRARY_URL = 'http://103.40.80.24:8080'
USERNAME = 'cse1'
PASSWORD = 'cse1'
SEMESTER = 'SIXTH SEMESTER'
BRANCH = 'COMPUTER SCIENCE'
# 3 letter course short code eg.'TFC' for 16CS6DCTFC.pdf
# Leave empty to rip papers for every course 
COURSE = ''
LAST_N_YEARS = 2

# set webdriver to browser you intend to run this on
driver = webdriver.Chrome()
# driver = webdriver.Firefox()


# ░█▀▄░▀█▀░█▀█░█▀█░█▀▀░█▀▄
# ░█▀▄░░█░░█▀▀░█▀▀░█▀▀░█▀▄
# ░▀░▀░▀▀▀░▀░░░▀░░░▀▀▀░▀░▀


def setLinksTargetToSelf():
    links = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
    )
    for link in links:
        driver.execute_script("arguments[0].target='_self';", link)
    
    return


def addPdfLinksToList(exam_name, links_list, course_code):
    pdf_links = driver.find_elements_by_partial_link_text(f'{course_code}.pdf')
    for pdf_link in pdf_links:
        pdf_filename = (exam_name + '_' + pdf_link.text).strip().replace(' ', '_')
        pdf_link_url = pdf_link.get_attribute('href')

        links_list.append([pdf_filename, pdf_link_url])
    return


def screamErrorAndQuit(msg):
    print(f'ERROR: {msg}')
    driver.quit()
    exit(1)


def ripper():
    links_list = []

    driver.get(LIBRARY_URL)

    username_field = driver.find_element_by_name('loginForm.userName')
    username_field.send_keys(USERNAME)
    
    password_field = driver.find_element_by_name('loginForm.userPassword')
    password_field.send_keys(PASSWORD)
    
    driver.find_element_by_tag_name('button').click()

    # check if login was succesful
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "logout"))
        )
    except:
        screamErrorAndQuit('login details are incorrect!')


    driver.get(LIBRARY_URL + '/browse/browseSubCategory?link=YnJvd3Nl&catCode=27283950369')

    try:
        semester_category = driver.find_element_by_partial_link_text(SEMESTER)
        print(f"---> Opening {semester_category.text}")
        semester_category.click()
        
        try:
            branch_category = driver.find_element_by_partial_link_text(BRANCH)
            print(f"---> Opening {branch_category.text}")
            branch_category.click()

            # find batch divs eg. '2019 and 2020', '2018 and 2019', etc
            batches = driver.find_elements_by_class_name('cat-row-col')
            batches = reversed(batches)

            # save last N years batches links
            batch_links = []
            for batch, _ in zip(batches, range(LAST_N_YEARS)):
                batch_btn = batch.find_element_by_class_name('btn')
                batch_links.append(batch_btn.get_attribute('href'))

            # iterate through last N years batches links
            for batch_link in batch_links:
                driver.get(batch_link)
                
                # extract batch name from the breadcrumb
                breadcrumb = driver.find_element_by_css_selector('li.active')
                batch_name = breadcrumb.text.replace(' ', '_').strip()

                # prevent links from opening in new tabs
                setLinksTargetToSelf()

                # exams -> main, supplementary, makeup, etc
                exams = driver.find_elements_by_class_name('cat-row-col')

                # save different exam type links
                exam_links = []
                for exam in exams:
                    exam_type = exam.find_element_by_xpath('./div/div/div[2]/div/h2/a')
                    exam_link_url = exam_type.get_attribute('href')

                    # minimize batch name '2018 AND 2019' to '2018-19'
                    batch_name = (batch_name[:4] + '-' + batch_name[-2:]).strip()
                    # minimize exam name 'SEMESTER_END_MAIN_EXAMINATION' to 'MAIN'
                    exam_type_name = exam_type.text.replace('SEMESTER END', '').replace('EXAMINATIONS', '').strip()
                    
                    exam_link_name = (batch_name + '_' + exam_type_name).replace(' ', '_')

                    exam_links.append([exam_link_name, exam_link_url])

                # iterate through exam type links
                for exam_link in exam_links:
                    print(f'------> Adding {exam_link[0]} Papers')
                    driver.get(exam_link[1])

                    try:
                        pagination_exists = driver.find_element_by_class_name('pagination')
                        pagination_exists = True
                    except:
                        pagination_exists = False

                    cur_page = 1

                    # add links from the first page
                    print(f'---------> page {cur_page}', end =" ")
                    addPdfLinksToList(exam_link[0], links_list, COURSE)
                    
                    # if pagination exists, iterate, add links from the other pages
                    if pagination_exists:
                        while(True):
                            cur_page += 1
                            try:
                                next_page = driver.find_element_by_link_text(str(cur_page))
                                next_page.click()

                                print(cur_page, end =" ")

                                addPdfLinksToList(exam_link[0], links_list, COURSE)
                            except:
                                break
                    print('')
                    # no need to go back a page, urls to the exam types are saved
                    # above, we directly go to them
                    
                # go back to the list of batches
                driver.back()

        except:
            screamErrorAndQuit(f'Could not find branch matching \"{BRANCH}\"!')
        
    except:
        screamErrorAndQuit(f'Could not find semester matching \"{SEMESTER}\"!')
    
    # return cookies to prevent session expiration errors
    # here, only the jsession id is required
    cookies = driver.get_cookies()
    jsession_id = cookies[0]['value']

    driver.quit()

    return links_list, jsession_id


def getPublicLinks(data, session_id):
    print("---> Extracting PUBLIC LINKS")

    cookies = {'JSESSIONID': session_id}

    # e[0] -> file name, e[1] -> non public file url
    for e in data:
        r = requests.get(e[1], cookies=cookies)
        
        # obtain public link from response
        public_links = re.findall(r'http.+\.pdf', r.text)

        # replace non-public with public link
        e[1] = public_links[0]

    return data


def exportToCSV(data):
    print("---> Exporting CSV")

    with open('pdf_links.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for e in data:
            csv_writer.writerow(e)
    
    return


def downloadPdfFiles(data):
    print("---> Downloading PDFs")
    
    dir = os.path.dirname(__file__)

    download_dir = os.path.join(dir, 'ripped_pdfs')
    os.makedirs(download_dir, exist_ok=True)

    # e[0] -> file name, e[1] -> file url
    for e in data:
        # extract subject/folder name from filename
        # '2018-19_MAIN_EXAMINATION_16IS6DCCNS.pdf' to 'CNS'
        folder_name = e[0][-7:-4]
        download_path = os.path.join(download_dir, folder_name)
        
        # make the subject folder if it doesnt exist already
        os.makedirs(download_path, exist_ok=True)
        
        filename = os.path.join(download_path, e[0])

        r = requests.get(e[1])
        with open(filename, 'wb') as f:
            f.write(r.content)

    return


def main():
    print("Starting Ripper")

    data, session_id = ripper()

    # Turns out the file link obtained from ripper() redirects to
    # another page with the public file link (which does not require
    # an authenticated session)
    # This function extracts the public urls before saving to CSV
    public_link_data = getPublicLinks(data, session_id)

    exportToCSV(public_link_data) 

    downloadPdfFiles(public_link_data)

    print("Ripped. 💀")


if __name__ == "__main__":
    main()


# ░█▀▀░█░█░▀█▀░█▀▄░█▀█
# ░█▀▀░▄▀▄░░█░░█▀▄░█▀█
# ░▀▀▀░▀░▀░░▀░░▀░▀░▀░▀

### Valid branch parameters:
# ARCHITECTURE
# BIOTECHNOLOGY
# CHEMICAL ENGINEERING
# CIVIL ENGINEERING
# COMPUTER SCIENCE AND INFORMATION SCIENCE
# ELECTRICAL AND ELECTRONIC ENGINEERING
# ELECTRONICS AND COMMUNICATION ENGINEERING
# INDUSTRIAL ENGINEERING AND MANAGEMENT
# INSTRUMENTATION ENGINEERING
# MECHANICAL ENGINEERING
# MEDICAL ELECTRONICS
# TELECOMMUNICATION ENGINEERING

### Valid semester parameters:
# FIRST SEMESTER
# SECOND SEMESTER
# THIRD SEMESTER
# FOURTH SEMESTER
# FIFTH SEMESTER
# SIXTH SEMESTER
# SEVENTH SEMESTER
# EIGHT SEMESTER

### UNSUPPORTED semester parameters:
# MATHEMATICS QUESTION PAPERS
# MBA QUESTION PAPERS
# MCA AUTONOMOUS QUESTION PAPERS
# MCA VTU Question Papers
# M.Tech QUESTION PAPERS