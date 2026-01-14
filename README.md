---
title: duolingobot
emoji: 📊
colorFrom: purple
colorTo: indigo
sdk: docker
pinned: false
license: other
app_file: main.rb
---

# DuolingoBot
Duolingo Bot for Telegram

## Available Implementations

This repository contains two implementations of the Duolingo Telegram bot:

### Ruby Implementation (Original)
Version 1.0 - Located in the root directory

### Python Implementation (New) 🐍
Version 2.0 - Located in the `python-bot/` directory

Both implementations provide the same functionality with different tech stacks.

## Features

Returns user experience points through /xp command as
```/xp myusername123```, the result is
> Hello telegramUser, the xp of myusername123 is 99999

Additional commands:
- `/streak <username>` - Get user's current streak
- `/crowns <username>` - Get user's total crowns
- `/start` - Start the bot
- `/help` - Display help information

## Running the Python Bot

### Quick Start with Docker

```bash
cd python-bot
docker build -t duolingo-bot-python .
docker run -e TELEGRAM_BOT_TOKEN="your_token_here" duolingo-bot-python
```

### Using Docker Compose

Create a `.env` file with your bot token:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Then run:
```bash
docker-compose -f docker-compose-python.yml up -d
```

### Running Locally (Python)

```bash
cd python-bot
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="your_token_here"
python app.py
```

For detailed Python implementation instructions, see [python-bot/README.md](python-bot/README.md).

## Running the Ruby Bot

Set your token in a `.env` file:
```env
TOKEN_TELEGRAM=your_token_here
```

Then run:
```bash
bundle install
ruby main.rb
```

Or use Docker:
```bash
docker-compose up
```

## Future improvements
- Add an user list of weekly experience
- Returns more statistics from an user
