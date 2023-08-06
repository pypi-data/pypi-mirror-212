
from behave import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from itaed.exception import ExceptionCheck
from itaed.tools import Tools
import time
class Click:


    @staticmethod
    def send_keys(self, driver, element, value, consts):
        driver=self.driver
        locater, element= Tools.define_locater(self, element)
        ExceptionCheck.driver_wait_exception(self, driver, consts ,EC.visibility_of_element_located((locater, element)), element, "TIMEOUT")
        element = driver.find_element(locater, "{}".format(element))
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.move_to_element(element).click().perform()
        actions.move_to_element(element).send_keys(value).perform() 

    @staticmethod
    def simple_click(self, driver, element, consts):
        locater, element= Tools.define_locater(self, element)
        ExceptionCheck.driver_wait_exception(self, driver, consts ,EC.visibility_of_element_located((locater, element)), element, "TIMEOUT")
        element = driver.find_element(locater, element)
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.move_to_element(element).click().perform()  


    @staticmethod
    def menu(self, driver, elements, inspected_element, name, consts):  
        name_split = name.split('-')
        list=[x.lower() for x in name_split]
        list=[x.replace(' ', '_') for x in list]
        dictionary = elements.elements["menu"]
        for i in range(len(list)):
            dictionary, element_id = elements.get_element(dictionary, inspected_element, list[i])
            Click.simple_click(self, driver, element_id, consts)

    @staticmethod
    def tab(field, elements, tab):
        tab = tab.lower()
        field=field.lower()
        dictionary = elements.elements[tab].get(field)
        return dictionary

    @staticmethod        
    def displayed(self, driver, element):
            locater, element = Tools.define_locater(self, driver, element)
            ExceptionCheck.driver_wait_exception(self, driver, EC.element_to_be_clickable((locater, element)), element, "TIMEOUT")  # + " element clickable"
            ExceptionCheck.driver_wait_exception(self, driver, EC.presence_of_element_located((locater, element)), element, "TIMEOUT")  # + " visibility of element"
            elements = driver.find_elements(locater, element)
            for i in range(len(elements)):
                element = elements[i]
                if element.is_displayed():
                    actions = ActionChains(self.driver)
                    actions.move_to_element(element)
                    actions.move_to_element(element).click().perform()
    

    @staticmethod
    def onchange(self, driver, elements, value):
        locater, element = Tools.define_locater(self, elements)
        selected_element = driver.find_element(locater, element)
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].onchange()", selected_element, value)

    
           