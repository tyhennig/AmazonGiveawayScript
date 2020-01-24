from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS4
import requests
import re
import time


def shortVideo():
            video.click()
            time.sleep(16)
            video.click()
            button = driver.find_element_by_tag_name("button")
            button.click()

        
def boxClick():
    box.click()




login_url = """https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&
openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%
2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2
.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.open
id.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpa
pe%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%
2Flogin%2Fs%3Fk%3Dlogin%26page%3D4%26ref_%3Dnav_custrec_signin&switch_account="""


amazon_link = "https://www.amazon.com"
driver = webdriver.Firefox()

#Logging in block
driver.get(login_url)
email =''
password = ''
emailInput = driver.find_element_by_id("ap_email")
emailInput.send_keys(email)
passInput = driver.find_element_by_id("ap_password")
passInput.send_keys(password);
passInput.send_keys(Keys.ENTER)
time.sleep(2)

#Getting statistics
stats_read = open('stats.txt', 'r')
lines = stats_read.readlines()

total_links = int(lines[1])
total_lost_links = int(lines[3])
total_won_links = int(lines[5])
total_unsure_links = int(lines[7])


#Getting which page it's on via text file
page_read = open("page.txt", "r")
page_number = page_read.read()
page_read.close()

#FOR TESTING
#page_number = 1
#FOR TESTING


for x in range(int(page_number), int(page_number)+10):
    giveaway_url = "https://www.amazon.com/ga/giveaways/?pageId={}".format(x)
    print("ON PAGE {}".format(x))
    driver.get(giveaway_url)
    time.sleep(3)
    soup = BS4(driver.page_source, 'html.parser')

    items = []
    lost_links = []
    won_links = []
    unsure_links = []

    for item in soup.find_all('a', attrs={'class': 'a-link-normal item-link'}):
        item_link = amazon_link + item.get('href')
        print(item_link)
        items.append(item_link)

    for links in items:
        driver.get(links)
        #try block for waiting until pages is fully loaded
        loaded = False
        loops = 0
        while loaded == False and loops < 4:
            try:
                soup = BS4(driver.page_source, 'html.parser')
                condition = soup.find('span', attrs={'class': 'a-size-medium a-color-secondary a-text-bold prize-title'})
                condition.get_text()
                loaded = True
            except:
                #print("Loading Initial Page...")
                loops += 1
                time.sleep(1)
        


        if condition.get_text() == "Enter for a chance to win!":
            loaded = "none"
            #print("condition detected as enter for chance to win")
            loops = 0
            while loaded == "none" and loops < 8:
                try:
                    box = driver.find_element_by_class_name("a-text-center.box-click-area")
                    boxClick()
                    #print("boxclick method completed")
                    loaded = "some"

                except:
                    try:
                        video = driver.find_element_by_class_name("youtube-video")
                        shortVideo()
                        #print("shortvideo youtube method completed")
                        loaded = "some"
                    except:
                        try:
                            video = driver.find_element_by_class_name("amazon-video")
                            shortVideo()
                            #print("shortvide amazon method complete")
                            loaded = "some"

                        except:
                            #print("Didn't find video or box, Loading...")
                            time.sleep(1)
                #print("staying in none loop")
                loops +=1
            time.sleep(2)
            loaded = "none"
            loops = 0
            while loaded is "none" and loops < 8:
                try:
                    #print("trying to get win status")
                    condition = driver.find_element_by_class_name('a-size-medium.a-color-secondary.a-text-bold.prize-title').get_attribute("innerHTML")
                    #print(condition)
                    if condition == "Tyler, you didn't win":
                        #print("GIVEAWAY LOST")
                        lost_links.append(links)
                        loaded = "some"
                    elif condition == "Enter for a chance to win!":
                        #print("still says enter for chance")
                        loops +=1
                        time.sleep(1)
                    else:
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!YOU WON HOLY COW!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        print(links)
                        won_links.append(links)
                        loaded = "some"
                except:
                   # print("win status not there retrying...")
                    time.sleep(1)


        elif condition.get_text() == "Tyler, you didn't win":
           # print("GIVEAWAY ALREADY ROLLED")
            lost_links.append(links)
        else:
            #print("ERROR OR GIVEAWAY ENDED...")
            unsure_links.append(links)


    print("Number of tried items:   {}".format(len(items)))
    print("Number of lost items:    {}".format(len(lost_links))) 
    print("Number of won items:     {}".format(len(won_links)))
    print("Number of unsure items:  {}".format(len(unsure_links)))
    page_write = open('page.txt', 'w')
    page_write.write(("{}".format(x+1)))
    page_write.close()

    if len(won_links) > 0:
        won_write = open('won_links.txt', 'a')
        for link in won_links:
            won_write.write(("{}\n").format(link))
        won_write.close()

    total_links += len(items)
    total_lost_links += len(lost_links)
    total_won_links += len(won_links)
    total_unsure_links += len(unsure_links)


    stats_write = open('stats.txt', 'w')
    stats_write.write('items tried:\n{}\nitems lost:\n{}\nitems won:\n{}\nitems unsure:\n{}'.format(total_links, total_lost_links, total_won_links, total_unsure_links))
    stats_write.close()
