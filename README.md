Here’s the `requirements.txt` file for the Ubuntu version of the bot. This file lists all the Python dependencies needed to run the bot on Ubuntu.

### `requirements.txt`
```plaintext
python-telegram-bot==20.6
```

---

### Explanation:
1. **`python-telegram-bot`**:
   - This is the main library used to interact with the Telegram Bot API.
   - Version `20.6` is specified to ensure compatibility with the async/await syntax used in the code.

---

### Additional System Dependencies (Ubuntu):
The bot also relies on **LibreOffice** for file conversion, which is not a Python package but a system dependency. To install LibreOffice on Ubuntu, run:

```bash
sudo apt-get update
sudo apt-get install libreoffice --no-install-recommends
```

---

### How to Use `requirements.txt`:
1. Save the `requirements.txt` file in the same directory as your bot script.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### Full Setup Instructions for Ubuntu:
1. Install system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install libreoffice python3-pip python3-venv --no-install-recommends
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```bash
   python3 bot.py
   ```

---

### Notes:
- The `requirements.txt` file only lists Python dependencies. System dependencies like LibreOffice must be installed separately.
- If you need additional Python packages in the future, add them to `requirements.txt` and re-run `pip install -r requirements.txt`.
