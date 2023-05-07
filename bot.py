import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 设置您的 API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your AI assistant. Just type your question or message and I'll help you.")

def chat(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    model_engine = "gpt-3.5-turbo"

    # 向 OpenAI API 发送请求
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "user", "content": user_text}
        ],
    )

    # 获取并发送回复
    reply = response.choices[0].message["content"].strip()
    update.message.reply_text(reply)

def main() -> None:
    updater = Updater(TELEGRAM_API_TOKEN)

    # 注册处理程序
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    # 启动机器人
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
