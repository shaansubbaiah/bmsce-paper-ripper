from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
import os
import re
from time import time as timer
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed

# ░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀
# ░█░░░█░█░█░█░█▀▀░░█░░█░█
# ░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀

# configuration options
# see valid config in the README/ bottom of this file
LIBRARY_URL = 'http://103.40.80.24:8080'
USERNAME = 'cse1'
PASSWORD = 'cse1'
SEMESTER = 'FIFTH SEMESTER'
BRANCH = 'COMPUTER SCIENCE'
# 3 letter course short code eg.'TFC' for 16CS6DCTFC.pdf
# Leave empty to rip papers for every course
COURSE = ''
LAST_N_YEARS = 3

# Enable to include the entire course name in the files and folder
LONG_FILE_NAMES = True

# set webdriver to browser you intend to run this on
driver = webdriver.Chrome(executable_path='chromedriver')
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
    # function returns a dict where key(pdf file name) corresponds to value(pdf url and folder name)
    table_rows = driver.find_elements_by_xpath('//*[@id="tab1"]/tbody/tr')

    for table_row in table_rows:
        table_columns = table_row.find_elements_by_tag_name('td')

        course_name = table_columns[2].text.strip().replace(
            ' ', '_').replace('.', '')
        course_code = table_columns[4].text.strip().replace(
            ' ', '').replace('_', '')[:-4]
        folder_name = '_'.join([course_code, course_name])
        pdf_filename = '_'.join([exam_name, course_name, course_code])

        pdf_link_url = table_columns[4].find_element_by_tag_name(
            'a').get_attribute('href')

        links_list[pdf_filename] = [pdf_link_url, folder_name]

    return links_list


def screamErrorAndQuit(msg):
    print(f'ERROR: {msg}')
    driver.quit()
    exit(1)


def ripper():
    links_list = {}

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

    driver.get(LIBRARY_URL +
               '/browse/browseSubCategory?link=YnJvd3Nl&catCode=27283950369')

    try:
        semester_category = driver.find_element_by_partial_link_text(SEMESTER)
        print(f"Opening {semester_category.text}")
        semester_category.click()

        try:
            branch_category = driver.find_element_by_partial_link_text(BRANCH)
            print(f"Opening {branch_category.text}")
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
                    exam_type = exam.find_element_by_xpath(
                        './div/div/div[2]/div/h2/a')
                    exam_link_url = exam_type.get_attribute('href')

                    # minimize batch name '2018 AND 2019' to '2018-19'
                    batch_name = (batch_name[:4] +
                                  '-' + batch_name[-2:]).strip()
                    # minimize exam name 'SEMESTER_END_MAIN_EXAMINATION' to 'MAIN'
                    exam_type_name = exam_type.text.replace(
                        'SEMESTER END', '').replace('EXAMINATIONS', '').strip()

                    exam_link_name = (batch_name + '_' +
                                      exam_type_name).replace(' ', '_')

                    exam_links.append([exam_link_name, exam_link_url])

                # iterate through exam type links
                for exam_link in exam_links:
                    print(f'·· Adding {exam_link[0]} Papers')
                    driver.get(exam_link[1])

                    try:
                        pagination_exists = driver.find_element_by_class_name(
                            'pagination')
                        pagination_exists = True
                    except:
                        pagination_exists = False

                    cur_page = 1

                    # add links from the first page
                    print(f'   ·· pages found: {cur_page}', end="")
                    addPdfLinksToList(exam_link[0], links_list, COURSE)

                    # if pagination exists, iterate, add links from the other pages
                    if pagination_exists:
                        while(True):
                            cur_page += 1
                            try:
                                next_page = driver.find_element_by_link_text(
                                    str(cur_page))
                                next_page.click()

                                print(",", cur_page, end=" ")

                                addPdfLinksToList(
                                    exam_link[0], links_list, COURSE)
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


