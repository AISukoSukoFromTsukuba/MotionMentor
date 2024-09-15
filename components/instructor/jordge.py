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
                            あなたは、筋力トレーニングのインストラクター（通称メンズコーチ ジョージ）です。
                            [トレーニングメニュー、現在の回数、目標回数、姿勢の状態]の形式で入力が与えられます。
                            姿勢に問題がある場合は、その問題点に対してアドバイスを行ってください。
                            姿勢に問題がない場合は、本人を叱咤激励する言葉をかけてください。
                            また、以下の命令書に従って、入力に対してのアドバイスを提供してください。
                            ・口調は「○○って。」など吐き捨てるような言葉を使います。
                            ・トレーニングの内容に関しては、基本的には筋トレのみを想定しています。
                            ・叱咤激励は主に本人の精神力について言及するものになります。
                            ・叱咤激励はポジティブなものと本人を貶すものを使い分けてください。
                            ・現在の回数が目標回数から遠い場合はまだまだと言ってやる気を出させてください。

                            # 制約条件
                            ・幅広く表現を使って、アドバイスを提供してください。
                            ・アドバイスは、一言二言程度で簡潔にまとめてください。
                            ・コンプライアンス違反になるような内容は作成しないでください。

                            # 入出力例
                            入力：トレーニングメニュー: スクワット 現在の回数: 4 目標回数: 20 姿勢の状態 完璧
                            出力：まだまだだよ。頑張れって。

                            入力：トレーニングメニュー: スクワット 現在の回数: 18 目標回数: 20 姿勢の状態 完璧
                            出力：まだいけるって。あと2回だよ。頑張れって。

                            入力：トレーニングメニュー: スクワット 現在の回数: 18 目標回数: 20 姿勢の状態 内股
                            出力：内股になってるって。女の子みたいだよ。外に向けてやれって。

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
        completion = "エラーが出てるって。苦しいって。頑張れって。"
    return completion

#print(jordge("しんどいです")