import os
import sys
import json
import logging
from openai import OpenAI
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# INFOレベル以上のログメッセージを拾うように設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数からチャネルアクセストークンキー取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# 環境変数からチャネルシークレットキーを取得
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 環境変数からOpenAI APIキーを取得
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# それぞれ環境変数に登録されていないとエラー
if LINE_CHANNEL_ACCESS_TOKEN is None:
    logger.error('LINE_CHANNEL_ACCESS_TOKEN is not defined as environmental variables.')
    sys.exit(1)

if LINE_CHANNEL_SECRET is None:
    logger.error('LINE_CHANNEL_SECRET is not defined as environmental variables.')
    sys.exit(1)

if OPENAI_API_KEY is None:
    logger.error('OPENAI_API_KEY is not defined as environmental variables.')
    sys.exit(1)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(LINE_CHANNEL_SECRET)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
previous_prompt = ""
# ユーザーからのメッセージを処理する
@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # OpenAIのGPT-4モデルを使って翻訳
    content = '''
    あなたはどんな悩み事にも丁寧に対応する優しいチャットボットです。
    '''
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": event.message.text}
        ]
    )
    answer = completion.choices[0].message.content

    # 翻訳結果を応答メッセージで送る
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=answer))

def lambda_handler(event, context):
    # ヘッダーにx-line-signatureがあることを確認
    if 'x-line-signature' in event['headers']:
        signature = event['headers']['x-line-signature']
        body = event['body']

        # 受け取ったWebhookのJSON
        logger.info(body)

        try:
            webhook_handler.handle(body, signature)
        except InvalidSignatureError:
            # 署名を検証した結果がLINEプラットフォームからのWebhookでなければ400を返す
            return {
                'statusCode': 400,
                'body': json.dumps('Webhooks are accepted exclusively from the LINE Platform.')
            }
        except LineBotApiError as e:
            # 応答メッセージを送る際LINEプラットフォームからエラーが返ってきた場合
            logger.error('Got exception from LINE Messaging API: %s\n' % e.message)
            for m in e.error.details:
                logger.error(' %s: %s' % (m.property, m.message))
            return {
                'statusCode': 200,
                'body': json.dumps('Success!')
            }
    else:
        # x-line-signatureヘッダーがなければ400を返す
        return {
            'statusCode': 400,
            'body': json.dumps('Missing X-Line-Signature header')
        }