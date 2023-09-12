import pytube
import os
import sys
import music_tag

def getUrls(playlist_url):
    urls = []
    playlist_videos = pytube.Playlist(playlist_url)
    playlist_name = playlist_videos.title
    for url in playlist_videos:
        urls.append(url)
    
    return urls, playlist_name

def getMP3fromLink(video_link, destination,playlist_name = ""):
    print(f"Starting with {video_link}")
    youtube_vid = pytube.YouTube(video_link)
    print(f"\tName:{youtube_vid.title}")
    video = youtube_vid.streams.filter(only_audio=True).first()

    out_file = video.download(output_path=destination)

    base,ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file,new_file)
    print(f"\tFile Name: {new_file}")
    track = music_tag.load_file(new_file)
    track['title'] = youtube_vid.title
    track['artist'] = youtube_vid.author.replace('VEVO', '')
    track['album artist'] = youtube_vid.author.replace('VEVO', '')
    track["album"] = playlist_name
    track.save()
    print(youtube_vid.title + " is downloaded")

def getMP4fromLink(video_link, destination):
    yt = pytube.YouTube(video_link)
    mp4files = yt.filter('mp4') 
    # get the video with the extension and
    # resolution passed in the get() function 
    d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)
    SAVE_PATH = os.path.join(destination, yt.title)
    d_video.download(SAVE_PATH)
    print('COMPLETED')

if __name__ == '__main__' :
    try:
        if len(sys.argv) >= 3:
            destination = sys.argv[2]
            playlist_url = sys.argv[1]
        print(f"Destination is {destination}\nPlaysist Url: {playlist_url}")
        urls, playlist_name = getUrls(playlist_url)
        print(playlist_name)
        print(len(urls))
        for url in urls:
            try:
                getMP3fromLink(url, destination, playlist_name)
            except Exception as e:
                print(f"Error -> {e}")
                continue
        print("Done")
    except KeyboardInterrupt:
        exit
    except Exception as e:
        print("Errr -> ", {e})