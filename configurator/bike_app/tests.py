from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from bike_app.views import home_page, form_page, submit_response, bike_details

"""
Make sure a virtual to run in a virtual
environment as described in the README.md file for this project.
To run unit tests, navigate to directory containing manage.py
and run 'python manage.py test'.  Six tests should pass.
"""


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        # Check for presence of correct buttons on home page
        self.assertIn(b'Configure My Bike!', response.content)
        self.assertIn(b'Safety Considerations', response.content)
        self.assertIn(b'E-Bike Technologies', response.content)
        self.assertIn(b'What Features Do I Need?', response.content)


class FormPageTest(TestCase):

    def test_form_url_resolves_to_form_page_view(self):
        found = resolve('/form')
        self.assertEqual(found.func, form_page)

    def test_form_page_returns_correct_html(self):
        request = HttpRequest()
        response = form_page(request)
        # Check all form questions and submit button are present
        self.assertIn(b'What is your budget?', response.content)
        self.assertIn(b'What your primary use for the bike?', response.content)
        self.assertIn(b'What are the maximum number of miles you will travel between recharging?', response.content)
        self.assertIn(b'Submit Questionaire', response.content)


class ResultsPageTest(TestCase):

    def test_form_url_resolves_to_submit_response_view(self):
        found = resolve('/results')
        self.assertEqual(found.func, submit_response)


class BikeDetailsPageTest(TestCase):

    def test_form_url_resolves_to_bike_details_view(self):
        found = resolve('/bike_details')
        self.assertEqual(found.func, bike_details)