def extractPublicLink(file_name, file_url, folder_name, cookies):
    # Function doesn't need all the passed variables but it makes tracking
    # the finished threads easier

    r = requests.get(file_url, cookies=cookies)

    # obtain public link from response
    public_links = re.findall(r'http.+\.pdf', r.text)
    public_file_url = public_links[0]

    return {file_name: [public_file_url, folder_name]}


def convertToPublicLinks(data, session_id):
    s_c = timer()

    cookies = {'JSESSIONID': session_id}
    print("Using Extracted Cookie ", session_id[:-6]+'XXXXXX')
    print("Extracting PUBLIC LINKS")

    public_data = {}
    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = []
        for e in data:
            # e -> file name, data[e][0] -> file url, data[e][1] -> folder name to store it
            futures.append(executor.submit(
                extractPublicLink, e, data[e][0], data[e][1], cookies))

        for future in as_completed(futures):
            public_data.update(future.result())

    print(f"   ·· took {(timer() - s_c):4.3f}s")

    return public_data


def exportToCSV(data):
    print("Exporting CSV")

    with open('pdf_links.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for e in data:
            # e -> file name, data[e][0] -> file url, data[e][1] -> folder name to store it
            csv_writer.writerow([e, data[e][0]])

    return


def downloadFile(file_name, file_url, folder_name, download_dir):
    download_path = os.path.join(download_dir, folder_name)

    # make the subject folder if it doesnt exist already
    os.makedirs(download_path, exist_ok=True)

    filename = os.path.join(download_path, file_name)

    r = requests.get(file_url)
    with open(filename+'.pdf', 'wb') as f:
        f.write(r.content)

    return


def downloadPdfFiles(data):
    s_d = timer()
    print("Downloading PDFs")

    dir = os.path.dirname(__file__)
    download_dir = os.path.join(dir, 'RIPPED_PAPERS')
    os.makedirs(download_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = []
        # e -> file name, data[e][0] -> file url, data[e][1] -> folder name to store it
        for e in data:
            futures.append(executor.submit(
                downloadFile, e, data[e][0], data[e][1], download_dir))

    print(f"   ·· took {(timer() - s_d):4.3f}s")
    return


def main():
    s_m = timer()
    print("Starting Ripper")

    data, session_id = ripper()

    # Turns out the file link obtained from ripper() redirects to
    # another page with the public file link (which does not require
    # an authenticated session)
    # This function extracts the public urls before saving to CSV
    public_link_data = convertToPublicLinks(data, session_id)

    exportToCSV(public_link_data)

    downloadPdfFiles(public_link_data)

    print(f'💀 Ripped {len(public_link_data)} files. \
        \nTook {(timer() - s_m):4.3f}s.')


if __name__ == "__main__":
    main()


# ░█▀▀░█░█░▀█▀░█▀▄░█▀█
# ░█▀▀░▄▀▄░░█░░█▀▄░█▀█
# ░▀▀▀░▀░▀░░▀░░▀░▀░▀░▀

# Valid branch parameters:
# ARCHITECTURE
# BIOTECHNOLOGY
# CHEMICAL ENGINEERING
# CIVIL ENGINEERING
# COMPUTER SCIENCE
# INFORMATION SCIENCE
# ELECTRICAL AND ELECTRONIC ENGINEERING
# ELECTRONICS AND COMMUNICATION ENGINEERING
# INDUSTRIAL ENGINEERING AND MANAGEMENT
# INSTRUMENTATION ENGINEERING
# MECHANICAL ENGINEERING
# MEDICAL ELECTRONICS
# TELECOMMUNICATION ENGINEERING

# Valid semester parameters:
# FIRST SEMESTER
# SECOND SEMESTER
# THIRD SEMESTER
# FOURTH SEMESTER
# FIFTH SEMESTER
# SIXTH SEMESTER
# SEVENTH SEMESTER
# EIGHT SEMESTER

# UNSUPPORTED semester parameters:
# MATHEMATICS QUESTION PAPERS
# MBA QUESTION PAPERS
# MCA AUTONOMOUS QUESTION PAPERS
# MCA VTU Question Papers
# M.Tech QUESTION PAPERS
