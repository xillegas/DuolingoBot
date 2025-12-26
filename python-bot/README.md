# Duolingo Bot for Telegram - Python Implementation

A Telegram bot that fetches and displays Duolingo user statistics using the public Duolingo API.

## Features

- Fetch total XP for any Duolingo user
- Get current streak information
- Display total crowns earned across all courses
- Async/await implementation using `python-telegram-bot` v20+
- Docker support for easy deployment

## Commands

- `/start` - Start the bot and get a welcome message
- `/help` - Display help information and available commands
- `/xp <username>` - Get total XP for a Duolingo user
- `/streak <username>` - Get current streak for a Duolingo user
- `/crowns <username>` - Get total crowns for a Duolingo user

### Example Usage

```
/xp myusername123
```

Response:
```
Hello John, the XP of myusername123 is 15420 ⭐
```

## Environment Variables

The bot requires the following environment variable:

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (get it from [@BotFather](https://t.me/botfather))

## Running Locally

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/xillegas/DuolingoBot.git
cd DuolingoBot/python-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set the environment variable:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

4. Run the bot:
```bash
python app.py
```

## Running with Docker

### Build the Docker image:

```bash
docker build -t duolingo-bot-python .
```

### Run the container:

```bash
docker run -e TELEGRAM_BOT_TOKEN="your_bot_token_here" duolingo-bot-python
```

## Running with Docker Compose

Create a `.env` file in the `python-bot` directory:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Then use the docker-compose configuration:

```yaml
version: "3.8"
services:
  python-bot:
    build:
      context: ./python-bot
      dockerfile: Dockerfile
    env_file:
      - ./python-bot/.env
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## API Information

This bot uses the public Duolingo API endpoint:
```
https://www.duolingo.com/2017-06-30/users?username={username}
```

No authentication is required for basic user statistics.

## Security Notes

- **Never commit your bot token** to version control
- Always use environment variables for sensitive data
- The `.env` file is gitignored by default

## Version

Python Implementation v2.0

## Developer

Developed by Xillegas

## License

See the main repository LICENSE file.
