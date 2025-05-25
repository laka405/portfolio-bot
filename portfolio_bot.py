import telebot
from playwright.sync_api import sync_playwright

# Your Telegram Bot Token (hardcoded)
TELEGRAM_BOT_TOKEN = '8013736348:AAFYTR-ggXW5CFBImfcdCPgPNKAOccA48MA'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

debank_url = "https://debank.com/profile/0x99f83ec57fe1e09da9a20efc00156b71826e11c6"
dropstab_url = "https://dropstab.com/p/main-helrs9u41s"

def get_balances():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # DeBank
        page.goto(debank_url)
        page.wait_for_timeout(5000)
        try:
            debank = page.locator('.PortfolioHeader_netWorth__value__zfoUt').inner_text()
        except:
            debank = "Error fetching"

        # DropsTab
        page.goto(dropstab_url)
        page.wait_for_timeout(5000)
        try:
            dropstab = page.locator('xpath=//div[contains(text(),"Total Portfolio Value")]/following-sibling::div').inner_text()
        except:
            dropstab = "Error fetching"

        browser.close()
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
