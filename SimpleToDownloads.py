import pytube
video_url = 'https://www.youtube.com/watch?v=tv8BRQaFlLU' # paste here your Youube videos' url
youtube = pytube.YouTube(video_url)
video = youtube.streams.first()
video.download('/Users/reper/Downloads')