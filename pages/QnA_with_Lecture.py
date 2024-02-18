#main file
from pprint import pprint
import requests
from pytube import YouTube
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import streamlit as st
import json


from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')



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
    if not os.path.exists(r'Cache/trpt.json'):
        output = query(r"D:\Github\Edu-AiX\Cache\extracted-audio.mp3")
        story=output['text']
        file_path = r"Cache\trpt.json"
        with open(file_path, "w") as json_file:
            json.dump(story, json_file)
    else:
        print('By-passing due to API issue')
        with open(r'D:\Github\Edu-AiX\Cache\trpt.json', 'r') as file:
            quiz_data = json.load(file)
        story=quiz_data
    
    return story
# import os
# import json
# import requests
# print(API())



def poopmt(que,trpt):
    poompt = '''
    I was studying from a youtube video, and I have a question, i am giving you transcript as context , feel free to use your knowledge to answer my question.
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:{}
    Question: {}

'''.format(trpt,que)
    return poompt



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


def ans(promt):
    answer = model.generate_content(promt)
    return answer.text

#for testing
# yt_url = 'https://www.youtube.com/watch?v=RP2gIgRL6Yw'

# X=AiText(yt_url)
# prmt=poopmt('What is the moral of the story',X)
# a1=ans(prmt)
# print(a1)



#UI starts from here 


st.set_page_config(layout='wide')

# Hardcoded YouTube video URL which could be changed
yt_url = 'https://www.youtube.com/watch?v=RP2gIgRL6Yw'


X=AiText(yt_url)

st.title("Lecture QnA ")

# Create two columns with the specified ratio
col1, col2 = st.columns([0.7, 0.3])

# Left column: YouTube video player
with col1:
    st.video(yt_url)

# Right column: Summarize button and bigger text box
with col2:

    input=st.text_input("Input your question ",key="input")
    submit=st.button("Ask the question")

    if submit and input:
        prmt=poopmt(input,X)
        a1=ans(prmt)
        st.write(a1)