from selenium import webdriver
from time import sleep
from secrets import pw
from secrets import username

debug = True

class InstaBot:
    def __init__(self, username, pw):
    #def __init__(self):
        self.username = username
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(2)
        
        sleep(2)
        #enter username and password
        self.driver.find_element_by_xpath("//input[@name = \"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name = \"password\"]")\
            .send_keys(pw)
        if debug: print("Logging in...")
        #click log in
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        if debug: print("Logged in...")

        #not now - save password?
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)
        if debug: print("Do not save password...")

        #not now - dont turn on notifications
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(4)
        if debug: print("Do not turn on notifications...")

    def get_unfollowers(self):
        #go to my profile - click button "my username"
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username))\
            .click()
        sleep(4)
        if debug: print("Clicked Profile...")
        
        #click following list        
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")\
            .click()
        sleep(2)
        if debug: print("Accessed following list...")
        following = self._get_names()

        
        #click followers list        
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")\
            .click()
        sleep(2)
        if debug: print("Accessed followers list...")
        followers = self._get_names()

        not_following_back = [user for user in following if user not in followers]
        opposite = [user for user in followers if user not in following]
        print("num followers: " + str(len(followers)))
        print("num following: " + str(len(following)))
        print("num nfb: " + str(len(not_following_back)))
        print("num opp: " + str(len(opposite)))
        print()
        print(not_following_back)
        print()
        print(opposite)

    def _get_names(self):
        sleep(2)

        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

        sleep(2)
        
        #Scroll through list
        last_ht,ht = 0,1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)
        
        #Add accts to list
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        #close button
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

my_bot = InstaBot(username, pw)
my_bot.get_unfollowers()