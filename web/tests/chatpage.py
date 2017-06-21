import setup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Test Setup
playerNames = {
        'zella': 'ZellaTheUltimate',
        'deckerd': 'DeckerdTheHesitant',
        'moldavi': 'MoldaviTheMoldavish',
        'drake': 'Drackan',
        'zeke': 'Zeke',
        'jack': 'JackSlayerTheBeanSlasher'
      }

def getPathToElement(playerName, tag, name):
  xpathForPageElement = "//*[contains(@id, 'chat-page-%s')]//%s[contains(@name, '%s')]"
  return xpathForPageElement % (playerName, tag, name)

def changeToPage(driver, drawerOption):
  driver.Click([[By.NAME, 'drawer' + drawerOption]])

def closeNotifications(driver):
  driver.Click([[By.NAME, 'close-notification']])

def openChatDrawer(driver, actingPlayer, chatRoomName):
  xpathChatDrawerButton = getPathToElement(actingPlayer, 'paper-icon-button', 'chat-info-' + chatRoomName)
  driver.Click([[By.XPATH, xpathChatDrawerButton]])  

def openChatDrawer(driver, actingPlayer, chatRoomName):
  xpathChatDrawerButton = getPathToElement(actingPlayer, 'paper-icon-button', 'chat-info-' + chatRoomName)
  driver.Click([[By.XPATH, xpathChatDrawerButton]])  


# Start Test
actingPlayer = 'zeke' # non-admin zombie
actingPlayerName = playerNames[actingPlayer]
newChatName = 'No hoomans allowed'
driver = setup.MakeDriver()
driver.WaitForGameLoaded()

# Open chat page
driver.SwitchUser(actingPlayer)
driver.Click([[By.NAME, 'drawerChat']])

# Open dialog for creating new chat room
driver.FindElement([[By.ID, 'new-chat']])
driver.Click([[By.ID, 'new-chat']])

# Set chat room settings to be zombie only
driver.FindElement([[By.ID, 'chatName']])
driver.SendKeys([[By.ID, 'chatName'], [By.TAG_NAME, 'input']], newChatName)
driver.Click([[By.ID, 'allegianceFilter']])
driver.Click([[By.ID, 'settingsForm'], [By.ID, 'done']])

# Check the newly created chat room is opened
driver.FindElement([[By.NAME, 'ChatRoom: %s' % newChatName]])

# Add a zombie to chat
openChatDrawer(driver, actingPlayerName, newChatName)
xpathAdd = getPathToElement(actingPlayerName, 'a', 'chat-drawer-add')
driver.Click([[By.XPATH, xpathAdd]])
driver.FindElement([[By.ID, 'lookup']])
driver.SendKeys([[By.TAG_NAME, 'ghvz-chat-page'], [By.ID, 'lookup'], [By.TAG_NAME, 'input']], playerNames['drake'])
driver.SendKeys([[By.TAG_NAME, 'ghvz-chat-page'], [By.ID, 'lookup'], [By.TAG_NAME, 'input']], Keys.RETURN)

# Check drawer to see that zombie was added
driver.FindElement([[By.NAME, playerNames['drake']]])

# Make sure human can't be added to chat
driver.Click([[By.XPATH, xpathAdd]])
driver.FindElement([[By.ID, 'lookup']])
driver.SendKeys([[By.TAG_NAME, 'ghvz-chat-page'], [By.ID, 'lookup'], [By.TAG_NAME, 'input']], playerNames['jack'])
driver.SendKeys([[By.TAG_NAME, 'ghvz-chat-page'], [By.ID, 'lookup'], [By.TAG_NAME, 'input']], Keys.RETURN)
driver.DontFindElement([[By.NAME, playerNames['jack']]])

driver.Quit()