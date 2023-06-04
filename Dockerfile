# Versión de Ruby a utilizar
FROM ruby:2.7.2

# Directorio de trabajo de la aplicación
WORKDIR /app

# Copiar los archivos de la aplicación al directorio de trabajo
COPY . .

# Instalar las dependencias de la aplicación
RUN bundle install

# Exponer el puerto utilizado por la aplicación
EXPOSE 80

# Ejecutar la aplicación utilizando el comando "ruby" y el archivo "bot.rb"
CMD bash start.sh
