import pytube
import os
import playlist    #Using an edited playlist script that adds ability to download only audio, among other things
import sys


import logging, sys
logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)
#I think in wondows the main console is tyed with the debug console, will test this on mac and a raspi to make sure main isnt being written to all the time




def DNLD_YT_Audio(link,dnldDest="default", AudioOnly=True, choice=False):
    """
        Download videos From Youtube!
        
        :param link:Provide a link to a youtube video or the root of a playlist

        :param dnldDest: (optional) Output path for the playlist If one is not specified, defaults to new folder in the current working directory called "downloads"

        :param Music: (optional) Download Audio only by default
    """

    if 'youtube' not in link:
        logging.debug("Not a Youtube Video")
        return False

    if "playlist?list=" in link:
        yt = playlist.Playlist(link)
    else:
        yt = pytube.YouTube(link)

    if dnldDest == "default":
        #dest = "D:/pythonProjects/downloads"
        
        dest = os.getcwd() + "\downloads"
        
    

    if "playlist?list=" in link:
        logging.debug("starting download of %s"%yt.playlist_url)
        logging.debug("Downloading Playlist to: %s"%str(dest))
        yt.download_all(download_path=dest, prefix_number=False, audio_only=AudioOnly)

    else:
        if choice == True:
            vids = yt.streams.filter(only_audio=AudioOnly,file_extension="mp4").order_by('abr').desc().all()
            for index in range(len(vids)):
                print(index,".",vids[index])

            print("Enter video you would like")
            n = int(input())
            video = vids[n]
        else:
            if AudioOnly == True:
                print("butts")
                video = yt.streams.filter(only_audio=AudioOnly, file_extension="mp4").order_by('abr').desc().first()
            else:
                print("not butts")
                video = yt.streams.filter(progressive=True, subtype='mp4').order_by('resolution').desc().first()
        

        logging.debug("starting download of %s"%yt.title)
        logging.debug("Downloading songs to: %s"%str(dest))
        video.download(dest)

    logging.debug("Done downloading video(s)!")
    #logging.debug("Video(s) should be located in %s"%dest)
    return True

def main():
    
    AudioOnly=True #Audio = True; Video = False

    print("This is the name of the script: ", sys.argv[0])
    print("Number of arguments: ", len(sys.argv))
    print("The arguments are: " , str(sys.argv))

    if len(sys.argv)==1: #should I make a UI come up if you did not include any in line arguments?
        link = input("Enter URL or leave empty to download a dodie song :D \n")
        if link=="":
            link= "https://www.youtube.com/watch?v=bKOIG1sIr0o"
    else:
        link=sys.argv[1]
        if "-v" in sys.argv:
            AudioOnly=True

            
    try:
        DNLD_YT_Audio(link, Music=AudioOnly)

    except Exception as e:
        print("Error occured")
        print(e)

if __name__ == "__main__":
    main()

