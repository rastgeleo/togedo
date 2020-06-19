import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_input_in_task_list(self, input_text):
        unordered_list = self.browser.find_element_by_id('id_task_list')
        task_list = unordered_list.find_elements_by_tag_name('li')
        self.assertIn(
            input_text,
            [task.find_elements_by_tag_name('a')[0].text
                for task in task_list]
            )

    def test_can_add_a_task_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Togedo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Togedo!', header_text)

        inputbox = self.browser.find_element_by_id('id_name')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Add a task')

        inputbox.send_keys('Do food shopping')

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_input_in_task_list('Do food shopping')

        inputbox = self.browser.find_element_by_id('id_name')
        inputbox.send_keys('Clean bathroom')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_input_in_task_list('Do food shopping')
        self.check_input_in_task_list('Clean bathroom')


if __name__ == "__main__":
    unittest.main()
