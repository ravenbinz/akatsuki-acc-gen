import os
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Bot token and configuration
BOT_TOKEN = "6476855791:AAGZ07MbW48QyFfR0gyd-XSFBCljsQ0jL1o"
COOLDOWN_TIME = 30  # 30-second cooldown

# Dictionary to track last request time for each user
user_last_request = {}

# Command handler to start the bot
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Crunchyroll", callback_data='crunchyroll'), InlineKeyboardButton("Steam", callback_data='steam')],
        [InlineKeyboardButton("Hotmail", callback_data='hotmail'), InlineKeyboardButton("IPVanish", callback_data='ipvanish')],
        [InlineKeyboardButton("Windscribe", callback_data='windscribe'), InlineKeyboardButton("Warp", callback_data='warp')],
        [InlineKeyboardButton("Disney+", callback_data='disneyplus'), InlineKeyboardButton("Xbox", callback_data='xbox')],
        [InlineKeyboardButton("Email-FA", callback_data='email-fa')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🎉 Welcome! Which account would you like to generate?", reply_markup=reply_markup)

# Callback handler to generate account
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    # Check cooldown
    last_request_time = user_last_request.get(chat_id, 0)
    current_time = time.time()

    if current_time - last_request_time < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (current_time - last_request_time)
        query.edit_message_text(text=f"⏳ Please wait {int(remaining_time)} seconds before generating another account.")
        return

    user_last_request[chat_id] = current_time

    # Generate account based on button clicked
    account = generate_account(query.data)
    query.edit_message_text(text=account)

# Function to generate an account and remove it from the file
def generate_account(account_type: str) -> str:
    file_map = {
        "crunchyroll": "crunchyroll.txt",
        "steam": "steam.txt",
        "hotmail": "hotmail.txt",
        "ipvanish": "ipvanish.txt",
        "windscribe": "windscribe.txt",
        "warp": "warp.txt",
        "disneyplus": "disneyplus.txt",
        "xbox": "xbox.txt",
        "email-fa": "email-fa.txt"  # Added email-fa to the list
    }

    file_path = file_map.get(account_type)
    if not file_path or not os.path.exists(file_path):
        return f"🚫 No more {account_type} accounts available!"

    with open(file_path, 'r') as file:
        lines = file.readlines()

    if not lines:
        return f"🚫 No more {account_type} accounts available!"

    account = lines[0].strip()
    with open(file_path, 'w') as file:
        file.writelines(lines[1:])

    return f"✅ Here is your {account_type} account: {account}"

# Main function to run the bot
def main() -> None:
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    