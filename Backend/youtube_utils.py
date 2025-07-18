from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs
from nltk.tokenize import sent_tokenize
from whisper import load_model
import yt_dlp
import os

def extract_video_id(url):
    query = parse_qs(urlparse(url).query)
    return query["v"][0]

def download_audio(url, output="audio.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_with_whisper(audio_path="audio.mp3"):
    model = load_model("base")
    result = model.transcribe(audio_path)
    return result['text']

def sentence_chunk(text, max_words=100):
    sentences = sent_tokenize(text)
    chunks, current = [], []
    count = 0

    for sent in sentences:
        words = sent.split()
        if count + len(words) > max_words:
            chunks.append(" ".join(current))
            current, count = [], 0
        current.extend(words)
        count += len(words)
    if current:
        chunks.append(" ".join(current))
    return chunks

def get_transcript(url):
    video_id = extract_video_id(url)
    try:
        raw_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([seg["text"] for seg in raw_transcript])
    except Exception:
        download_audio(url, "audio.mp3")
        full_text = transcribe_with_whisper("audio.mp3")

    chunks = sentence_chunk(full_text)
    return video_id, full_text, chunks