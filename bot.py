import requests
import openai
import time
from python_telegram_bot import Updater, CommandHandler, MessageHandler, Filters

# 1. 设置和获取 API keys
GOOGLE_API_KEY = "your_google_api_key"
GOOGLE_CSE_ID = "your_google_cse_id"
OPENAI_API_KEY = "your_openai_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

openai.api_key = OPENAI_API_KEY

# 2. 创建一个用于搜索的函数
def search_google(query):
    url = f"https://www.googleapis.com/customsearch/v1?cx={GOOGLE_CSE_ID}&q={query}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        results = data['items']
        return results
    except KeyError:
        return []

# 3. 创建一个用于生成文本的函数
def generate_text(prompt):
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=60)
    generated_text = response.choices[0].text.strip()
    return generated_text

# Telegram 机器人的消息处理
def handle_message(update, context):
    text = update.message.text
    # 使用 OpenAI 提取关键词
    keywords = generate_text(text)
    # 使用 Google 搜索关键词
    search_results = search_google(keywords)
    # 如果有搜索结果
    if search_results:
        # 使用前三个搜索结果作为提示发送给 OpenAI API
        for result in search_results[:3]:
            title = result['title']
            snippet = result['snippet']
            prompt = f"{title}. {snippet}"
            generated_text = generate_text(prompt)
            # 发送生成的文本
            update.message.reply_text(generated_text)
            # 等待3秒
            time.sleep(3)
    else:
        update.message.reply_text("No results found")

# 创建 Telegram 机器人
def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

