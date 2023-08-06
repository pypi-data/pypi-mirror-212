from selenium import webdriver
import platform


class Enviroments:
    @staticmethod
    def before_all(self, consts):
        chrome_options = webdriver.ChromeOptions()
        os_name = platform.system()
        print('wich platform =>' + os_name) 

        if os_name == 'Windows':
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.driver = webdriver.Chrome(executable_path= consts.PATH["WINDOWS_CHROMEDRIVER_PATH"], chrome_options=options)
            self.driver.maximize_window() # Ene ni delgetsiig tomruulna.
        else:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(consts.PATH["LINUX_CHROMEDRIVER_PATH"], options=chrome_options)
            self.driver.maximize_window()   

    def after_all(self):
        self.driver.quit()

