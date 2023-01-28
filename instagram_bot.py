import os

from dotenv import load_dotenv
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException

from time import sleep
from random import randint

# Instagram "Likes" and "Comments" limits to be aware of:
# Likes: 120 per hour or 300-500 per day
# Comments: 200 per day

like = True
comment = True
photosPerHashtag = 40
hashtags = ['l4l', 'travel', 'summer']

# Load Environment Variables
load_dotenv()

# Firefox Profile Configuration
service = Service(os.getenv('GECKO_DRIVER_PATH'))
options = Options()
options.set_preference('intl.accept_languages', 'en-US, en')
options.set_preference('profile', os.getenv('FIREFOX_PROFILE_PATH'))
webdriver = Firefox(service=service, options=options)
sleep(1)

# Go To Login Page
webdriver.get('https://www.instagram.com/accounts/login/')
sleep(3)

# Accept Cookies
cookies = webdriver.find_element(by=By.CLASS_NAME, value="_a9_0")
cookies.click()
sleep(3)

# Enter User Credentials
username = webdriver.find_element(by=By.NAME, value='username')
username.send_keys(os.getenv('INSTA_USERNAME'))
password = webdriver.find_element(by=By.NAME, value='password')
password.send_keys(os.getenv('INSTA_PASSWORD'))
sleep(3)

# Click Login Button
login = webdriver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button")
login.click()
sleep(10)

# Click 'not now' buttons
notNow = webdriver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button")
notNow.click()
sleep(3)

# Loop Through Hashtags
for hashtag in hashtags:

    webdriver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    sleep(5)
    newestPhoto = webdriver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div/div[1]/div[1]/a/div")
    newestPhoto.click()
    sleep(3)

    # Loop Through Pictures
    for x in range(1, photosPerHashtag):

        if like:
            # Like the photo
            selectedPhoto = webdriver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div/div")
            likeActions = ActionChains(webdriver)
            likeActions.move_to_element(selectedPhoto)
            likeActions.double_click(selectedPhoto)
            likeActions.perform()
            sleep(2)

        if comment:
            # Comment on the photo
            commentRandomizer = randint(1, 10)

            try:
                commentInput = webdriver.find_element(By.CSS_SELECTOR, "textarea")
            except NoSuchElementException:
                print("Comments are disabled on this photo...") 

            # Type randomized comment and hit 'Enter' to submit it
            if commentRandomizer < 5:
                commentInput.send_keys("That's a great photo! 📸", Keys.ENTER)
            elif commentRandomizer < 7:
                commentInput.send_keys('Really cool!', Keys.ENTER)
            elif (commentRandomizer > 6) and (commentRandomizer < 9):
                commentInput.send_keys('🤩', Keys.ENTER)
            elif commentRandomizer == 9:
                commentInput.send_keys('Amazing!', Keys.ENTER)
            elif commentRandomizer == 10:
                commentInput.send_keys('So cool! 😎', Keys.ENTER)

        # There is a "timing" limit too...
        # Wait 20–30 seconds between each "like" or "comment".
        # If you go too fast, Instagram might think you are a bot (XD) and block you.
        sleep(20)

        # Next photo
        webdriver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button").click()
