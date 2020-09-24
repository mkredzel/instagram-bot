from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
from time import sleep, strftime
from random import randint

# Firefox Profile Language Preferences
firefox_profile = webdriver.FirefoxProfile() 
firefox_profile.set_preference('intl.accept_languages', 'en')

# Gecko Driver Path
webdriver = webdriver.Firefox(executable_path=r'Enter_your_path_for_geckodriver.exe', firefox_profile=firefox_profile)
sleep(3)

# Go To Login Page
webdriver.get('https://www.instagram.com/accounts/login/')
sleep(3)

# User Credentials
username = webdriver.find_element_by_name('username')
username.send_keys('enter_your_username')
password = webdriver.find_element_by_name('password')
password.send_keys('enter_your_password')

# Click 'not now' buttons
buttons = webdriver.find_elements_by_tag_name('button')
buttons[2].click()
sleep(3)

buttons = webdriver.find_elements_by_tag_name('button')
buttons[1].click()
sleep(3)

notnow = webdriver.find_element_by_class_name("aOOlW")
notnow.click()
sleep(3)

# Desired Hashtags
hashtag_list = ['travel', 'summer', 'design']
tag = -1

# Loop Through Hashtags
for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    
    first_thumbnail.click()
    sleep(3)

    # Loop Through Pictures
    for x in range(1,200):

        # Likes
        variable = webdriver.find_element_by_class_name('_2dDPU')
        actions = ActionChains(webdriver)
        actions.move_to_element(variable)
        actions.double_click(variable)
        actions.perform()
        sleep(2)
       
        # Comments
        comm_prob = randint(1,10)
        webdriver.find_element_by_class_name('Ypffh').click()
        comment_box = webdriver.find_element_by_class_name('Ypffh')
        
        if comm_prob < 7:
            comment_box.send_keys('Really cool!')
            sleep(1)
        if (comm_prob > 6) and (comm_prob < 9):
            comment_box.send_keys('🤩')
            sleep(1)
        elif comm_prob == 9:
            comment_box.send_keys('Thats amazing!')
            sleep(1)
        elif comm_prob == 10:
            comment_box.send_keys('So cool! 😎')
            sleep(1)

        # Enter to post comment
        comment_box.send_keys(Keys.ENTER)
        sleep(10)

        # Next picture
        webdriver.find_element_by_link_text('Next').click()
        sleep(2)
