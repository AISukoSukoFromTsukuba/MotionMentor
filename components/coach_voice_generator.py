import requests
import json
import pyaudio


def vvox_test(text: str, speaker: int):
    # エンジン起動時に表示されているIP、portを指定
    host = "127.0.0.1"
    port = 50021

    # 音声化する文言と話者を指定(3で標準ずんだもんになる)
    params = (
        ("text", text),
        ("speaker", speaker),
    )

    # 音声合成用のクエリ作成
    query = requests.post(f"http://{host}:{port}/audio_query", params=params).json()
    query["speedScale"] = 1.5

    # 音声合成を実施
    synthesis = requests.post(
        f"http://{host}:{port}/synthesis",
        headers={"Content-Type": "application/json"},
        params=params,
        data=json.dumps(query),
    )

    # 再生処理
    voice = synthesis.content
    pya = pyaudio.PyAudio()

    # サンプリングレートが24000以外だとずんだもんが高音になったり低音になったりする
    stream = pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    stream.write(voice)
    stream.stop_stream()
    stream.close()
    pya.terminate()


if __name__ == "__main__":
    text = "まだまだいけるよ！頑張って！"
    vvox_test(text, 4)
