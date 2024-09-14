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


def mesugaki(input=""):
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
    return response["choices"][0]["message"]["content"]
