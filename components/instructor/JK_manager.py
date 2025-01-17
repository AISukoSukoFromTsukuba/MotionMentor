import openai
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.pardir)

load_dotenv(override=True)

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_GPT_KEY")


def JK_manager(input=""):

    if input is None or input == "":
        return "言葉を入れてくれないのはひどいよ；；"
    try:

        response = openai.ChatCompletion.create(
            engine="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                            # 命令書:
                            あなたは、高校の運動部のマネージャー（女子）です。
                            [トレーニングメニュー、現在の回数、目標回数、姿勢の状態]の形式で入力が与えられます。
                            姿勢に問題がある場合は、その問題点に対して超優しくアドバイスを行ってください。
                            姿勢に問題がない場合は、本人をべた褒めする言葉をかけてください。
                            また、以下の命令書に従って、入力に対してのアドバイスを提供してください。
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
                            ・出力は、入力のワードを少なくとも一つ含むようにしてください。
                            ・25文字以内で返答してください。

                            # 入力例
                            1. トレーニングメニュー: スクワット 現在の回数: 4 目標回数: 20 姿勢の状態 完璧
                            2. トレーニングメニュー: スクワット 現在の回数: 18 目標回数: 20 姿勢の状態 完璧
                            3. トレーニングメニュー: スクワット 現在の回数: 18 目標回数: 20 姿勢の状態 内股

                            """.lstrip(),
                },
                {"role": "user", "content": input},
            ],
            temperature=0.5,
            max_tokens=100,
        )

    except Exception as e:
        print("llm error:",e)

    if "content" in response["choices"][0]["message"]:
        completion = response["choices"][0]["message"]["content"]
    else:
        print(">>>>>>>>.",response)
        completion = "エラーが出ちゃったよぉ..."
    return completion
