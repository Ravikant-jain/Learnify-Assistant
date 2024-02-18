#main file
from pprint import pprint
import requests
from pytube import YouTube
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import streamlit as st


from dotenv import load_dotenv


load_dotenv()
os.getenv("BART_API_KEY")



#creating Cache folder to store files
path= 'D:\Github\Edu-AiX'
cache_folder = os.path.join(path, 'Cache')
os.makedirs(cache_folder, exist_ok=True)
output_path= os.path.abspath(cache_folder)


#func which downloads yt video
def download_youtube_video(youtube_url, output_path='.', resolution='360p'):
    
    if os.path.exists(r'Cache/video01.mp4'):
        return 
    else:
        try:
            # Create a YouTube object
            youtube = YouTube(youtube_url)

            # Get the stream with the specified resolution
            video_stream = youtube.streams.get_by_resolution(resolution)

            if video_stream:
                # Download the video with the specified file name
                video_stream.download(output_path, filename='video01.mp4')

                print(f"Video download successful in {resolution} resolution! Saved as video01.mp4")
            else:
                print(f"Error: Video stream with {resolution} resolution not available.")
        except Exception as e:
            print(f"Error: {e}")

#func which extracts audio from the downloaded video
def extract_audio(video_path, output_audio_path):
    
    if os.path.exists(r'Cache\extracted-audio.mp3'):
        return
    else:    
        try:
            # Load the video clip
            video_clip = VideoFileClip(video_path)

            # Extract audio
            audio_clip = video_clip.audio

            # Save the audio to the specified output path
            output_audio_path = os.path.join(output_audio_path, 'extracted-audio.mp3')
            audio_clip.write_audiofile(output_audio_path)

            print("Audio extraction successful!")
        except Exception as e:
            print(f"Error: {e}")

#func which calls all the api and returns the story and summery
def API():
    res={}

    
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-medium.en"
    headers = {"Authorization": "Bearer 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"}

    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    print('done till here')
    output = query(r"D:\Github\Edu-AiX\Cache\extracted-audio.mp3")
    try:
        story=output['text']
    except:
        print('By-passing due to API issue')
        with open(r'D:\Github\Edu-AiX\TextAi.json', 'r') as file:
            quiz_data = json.load(file)
        story=quiz_data['Story']
    #summerise Ai

    API_URL2 = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
    headers2 = {"Authorization": os.getenv("BART_API_KEY")}

    def query2(payload):
        response = requests.post(API_URL2, headers=headers2, json=payload)
        return response.json()
    
    output2 = query2({"inputs": story})
    xo=output2[0]
    summery=xo['summary_text']
    
    res['Story']=story
    res['Summery']=summery
    
    print("transcribe done")
    return res


@st.cache_data
def AiText(url):
    print(f'Cooking initialized...\n')
    print(f'Stage I: Video download\n')
    download_youtube_video(url, output_path, '360p')
    print(f'\nStage II: Audio Extraction\n')
    extract_audio(r'D:\Github\Edu-AiX\Cache\video01.mp4', output_path)
    print(f'\nLast stage : APIs Triggered')
    ans=API()
    print(f'\nGot response successfully\nGoodBye\n')

    return ans



#for testing
# yt_url = 'https://www.youtube.com/watch?v=RP2gIgRL6Yw'

# X=AiText(yt_url)











#UI starts from here 


st.set_page_config(layout='wide')

# Hardcoded YouTube video URL which could be changed
yt_url = 'https://www.youtube.com/watch?v=RP2gIgRL6Yw'


X=AiText(yt_url)

import json
file_path = r"Jsons\TextAi.json"
with open(file_path, "w") as json_file:
    json.dump(X, json_file)

st.title("Lecture")

# Create two columns with the specified ratio
col1, col2 = st.columns([0.7, 0.3])

# Left column: YouTube video player
with col1:
    st.video(yt_url)

# Right column: Summarize button and bigger text box
with col2:

    st.text_area("Video Transcription:",X['Story'], height=400)

    if st.button("Summarize"):
        
        
        st.text_area("Video Summary:",X['Summery'], height=400)