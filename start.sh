#!/bin/sh

echo "Enter your TELEGRAM_API_TOKEN:"
read telegram_api_token

echo "Enter your OPENAI_API_KEY:"
read openai_api_key

docker build -t telegram-openai-bot-pro .

docker run --name telegram-openai-bot-pro -d -e TELEGRAM_API_TOKEN=$telegram_api_token -e OPENAI_API_KEY=$openai_api_key telegram-openai-bot-pro
