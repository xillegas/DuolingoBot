# Duolingo bot for Telegram
require_relative 'user'

require 'telegram/bot'
require 'open-uri'
require 'json'
require 'dotenv'

Dotenv.load('.env')

token = ENV['TOKEN_TELEGRAM']

def fetch_user(username_recieved)
  url = "https://www.duolingo.com/2017-06-30/users?username=#{username_recieved}"
  duohash_serialized = URI.open(url).read
  duohash = JSON.parse(duohash_serialized)
  User.new(duohash['users'][0]) unless duohash['users'].empty?
end

puts "Duolingo Bot for Telegram"
puts "Version 1.0"
puts "Developed by Xillegas"

Telegram::Bot::Client.run(token) do |bot|
  bot.listen do |message|
    # puts "ok"
    if message.instance_of?(Telegram::Bot::Types::Message) && message.text.instance_of?(String)
      attempt = message.text.split
      if attempt[0] == '/starts'
        bot.api.send_message(chat_id: message.chat.id, text: "Hello, #{message.from.first_name}.")
      elsif attempt[0] == '/xp' && /^[a-zA-Z0-9._-]{3,16}$/.match?(attempt[1])
        duo_user = fetch_user(attempt[1])
        unless duo_user.nil?
          msg = "Hello #{message.from.first_name}, the xp of #{duo_user.username} is #{duo_user.total_xp}"
          bot.api.send_message(chat_id: message.chat.id, text: msg)
        end
      elsif attempt[0] == '/streak' && /^[a-zA-Z0-9._-]{3,16}$/.match?(attempt[1])
        duo_user = fetch_user(attempt[1])
        unless duo_user.nil?
          msg = "Hello #{message.from.first_name}, the streak of #{duo_user.username} is: 🔥#{duo_user.streak} days"
          bot.api.send_message(chat_id: message.chat.id, text: msg)
        end
      elsif attempt[0] == '/crowns' && /^[a-zA-Z0-9._-]{3,16}$/.match?(attempt[1])
        bot.api.send_chat_action(chat_id: message.chat.id, action: 'typing')
        duo_user = fetch_user(attempt[1])
        unless duo_user.nil?
          msg = "Hi #{message.from.first_name}, the user #{duo_user.username} has: 👑#{duo_user.crowns} crowns"
          bot.api.send_message(chat_id: message.chat.id, text: msg)
        end
      elsif attempt[0] == '/stoped'
        bot.api.send_message(chat_id: message.chat.id, text: "Bye, #{message.from.first_name}")
      end
    end
  end
end
