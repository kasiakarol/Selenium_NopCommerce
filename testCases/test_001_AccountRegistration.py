from pageObjects.HomePage import MainPage
from pageObjects.AccountRegistrationPage import AccountRegistrationPage
import random
from utilities import randomeString
import os
from utilities.readProperties import ReadConfig
import time
import pytest

# TC_RF_002 - Validate registering an account by providing all the fields

# Test case to register a new user with a random gender, using a unique email address generated by randomString function
# It validates if the user, after the successful registration, is taken to the 'Account Success' page
# and if the confirmation message displayed is correct


class Test_001_AccountReg():
    baseURL = ReadConfig.getApplicationURL()
    password = ReadConfig.getPassword()
    fname_reg = ReadConfig.fname_reg()
    lname_reg = ReadConfig.lname_reg()
    dob_day_reg = ReadConfig.dob_day_reg()
    dob_month_reg = ReadConfig.dob_month_reg()
    dob_year_reg = ReadConfig.dob_year_reg()
    company_name_reg = ReadConfig.company_name_reg()
    email = randomeString.random_login_generator() + '@test.com'

    @pytest.mark.sanity
    @pytest.mark.regression
    @pytest.mark.myaccount
    def test_account_reg(self, setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        self.hp=MainPage(self.driver)
        self.hp.register()

        self.rp=AccountRegistrationPage(self.driver)
        self.random_gender = random.randint(0, 1)
        if self.random_gender == 0:
            self.rp.setGenderMale()
        elif self.random_gender == 1:
            self.rp.setGenderFemale()
        self.rp.setFirstName(self.fname_reg)
        self.rp.setLastName(self.lname_reg)
        self.rp.setDoBDay(self.dob_day_reg)
        self.rp.setDoBMonth(self.dob_month_reg)
        self.rp.setDoBYear(self.dob_year_reg)

        self.rp.setEmail(self.email)
        self.rp.setCompanyName(self.company_name_reg)
        self.rp.setNewsletter()
        self.rp.setPassword(self.password)
        self.rp.setConfirmPassword(self.password)
        time.sleep(2)
        self.rp.clickRegister()
        self.confmsg=self.rp.getcompletedmsg()

        # to validate the confirmation message. In case of failure, the screenshot is taken
        if self.confmsg == "Your registration completed":
            assert True
            self.driver.close()
        else:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\screenshots\\" + "test_account_reg.png")
            self.driver.close()
            assert False
