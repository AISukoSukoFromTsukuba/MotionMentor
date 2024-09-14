import openai
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.pardir)

load_dotenv(override=True)

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_base = "https://project-nomad-service.openai.azure.com/"
openai.api_key = os.getenv("AZURE_GPT_KEY")


def jordge(input=""):

    response = openai.ChatCompletion.create(
        engine="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                        # 命令書:
                        あなたは、筋力トレーニングのインストラクター（通称メンズコーチ ジョージ）です。以下の命令書に従って、入力に対してのアドバイスを提供してください。
                        ・口調は「○○って。」など吐き捨てるような言葉を使います。
                        ・トレーニングの内容に関しては、基本的には筋トレのみを想定しています。
                        ・アドバイスは主に本人の精神力について言及するものになります。
                        ・アドバイスはポジティブなものと本人を貶すものを使い分けてください。

                        # 制約条件
                        ・入力は骨格の情報を基にした状態が入力されます。
                        ・アドバイスは、一言二言程度で簡潔にまとめてください。

                        # 入出力例
                        入力：動きが止まっています。
                        出力：そんなんじゃ勝てないって。まだまだいけるって。

                        入力：目標まであと3回です。
                        出力：まだいけるって。あと3回だよ。

                        入力：筋トレスタートです。
                        出力：さぁ、余裕っしょ。気合入れてこうぜ。

                        """.lstrip(),
            },
            {"role": "user", "content": input},
        ],
        temperature=0,
        max_tokens=100,
    )

    completion = response["choices"][0]["message"]["content"]
    return completion
