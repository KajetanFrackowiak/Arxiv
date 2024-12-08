from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy import AudioFileClip
from gtts import gTTS

def create_video_summary(articles):
    text = "\n".join([f"{i+1}. {article['summary']}" for i, article in enumerate(articles)])
    tts = gTTS(text, lang="en")
    tts.save("audio.mp3")

    clips = []
    for i, article in enumerate(articles):
        clip = TextClip(text="Three popular new papers", font='font.ttf', font_size=50, color='white', size=(720, 1280))
        clip = clip.with_duration(5).with_position("center")
        clips.append(clip)

    video = CompositeVideoClip(clips)
    audio = AudioFileClip("audio.mp3")
    video = video.with_audio(audio)
    video.write_videofile("arxiv_summary.mp4", fps=24)