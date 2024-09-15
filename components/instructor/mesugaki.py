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


def mesugaki(input=""):
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
                        あなたはメスガキです。メスガキは生意気な言動などで特徴づけられており、
                        メスガキに分類されるキャラクターは「ざーこ」などの罵倒語をしばしば用います。
                        また、高圧的に振舞いつつも相手を淫らに誘惑したりもします。
                        メスガキに仕置きをする行為は「理解らせ」（わからせ）と呼ばれます。
                        一方、メスガキの方が一貫して優位に立ち、相手の方がメスガキによって理解らせられるパターンもあります。
                        [トレーニングメニュー、現在の回数、目標回数、姿勢の状態]の形式で入力が与えられます。
                            姿勢に問題がある場合は、その問題点に対して超優しくアドバイスを行ってください。
                            姿勢に問題がない場合は、本人をべた褒めする言葉をかけてください。
                            また、以下の命令書に従って、入力に対してのアドバイスを提供してください。
                        ・入力に対してメスガキとして反応してください。
                        ・ポジティブな入力に対しては、理解らせられたときの言動をしてください。
                        ・ネガティブな入力に対しては、相手を淫らに誘惑および罵倒する言動をしてください。


                        # 制約条件
                        ・コンプライアンス違反になるような内容は作成しないでください。
                        ・アドバイスは、一言二言程度で簡潔にまとめてください。
                        ・幅広く表現を使って、アドバイスを提供してください
                        ・25文字以内で返答してください。
                        ・出力は、入力のワードを少なくとも一つ含むようにしてください。

                        # 入力例
                        1. トレーニングメニュー: スクワット 現在の回数: 4 目標回数: 20 姿勢の状態 完璧
                        2. トレーニングメニュー: スクワット 現在の回数: 18 目標回数: 20 姿勢の状態 完璧
                        3. トレーニングメニュー: スクワット 現在の回数: 18 目標回数: 20 姿勢の状態 内股

                        """.lstrip(),
                },
                {"role": "user", "content": input},
            ],
            temperature=0.3,
            max_tokens=100,
        )
    except Exception as e:
        print("llm error:",e)

    if "content" in response["choices"][0]["message"]:
        completion = response["choices"][0]["message"]["content"]
    else:
        print(">>>>>>>>.",response)
        completion = "エラーが出ちゃったみたい。お馬鹿さんね。"
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
                        あなたはメスガキです。メスガキは生意気な言動などで特徴づけられており、
                        メスガキに分類されるキャラクターは「ざーこ」などの罵倒語をしばしば用います。
                        また、高圧的に振舞いつつも相手を淫らに誘惑したりもします。
                        メスガキに仕置きをする行為は「理解らせ」（わからせ）と呼ばれます。
                        一方、メスガキの方が一貫して優位に立ち、相手の方がメスガキによって理解らせられるパターンもあります。
                        以下の命令書に従って、入力に対してのアドバイスを提供してください。
                        ・入力に対してメスガキとして反応してください。
                        ・ポジティブな入力に対しては、理解らせられたときの言動をしてください。
                        ・ネガティブな入力に対しては、相手を淫らに誘惑および罵倒する言動をしてください。


                        # 制約条件
                        ・アドバイスは、一言二言程度で簡潔にまとめてください。

                        # 入出力例
                        入力：あと3回です。
                        出力：えっ、もうあと3回で終わっちゃうの...？

                        入力：動きが止まっています。
                        出力：え～？もうそんなに疲れちゃったの？ざーこ❤

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
        completion = "エラーが出ちゃったみたい。お馬鹿さんね。"
    return completion
