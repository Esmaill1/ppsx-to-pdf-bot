import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7289833807:AAFOqKJCMDlr2aIdiGVv-L6AYmlLRsQEprQ"

# Function to convert PPSX to PDF using LibreOffice
def convert_ppsx_to_pdf(input_path, output_path):
    try:
        # Use LibreOffice to convert PPSX to PDF
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(output_path), input_path],
            check=True
        )
        return True
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a .ppsx file, and I'll convert it to a .pdf for you!")

# File handler
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file.file_name.lower().endswith('.ppsx'):
        await update.message.reply_text("Please send a valid .ppsx file.")
        return

    # Download the file
    file_path = f"downloads/{file.file_name}"
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("converted", exist_ok=True)
    file_obj = await file.get_file()
    await file_obj.download(file_path)

    # Convert to PDF
    output_file = f"converted/{os.path.splitext(file.file_name)[0]}.pdf"
    await update.message.reply_text("Converting your file to PDF. Please wait...")
    success = convert_ppsx_to_pdf(file_path, output_file)

    if success:
        # Send the converted file back to the user
        await update.message.reply_document(document=open(output_file, "rb"))
        await update.message.reply_text("Here is your converted PDF!")
    else:
        await update.message.reply_text("Sorry, something went wrong during the conversion.")
    
    # Cleanup
    os.remove(file_path)
    if os.path.exists(output_file):
        os.remove(output_file)

# Main function to set up the bot
def main():
    # Initialize the bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
