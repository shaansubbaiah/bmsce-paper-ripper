from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# configuration options
LIBRARY_URL = 'http://103.40.80.24:8080'
USERNAME = 'cse1'
PASSWORD = 'cse1'
SEMESTER = 'Sixth'
BRANCH = 'Computer'
LAST_N_YEARS = 5


links_dict = []


driver = webdriver.Chrome()
driver.get(LIBRARY_URL)


def setLinksTargetToSelf():
    links = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
    )
    for link in links:
        driver.execute_script("arguments[0].target='_self';", link)
    
    return


def addPdfLinksToDict(exam_name, links_dict):
    pdf_links = driver.find_elements_by_partial_link_text('pdf')
    for pdf_link in pdf_links:
            pdf_filename = (exam_name.replace(' ', '_') + '_' + pdf_link.text).strip()
            pdf_link_url = pdf_link.get_attribute('href')

            links_dict.append({pdf_filename: pdf_link_url})

    driver.back()

    return


def ripper():
    username_field = driver.find_element_by_name('loginForm.userName')
    username_field.send_keys(USERNAME)
    
    password_field = driver.find_element_by_name('loginForm.userPassword')
    password_field.send_keys(PASSWORD)
    
    driver.find_element_by_tag_name('button').click()

    driver.get(LIBRARY_URL + '/browse/browseSubCategory?link=YnJvd3Nl&catCode=27283950369')

    categories = driver.find_elements_by_class_name('cat-row-col')

    for category in categories:
        # match SEM from config
        if category.text.find(SEMESTER) > -1:
            print(f"---> Opening {category.text}")
            category.find_element_by_class_name('btn').click()
            
            branches = driver.find_elements_by_class_name('cat-row-col')

            for branch in branches:
                # match BRANCH from config
                if branch.text.find(BRANCH) > -1:
                    print(f"---> Opening {branch.text}")
                    branch.find_element_by_class_name('btn').click()

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
                            exam_link_name = (batch_name + '_' + exam_type.text).strip()
                            exam_link_url = exam_type.get_attribute('href')

                            exam_links.append([exam_link_name, exam_link_url])

                        # iterate through exam type links
                        for exam_link in exam_links:
                            print(f'---> Adding {exam_link[0]} Papers')
                            driver.get(exam_link[1])
                            
                            # add links from the page to the dict
                            addPdfLinksToDict(exam_link[0], links_dict)

                            # sometimes, a second page exists
                            try:
                                secondPageExists = EC.presence_of_element_located((By.CLASS_NAME, 'navigationLink'))

                                if secondPageExists is True:
                                    print('Found 2 pages!')

                                    driver.find_element_by_class_name('navigationLink').click()

                                    addPdfLinksToDict(exam_link[0], links_dict)
                            
                            except:
                                print('Found 1 Page!')
                            
                        driver.back()
                        
                    # exit after processing the branch
                    break
            # exit after processing the batch 
            break

    print(links_dict)
    return

ripper()


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