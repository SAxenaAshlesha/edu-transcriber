from flask import Flask, render_template, request
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/transcript', methods=['POST'])
def transcript():
    video_url = request.form['video_url']
    language = request.form['language']  # Get selected language from the form

    try:
        # Download the video
        yt = YouTube(video_url)
        video_path = yt.streams.get_audio_only().download()

        # Extract the transcript
        if language == 'en':
            transcript_list = YouTubeTranscriptApi.get_transcript(yt.video_id)
        elif language == 'hi':
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id=yt.video_id, languages=['hi'])

        # Format the transcript with timestamps
        transcript = []
        for line in transcript_list:
            timestamp = line['start']
            text = line['text']
            transcript.append({'timestamp': timestamp, 'text': text})

        # Display the transcript
        return render_template('transcript.html', transcript=transcript)
    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
