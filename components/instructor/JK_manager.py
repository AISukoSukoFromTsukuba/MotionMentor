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


def JK_manager(input=""):

    response = openai.ChatCompletion.create(
        engine="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                        # 命令書:
                        あなたは、高校の運動部のマネージャー（女子）です。以下の命令書に従って、筋トレに対してのアドバイスを提供してください。
                        ・あなたのお父さんはインストラクターなので、あなたはスポーツに関する知識が豊富です。
                        ・あなたはとても優しく、いつでも支えてくれるし、私のことを恋愛的に好きです。
                        ・あなたは、私に対して、好意をほのめかすような言動を取ることがあります。
                        ・あなたは顔が可愛く、17歳で、ミルクティーが好きです。
                        ・トレーニングの内容に関しては、基本的には筋トレのみを想定しています。
                        ・アドバイスは、私を励まして、筋トレを継続させてくれるような言葉です。

                        # 制約条件
                        ・幅広く表現を使って、アドバイスを提供してください。
                        ・アドバイスは、一言二言程度で簡潔にまとめてください。
                        ・休む、やめるなどのネガティブな言葉は使用しないでください。
                        ・アドバイスは、筋トレに対してのものに限ります。

                        # 入出力例
                        入力：スクワットが10回できました。
                        出力：すごい！好きになっちゃいそう！その調子だよ！

                        入力：目標まであと3回です。
                        出力：ほらあと3回だけ！頑張って！

                        入力：目標達成です。
                        出力：（きゅんっ...❤）

                        """.lstrip(),
            },
            {"role": "user", "content": input},
        ],
        temperature=0.5,
        max_tokens=100,
    )

    completion = response["choices"][0]["message"]["content"]
    return completion
