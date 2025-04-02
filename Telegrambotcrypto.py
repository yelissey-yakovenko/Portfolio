from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

TOKEN = "token"

# Price functions
def get_price(coin: str):
    url = f"https://coinmarketcap.com/currencies/{coin}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    price_tag = soup.find("span", class_="sc-65e7f566-0 WXGwg base-text")
    if price_tag:
        price = price_tag.text.replace('$', '').replace(',', '')
        return float(price)
    return None

# /start command shows the "Старт" button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Старт", callback_data="show_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажмите кнопку:", reply_markup=reply_markup)

# Handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None:
        return

    await query.answer()

    if query.data == "show_menu":
        keyboard = [
            [InlineKeyboardButton("Курс BTC", callback_data="bitcoin")],
            [InlineKeyboardButton("Курс SOL", callback_data="solana")],
            [InlineKeyboardButton("Курс XRP", callback_data="xrp")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите криптовалюту:", reply_markup=reply_markup)

    elif query.data in ["bitcoin", "solana", "xrp"]:
        coin_name = query.data.upper()
        price = get_price(query.data)
        if price:
            await query.edit_message_text(f"💰 {coin_name} сейчас стоит ${price:,.2f}")
        else:
            await query.edit_message_text(f"⚠️ Не удалось получить цену для {coin_name}")

# Run the bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()