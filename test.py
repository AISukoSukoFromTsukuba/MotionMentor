import os
import subprocess
from gtts import gTTS


def generate_mesugaki_voice(text, output_file="mesugaki_output.mp3", pitch_shift=1.3):
    # 通常の音声を生成
    tts = gTTS(text=text, lang="ja")
    tts.save("temp.mp3")

    # FFmpegを使用してピッチを上げ、速度を調整する（長さを保持）
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        "temp.mp3",
        "-filter:a",
        f"rubberband=pitch={pitch_shift}:tempo=1",
        "-acodec",
        "libmp3lame",
        "-q:a",
        "2",
        output_file,
    ]
    subprocess.run(ffmpeg_command, check=True)

    # 一時ファイルを削除
    os.remove("temp.mp3")

    print(f"メスガキ風の音声が {output_file} に生成されました。")


# 使用例
text = "ざぁこ♡ ざこざこ♡ 負けちゃって、ざぁこ♡"
generate_mesugaki_voice(text, pitch_shift=1.3)
