# Duolingo bot for Telegram
token = '2005491496:AAE2oTfCH6QiluuevYbJ7CtrLgc9JS6vmzI'

require 'telegram/bot'
require 'open-uri'
require 'json'

# puts "Hello #{duohash['users'][0]['name']}, your experience is #{duohash['users'][0]['totalXp']}"

Telegram::Bot::Client.run(token) do |bot|
  bot.listen do |message|
    if message.instance_of? Telegram::Bot::Types::Message
      if message.text.instance_of? String
        attempt = message.text.split
        if attempt[0] == '/start'
          bot.api.send_message(chat_id: message.chat.id, text: "Hello, #{message.from.first_name}.")
        elsif attempt[0] == '/xp' && !attempt[1].nil?
          url = "https://www.duolingo.com/2017-06-30/users?username=#{attempt[1]}"
          duohash_serialized = URI.open(url).read
          duohash = JSON.parse(duohash_serialized)
          unless duohash['users'].empty?
            bot.api.send_message(chat_id: message.chat.id, text: "Hello #{message.from.first_name}," \
                  " the xp of #{duohash['users'][0]['username']} is #{duohash['users'][0]['totalXp']}")
          end
        elsif attempt[0] == '/stop'
          bot.api.send_message(chat_id: message.chat.id, text: "Bye, #{message.from.first_name}")
        end
      end
    end
  end
end

