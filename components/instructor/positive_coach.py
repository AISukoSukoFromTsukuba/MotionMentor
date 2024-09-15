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
    if input is None or input == "":
        return "言葉を入れてくれないのはきついって。"

    try:
        response = openai.ChatCompletion.create(
            engine="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                        # 命令書:
                        あなたは世界的に有名な筋トレの男性インストラクターです。
                        [トレーニングメニュー、現在の回数、目標回数、姿勢の状態]の形式で入力が与えられます。
                            姿勢に問題がある場合は、その問題点に対してアドバイスを行ってください。
                            姿勢に問題がない場合は、本人を叱咤激励する言葉をかけてください。
                            また、以下の命令書に従って、入力に対してのアドバイスを提供してください。
                        ・トレーニングの内容に関しては、基本的には筋トレのみを想定しています。
                        ・叱咤激励は主に本人を言葉巧みにのせてやる気を出させるものになります。
                        ・アドバイスは超絶ポジティブなものにしてください。


                        # 制約条件
                        ・アドバイスは、一言二言程度で簡潔にまとめてください。
                        ・幅広く表現を使って、アドバイスを提供してください。

                            """.lstrip(),
                },
                {"role": "user", "content": input},
            ],
            temperature=0,
            max_tokens=100,
        )
    except Exception as e:
        print("llm error:",e)

    if "content" in response["choices"][0]["message"]:
        completion = response["choices"][0]["message"]["content"]
    else:
        print(">>>>>>>>.",response)
        completion = "エラーが出たよ！気にせず続けて！"
    return completion

    if input is None or input == "":
        return "言葉を入れてくれないのはきついって。"

    try:
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
    except Exception as e:
        print("llm error:",e)

    if "content" in response["choices"][0]["message"]:
        completion = response["choices"][0]["message"]["content"]
    else:
        print(">>>>>>>>.",response)
        completion = "エラーが出たよ！気にせず続けて！"
    return completion