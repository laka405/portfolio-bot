import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Your bot token from BotFather
TELEGRAM_BOT_TOKEN = '7865171608:AAHq8aW-5BKBBTjWzwJ6FH_iWT1Qm5SsPk0'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Portfolio URLs
debank_url = "https://debank.com/profile/0x99f83ec57fe1e09da9a20efc00156b71826e11c6"
dropstab_url = "https://dropstab.com/p/main-helrs9u41s"

def get_balances():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # DeBank
    driver.get(debank_url)
    time.sleep(5)
    try:
        debank = driver.find_element(By.CLASS_NAME, "PortfolioHeader_netWorth__value__zfoUt").text
    except:
        debank = "Error fetching"

    # DropsTab
    driver.get(dropstab_url)
    time.sleep(5)
    try:
        dropstab = driver.find_element(By.XPATH, '//div[contains(text(),"Total Portfolio Value")]/following-sibling::div').text
    except:
        dropstab = "Error fetching"

    driver.quit()
    return debank, dropstab

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hi! Send /balance to get your portfolio balances.")

@bot.message_handler(commands=['balance'])
def send_balance(message):
    bot.reply_to(message, "⏳ Fetching your balances...")
    debank, dropstab = get_balances()
    reply = f"💼 DeBank: {debank}\n📊 DropsTab: {dropstab}"
    bot.send_message(message.chat.id, reply)

print("Bot is running...")
bot.infinity_polling()
