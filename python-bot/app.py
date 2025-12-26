"""
Duolingo Bot for Telegram - Python Implementation
Fetches Duolingo user statistics and provides them via Telegram commands.
"""

import os
import logging
import json
from typing import Optional
import asyncio

import httpx
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class DuolingoUser:
    """Represents a Duolingo user with their statistics."""
    
    def __init__(self, data: dict):
        """Initialize a DuolingoUser from API response data."""
        self.username = data.get('username', '')
        self.total_xp = data.get('totalXp', 0)
        self.streak = data.get('streak', 0)
        self.crowns = self._count_crowns(data.get('courses', []))
        self.user_id = data.get('id', '')
    
    @staticmethod
    def _count_crowns(courses: list) -> int:
        """Count total crowns across all courses."""
        total = 0
        for course in courses:
            total += course.get('crowns', 0)
        return total


async def fetch_duolingo_user(username: str) -> Optional[DuolingoUser]:
    """
    Fetch Duolingo user data from the public API.
    
    Args:
        username: The Duolingo username to fetch
        
    Returns:
        DuolingoUser object if found, None otherwise
    """
    url = f"https://www.duolingo.com/2017-06-30/users?username={username}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            users = data.get('users', [])
            
            if users:
                return DuolingoUser(users[0])
            return None
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching user {username}: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for user {username}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching user {username}: {e}")
        return None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello, {user.first_name}! 👋\n\n"
        "I'm a Duolingo Bot that can fetch statistics for Duolingo users.\n\n"
        "Use /help to see available commands."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = (
        "📚 *Available Commands:*\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/xp <username> - Get total XP for a Duolingo user\n"
        "/streak <username> - Get current streak for a Duolingo user\n"
        "/crowns <username> - Get total crowns for a Duolingo user\n\n"
        "*Example:*\n"
        "`/xp myusername123`\n\n"
        "Note: Username must be 3-16 characters (letters, numbers, dots, dashes, underscores)."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def xp_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /xp command to fetch user XP."""
    user = update.effective_user
    
    if not context.args or len(context.args) < 1:
        await update.message.reply_text(
            "Please provide a Duolingo username.\n"
            "Usage: /xp <username>\n"
            "Example: /xp myusername123"
        )
        return
    
    username = context.args[0]
    
    # Validate username format (3-16 chars, alphanumeric with .-_)
    if not (3 <= len(username) <= 16) or not all(c.isalnum() or c in '._-' for c in username):
        await update.message.reply_text(
            "Invalid username format. Username must be 3-16 characters "
            "and contain only letters, numbers, dots, dashes, or underscores."
        )
        return
    
    # Fetch user data
    duo_user = await fetch_duolingo_user(username)
    
    if duo_user:
        message = f"Hello {user.first_name}, the XP of {duo_user.username} is {duo_user.total_xp} ⭐"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(
            f"Sorry, I couldn't find the Duolingo user '{username}'. "
            "Please check the username and try again."
        )


async def streak_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /streak command to fetch user streak."""
    user = update.effective_user
    
    if not context.args or len(context.args) < 1:
        await update.message.reply_text(
            "Please provide a Duolingo username.\n"
            "Usage: /streak <username>\n"
            "Example: /streak myusername123"
        )
        return
    
    username = context.args[0]
    
    # Validate username format
    if not (3 <= len(username) <= 16) or not all(c.isalnum() or c in '._-' for c in username):
        await update.message.reply_text(
            "Invalid username format. Username must be 3-16 characters "
            "and contain only letters, numbers, dots, dashes, or underscores."
        )
        return
    
    # Fetch user data
    duo_user = await fetch_duolingo_user(username)
    
    if duo_user:
        message = f"Hello {user.first_name}, the streak of {duo_user.username} is: 🔥{duo_user.streak} days"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(
            f"Sorry, I couldn't find the Duolingo user '{username}'. "
            "Please check the username and try again."
        )


async def crowns_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /crowns command to fetch user crowns."""
    user = update.effective_user
    
    if not context.args or len(context.args) < 1:
        await update.message.reply_text(
            "Please provide a Duolingo username.\n"
            "Usage: /crowns <username>\n"
            "Example: /crowns myusername123"
        )
        return
    
    username = context.args[0]
    
    # Validate username format
    if not (3 <= len(username) <= 16) or not all(c.isalnum() or c in '._-' for c in username):
        await update.message.reply_text(
            "Invalid username format. Username must be 3-16 characters "
            "and contain only letters, numbers, dots, dashes, or underscores."
        )
        return
    
    # Send typing action while fetching data
    await update.message.chat.send_action(action="typing")
    
    # Fetch user data
    duo_user = await fetch_duolingo_user(username)
    
    if duo_user:
        message = f"Hi {user.first_name}, the user {duo_user.username} has: 👑{duo_user.crowns} crowns"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(
            f"Sorry, I couldn't find the Duolingo user '{username}'. "
            "Please check the username and try again."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """Start the bot."""
    # Get bot token from environment variable
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        print("Error: TELEGRAM_BOT_TOKEN environment variable is required.")
        print("Please set it before running the bot.")
        return
    
    # Log startup (without revealing token)
    logger.info("Starting Duolingo Bot for Telegram")
    logger.info("Version: Python 2.0")
    logger.info("Developed by Xillegas")
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("xp", xp_command))
    application.add_handler(CommandHandler("streak", streak_command))
    application.add_handler(CommandHandler("crowns", crowns_command))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Run the bot
    logger.info("Bot is running... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
