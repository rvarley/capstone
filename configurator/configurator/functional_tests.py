from selenium import webdriver
import unittest
import time

"""
This functional test should pass 5 test cases.  It is necessary to run the
propel_spider.py scraper to populate the database prior to running these test.
Test was run in a virtual environment with the packages installed as 
per the README.md file for this project. 
"""

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        time.sleep(2)
        self.browser.quit()

    def test_can_go_to_configurator_homepage(self):
        # Sally is interested in purchasing an ebike and heard
        # about a website that can help he make a good purchase decision
        self.browser.get('http://localhost:8000')

        # She noticed the page title reads 'E-bike Configuration Tool'
        self.assertIn('Configurator', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your Source for E-bike Information', header_text)

        # She finds a series of buttons including
        # 'Configure My Bike', 'Build Your Own', 'Off The Shelf', 
        # and 'Legal and Saftey'
        button_text = self.browser.find_element_by_id('configure_my_bike').text
        self.assertIn('Configure My Bike!', button_text)

    def test_can_go_to_form_page(self):
        # She presses the 'Configure My Bike' button and is taken to
        # the questioneer form.
        self.browser.get('http://localhost:8000')
        button_id = self.browser.find_element_by_id('configure_my_bike')
        button_id.click()
        h2_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('What is your budget', h2_text)

    def test_can_go_to_results_page(self):
        # She presses the 'Submit Questionaire' button with the form defaults
        # and is taken to the results page

        self.browser.get('http://localhost:8000/form.html')
        button_id = self.browser.find_element_by_id('submit')
        button_id.click()

        # She sees the results form and it has a section
        # with heading 'Matching Bike Results'
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Matching Bike Results', header_text)

    def test_no_bikes_found_results_page(self):
        # Sally has unreasonable expectations for bike specs
        # and queries for bikes in the 1501 - 2500 with
        # a range of at least 100 miles.
        # The results page shows her 'Query Returned No Matching Bikes'

        self.browser.get('http://localhost:8000/form.html')
        self.browser.find_element_by_xpath\
            ('//*[@id="price"]/select[3]/option[4]').click()
        button_id = self.browser.find_element_by_id('submit')
        button_id.click()

        # She sees the results form and it has a section
        # with heading 'Matching Bike Results'
        # header_text = self.browser.find_element_by_tag_name('h2').text
        button_text = self.browser.find_element_by_xpath\
            ('//*[@id="configurator"]').text
        self.assertIn('Query returned no matching bikes.', button_text)

        # She clicks the button and is returned to the form page so she
        # can make more reasonable choices.
        button_id = self.browser.find_element_by_xpath\
            ('//*[@id="configurator"]')
        button_id.click()
        h2_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('What is your budget', h2_text)

    def test_can_go_to_bike_details_page(self):
        # She leaves the default answers on the form and clicks the submit
        # button.
        self.browser.get('http://localhost:8000/form.html')
        button_id = self.browser.find_element_by_id('submit')
        button_id.click()

        # She is presented with a list of bikes and selects the button
        # for the first bike on the list.  She is taken to the bike details
        # page
        button_id = self.browser.find_element_by_xpath\
            ('//*[@id="results_table"]/tbody/tr[2]/td[1]/form/input[1]')
        button_id.click()

        # She sees a table of bike details for the selected model.
        # The first row lists the supplier website.
        table_text = self.browser.find_element_by_xpath\
            ('//*[@id="results_table"]/tbody/tr[1]/td[1]').text
        self.assertIn('Supplier Website', table_text)

        # She decides to return to the results page by clicking the
        # "Return to Results Page" button
        button_id = self.browser.find_element_by_xpath\
            ('//*[@id="configurator"]')
        button_id.click()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
