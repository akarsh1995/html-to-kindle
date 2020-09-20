from datetime import datetime

from selenium.webdriver.common.keys import Keys

from ken.browser import Browser


class KenArticle:

    def __init__(self, username, password, browser: Browser):
        self.username = username
        self.password = password
        self.browser = browser


    def get_latest_article_source(self):
        self.login()
        self.navigate_to_beyond_first_order()
        self.navigate_to_latest_article()
        return self.browser.page_source

    def navigate_to_beyond_first_order(self):
        self.browser.get('https://www.the-ken.com/bfo')

    def navigate_to_latest_article(self):
        latest_article_element = self.browser.wait_and_find_elem(
            '//date[text()="{}"]'.format(self.latest_article_date)
        )
        latest_article_element.click()
        self.browser.wait_and_find_elem('//img[@alt="Beyond The First Order"]')

    def login(self):
        self.browser.get('https://www.the-ken.com/login')
        username_input = self.browser.wait_and_find_elem('//*[@id="user_login"]')
        username_input.send_keys(self.username)
        password_input = self.browser.wait_and_find_elem('//*[@id="user_pass"]')
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        self.browser.wait_and_find_elem('//*[@id="recent-stories"]')

    @property
    def latest_article_date(self):
        today = datetime.now()
        return today.strftime('%d %b, %y')
