from selenium.webdriver.common.by import By

class Locators:
    From_input = (By.ID, "src")
    To_input = (By.ID, "dest")
    Date_picker = (By.XPATH,"//div[@id='onwardCal']")
    Help_button = (By.ID, "help_redcare")
    Iframe1= (By.XPATH,"//div[@class='modal']//iframe[@class='modalIframe']")
    Iframe = (By.XPATH, "//div[@class='iframe-content']/iframe[@src='//www.redbus.in/help?hideLayout=true']")
    Technical_issues = (By.XPATH, '//body[1]/div[2]/div[1]/div[2]/div[4]/div[2]/div[1]/div[3]/img[1]')
    No_buses_found = (By.XPATH, "//div[normalize-space()='No buses found']")
    Response = (By.XPATH, " //div[@class='new-issutype-head']")
    Searchbutton = (By.ID, "search_button")
    Bus_items = (By.XPATH, "//div/ul[@class='bus-items']/div")
    Departure = (By.XPATH, "//div/ul[@class='bus-items']/div/li/div/div/div[1]/div[4]/div[1]")
    Type = (By.XPATH, "//div/ul[@class='bus-items']/div/li/div/div/div[1]/div[1]/div[2]")
    Cost = (By.XPATH,"//span[contains(@class, 'f-19')]")
    amenities = (By.XPATH, "//li[2][@class='amenties b-p-list']")
    Dropdown = (By.XPATH, "//ul/li/div/text[@class='placeHolderMainText']")
    date = (By.XPATH, "//span[@class='DayTiles__CalendarDaysSpan-sc-1xum02u-1 dkWAbH']")

# //div[@class='DayNavigator__IconBlock-qj8jdz-2 iZpveD']
# //div[class="DayNavigator__IconBlock-qj8jdz-2 iZpveD"]
# //div[class="DayTilesWrapper__RowWrap-sc-19pz9i8-1 fGGTDM"]/span/div/span