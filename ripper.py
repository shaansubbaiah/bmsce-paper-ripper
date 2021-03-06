from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get('http://103.40.80.24:8080')


links_dict = []


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

            # print(f'Added {pdf_filename}: {pdf_link_url}')
            links_dict.append({pdf_filename: pdf_link_url})

    driver.back()

    return


def login():
    username_field = driver.find_element_by_name('loginForm.userName')
    username_field.send_keys('cse1')
    
    password_field = driver.find_element_by_name('loginForm.userPassword')
    password_field.send_keys('cse1')
    
    driver.find_element_by_tag_name('button').click()

    driver.get('http://103.40.80.24:8080/browse/browseSubCategory?link=YnJvd3Nl&catCode=27283950369')

    categories = driver.find_elements_by_class_name('cat-row-col')

    for category in categories:
        print(category.text)
        # match SEM query
        if category.text.find("SIXTH") > -1:
            print(f"---{category.text}---")
            category.find_element_by_class_name('btn').click()
            
            branches = driver.find_elements_by_class_name('cat-row-col')

            for branch in branches:
                print(branch.text)
                # match BRANCH
                if branch.text.find("COMPUTER") > -1:
                    print(f"---{branch.text}---")
                    branch.find_element_by_class_name('btn').click()

                    batches = driver.find_elements_by_class_name('cat-row-col')

                    # fetch last N years papers
                    LAST_N_YEARS = 5
                    for batch in reversed(batches):
                        for i in range(LAST_N_YEARS + 1):
                            batch.find_element_by_class_name('btn').click()
                            
                            breadcrumb = driver.find_element_by_css_selector('li.active')
                            batch_name = breadcrumb.text.replace(' ', '_').strip()

                            setLinksTargetToSelf()

                            # exams -> main, supplementary, makeup, etc
                            exams = driver.find_elements_by_class_name('cat-row-col')

                            for exam in exams:
                                exam_type = exam.find_element_by_xpath('./div/div/div[2]/div/h2/a')
                                exam_name = (batch_name + exam_type.text).strip()
                                print(f'Adding {exam_name} Papers')
                                
                                driver.get(exam_type.get_attribute('href'))
                                
                                # add links from the page to the dict
                                addPdfLinksToDict(exam_name, links_dict)

                                # sometimes, a second page exists
                                try:
                                    secondPageExists = EC.presence_of_element_located((By.CLASS_NAME, 'navigationLink'))

                                    if secondPageExists is True:
                                        print('Found 2 pages!')

                                        driver.find_element_by_class_name('navigationLink').click()

                                        addPdfLinksToDict(exam_name, links_dict)
                                
                                except:
                                    print('Found 1 Page!')
                                

                            print(links_dict)
                                                          
                            # driver.implicitly_wait(3)
                            driver.back()
                        

                    break
 
            break
    
    return

login()