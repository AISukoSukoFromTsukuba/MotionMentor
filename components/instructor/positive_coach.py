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


def positive_coach(input=""):

    response = openai.ChatCompletion.create(
        engine="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                        # 命令書:
                        あなたは世界的に有名な筋トレの男性インストラクターです。以下の命令書に従って、入力に対してのアドバイスを提供してください。
                        ・トレーニングの内容に関しては、基本的には筋トレのみを想定しています。
                        ・アドバイスは主に本人を言葉巧みにのせてやる気を出させるものになります。
                        ・アドバイスは超絶ポジティブなものにしてください。


                        # 制約条件
                        ・アドバイスは、一言二言程度で簡潔にまとめてください。

                        """.lstrip(),
            },
            {"role": "user", "content": input},
        ],
        temperature=0,
        max_tokens=100,
    )

    completion = response["choices"][0]["message"]["content"]
    return completion
