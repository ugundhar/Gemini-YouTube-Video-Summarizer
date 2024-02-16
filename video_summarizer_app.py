import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import os

load_dotenv()  # Load environment variables

# Importing Gemini for summarization
import google.generativeai as genai

# Configuring Gemini with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for summarization
prompt = "You are using the YouTube Video Summarizer. Please summarize the video within 250 words: "


# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


# Function to generate summary using Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# UI part
st.title("YouTube Transcript Summarizer")

# Input field for YouTube link
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    # Extracting video ID from YouTube link
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Button to get detailed notes
if st.button("Get Video Summary"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Video Summary:")
        st.write(summary)
