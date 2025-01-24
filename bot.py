import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7289833807:AAFOqKJCMDlr2aIdiGVv-L6AYmlLRsQEprQ"

# Linux/Ubuntu paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
CONVERTED_DIR = os.path.join(BASE_DIR, "converted")

# Create directories with proper permissions
os.makedirs(DOWNLOADS_DIR, exist_ok=True, mode=0o755)
os.makedirs(CONVERTED_DIR, exist_ok=True, mode=0o755)

def convert_ppsx_to_pdf(input_path, output_path):
    try:
        # Verify LibreOffice installation
        subprocess.run(["which", "soffice"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Run conversion command
        result = subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", CONVERTED_DIR, input_path],
            check=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        
        # Verify output file
        if not os.path.exists(output_path):
            print(f"Conversion failed. LibreOffice output:\n{result.stdout}")
            return False
        return True

    except subprocess.CalledProcessError as e:
        print(f"LibreOffice Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Conversion Error: {str(e)}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📎 Hello! Send me a .ppsx file, and I'll convert it to PDF for you!")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = None
    output_file = None
    
    try:
        document = update.message.document
        if not document.file_name.lower().endswith('.ppsx'):
            await update.message.reply_text("❌ Please send a valid .ppsx file.")
            return

        # Generate safe file paths
        file_name = document.file_name
        safe_file_name = "".join([c if c.isalnum() else "_" for c in file_name])
        file_path = os.path.join(DOWNLOADS_DIR, safe_file_name)
        output_file = os.path.join(CONVERTED_DIR, f"{os.path.splitext(safe_file_name)[0]}.pdf")

        # Download the file (proper async handling)
        file_obj = await document.get_file()
        await file_obj.download_to_drive(custom_path=file_path)  # Correct async method

        # Convert to PDF
        await update.message.reply_text("⏳ Converting your file to PDF...")
        if convert_ppsx_to_pdf(file_path, output_file):
            await update.message.reply_document(
                document=open(output_file, "rb"),
                caption="✅ Here's your converted PDF!"
            )
        else:
            await update.message.reply_text("❌ Conversion failed. Please try again with a valid .ppsx file.")

    except Exception as e:
        print(f"Error: {str(e)}")
        await update.message.reply_text("❌ An error occurred. Please try again.")
    
    finally:
        # Cleanup files
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        if output_file and os.path.exists(output_file):
            os.remove(output_file)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
