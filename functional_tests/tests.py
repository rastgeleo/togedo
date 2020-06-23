import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_name_in_list_contents(self, text):
        start_time = time.time()
        while True:
            try:
                contents = self.browser.find_elements_by_class_name('content')
                self.assertIn(text, [content.text for content in contents])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):

        # check out homepage
        self.browser.get(self.live_server_url)

        # page title and header mention to-do list
        self.assertIn('Togedo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('TODO LISTS', header_text)

        # press add list button to start a new list
        new_list_link = self.browser.find_element_by_id('id_new_list')
        new_list_link.click()
        time.sleep(3)

        # move to the create_list page
        new_list_add_url = self.browser.current_url
        self.assertEqual(
            new_list_add_url,
            self.live_server_url + reverse('todo:tasklist_create'))

        # Enter a new list name and start a new list
        input_box = self.browser.find_element_by_id('id_name')
        input_box.send_keys('Shopping list')
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # page redirect to the newly created list page and
        # the list name is shown.
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Shopping list')

        # There is a button to add a new task and when clicked,
        # a user taken to task adding page.

        add_task_link = self.browser.find_element_by_id('id_new_task')
        add_task_link.click()
        time.sleep(3)

        # enter the name and submit the form to add a new task
        task_input_box = self.browser.find_element_by_id('id_name')
        task_name = 'Buy leather boots'
        task_input_box.send_keys(task_name)
        task_input_box.send_keys(Keys.ENTER)

        # page redirected to the list page and task appears.
        self.wait_for_name_in_list_contents(task_name)

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # one user start a new to-do list
        self.browser.get(self.live_server_url)

        new_list_link = self.browser.find_element_by_id('id_new_list')
        new_list_link.click()
        time.sleep(3)

        input_box = self.browser.find_element_by_id('id_name')
        input_box.send_keys('Shopping list')
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # page redirect to the newly created list page with unique url
        user_a_list_url = self.browser.current_url
        self.assertRegex(user_a_list_url, '/list/.+')

        # A new user come along to the site.

        ## make sure new browser session is started
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # New user visit the home page. There is no sign of User A list
        self.browser.get(self.live_server_url)
        # page_text = self.browser.find_element_by_tag_name('body').text
        # self.assertNotIn('Shopping list', page_text)

        # New user starts a new list
        new_list_link = self.browser.find_element_by_id('id_new_list')
        new_list_link.click()
        time.sleep(3)

        input_box = self.browser.find_element_by_id('id_name')
        input_box.send_keys('Holiday')
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # New user gets their own unique URL
        user_b_list_url = self.browser.current_url
        self.assertRegex(user_b_list_url, '/list/.+')
        self.assertNotEqual(user_a_list_url, user_b_list_url)
