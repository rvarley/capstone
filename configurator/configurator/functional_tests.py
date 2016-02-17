from selenium import webdriver
from selenium import selenium
import unittest
import time
import re


"""
This functional test should pass 5 test cases.  It is necessary to run the
propel_spider.py scraper to populate the database prior to running these test.
Test was run in a virtual environment with the packages installed as
per the README.md file for this project.
"""


class NewVisitorTest(unittest.TestCase):
    """ 
    doc string test 
    """

    def go_home(self):
        """ 
        doc string test 
        """
        self.browser.get('http://localhost:8000')

    def go_form(self):
        self.browser.get('http://localhost:8000/form.html')

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        time.sleep(3)
        self.browser.quit()

    def test_can_go_to_configurator_homepage(self):
        # Sally is interested in purchasing an ebike and heard
        # about a website that can help he make a good purchase decision
        self.browser.get('http://localhost:8000')

        # She noticed the page title reads 'E-bike Configuration Tool'
        self.assertIn('Configurator', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Your Source for E-bike Information', header_text)

        # She finds a series of buttons including
        # 'Configure My Bike', 'Build Your Own', 'Off The Shelf',
        # and 'Legal and Saftey'
        button_text = self.browser.find_element_by_id('configure_my_bike').text
        self.assertIn('Configure My Bike!', button_text)

    def test_home_page_footer_buttons(self):
        """
        # Make sure all 3 footer buttons on home page work correctly
        """

        NewVisitorTest.go_home(self)
        self.browser.find_element_by_xpath('//*[@id="safety"]').click()
        safety_text = self.browser.find_element_by_xpath('/html/body/div/div/div[3]/h3').text
        self.assertIn('On Going Safety Precautions', safety_text)
        NewVisitorTest.go_home(self)
        self.browser.find_element_by_xpath('//*[@id="technology"]').click()
        tech_text = self.browser.find_element_by_xpath('/html/body/div/div/div[3]/h1').text
        self.assertIn('E-Bike Technology', tech_text)
        NewVisitorTest.go_home(self)
        self.browser.find_element_by_xpath('//*[@id="features"]').click()
        time.sleep(1)
        equipment_text = self.browser.find_element_by_xpath('/html/body/div/div/div[3]/h1').text
        self.assertIn('Additional Equipment', equipment_text)

    def test_form_page_menus(self):
        """
        Test menu options on form page
        Go to from page
        """

        NewVisitorTest.go_form(self)
        h2_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('What is your budget', h2_text)

        # Find home menu option on form pate and verify it goes back to home page
        menu_choice = self.browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[1]/a')
        time.sleep(1)
        menu_choice.click()
        button_text = self.browser.find_element_by_id('configure_my_bike').text
        self.assertIn('Configure My Bike!', button_text)

        # Find contact menu option and make sure it goes to contact page
        NewVisitorTest.go_form(self)
        menu_choice = self.browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[2]/a')
        time.sleep(1)
        menu_choice.click()
        contact_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Contact Form', contact_text)

    def test_form_page_form(self):
        """
        Tests for form drop down menu options
        Best Use 'Comfort Cruiser'
        """

        NewVisitorTest.go_form(self)
        self.browser.find_element_by_xpath('//*[@id="price"]/select[2]/option[2]').click()
        self.browser.find_element_by_id('submit').click()

        # Click on first bike in the results table and make sure the results
        # table lists 'Comfort and Cruiser' in 'Best Use' row
        # This test requires a bike the meets search criteria in database
        self.browser.find_element_by_xpath('//*[@id="results_table"]/tbody/tr[2]/td[1]/form/input[1]').click()
        best_use = self.browser.find_element_by_xpath('//*[@id="results_table"]/tbody/tr[2]/td[2]').text
        self.assertIn('Comfort Cruiser', best_use)

        # Find and click button to return to results page
        self.browser.find_element_by_xpath('//*[@id="configurator"]').click()

        # Select Budget '2501 - 3500' and Best Use 'Cargo & Hauling'
        # Test all price drop downs work

    def test_form_page_form_1(self):
        """
        Test to go to each price point and make sure all the rows in the
        table contain bikes in the correct price range as specified
        on the form page
        """

        prices = {1:1501, 2:2501, 3:3501, 4:4501}
        # for loop to check each price range
        for x in range(1,5):
            # xpath = "'" + "//*[@id=\"price\"]/select[1]/option[" + str(i) + "]" + "'"
            xpath = "//*[@id=\"price\"]/select[1]/option[" + str(x) + "]"
            print("value of xpath is: ", xpath)
            NewVisitorTest.go_form(self)
            self.browser.find_element_by_xpath(xpath).click()

        # Click Submit button to load results page
            self.browser.find_element_by_id('submit').click()
            # Count the number of rows on the resulting page
            # If rows are > 0, check each row for the correct price
            rows = len(self.browser.find_elements_by_xpath('//*[@id="results_table"]/tbody/tr'))
            print('table rowCount is ', rows)
            if rows > 0:  # Don't do this check if query returned no bikes
                for i in range(2, rows):
                    price = self.browser.find_element_by_xpath('//*[@id="results_table"]/tbody/tr[2]/td[2]')
                    print("price found is{}.  min price range is {} ".format(price.text, prices[x]))
                    print("The value of x is: ", x)
                    self.assertGreaterEqual(float(price.text), prices[x])
                    if x == 4:
                        y = 5000
                    else:
                        y = 999
                    self.assertLessEqual(float(price.text), (prices[x] + y) )
                    time.sleep(1)


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
