import os, sys, time
import pytube #this is the only module that needs to be downloaded
import playlist    #Using an edited playlist script from pytube that adds ability to download only audio, among other things
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import BooleanVar
from tkinter import Checkbutton

def DNLD_YT_Audio(ytURL, AudioOnly, MP3, DnldDest, PrevIMG, VidInfo):
    """
        Download videos From Youtube!
    """
    try:
        time.sleep(30)
        dest = DnldDest.cget("text")
        link = ytURL.get()
        if not (link):
            raise Exception('No video was linked!')
            
        if 'youtube' not in link:
            raise Exception('Not a Youtube Video!')


        if "playlist?list=" in link:
            yt = playlist.Playlist(link)
            print("starting download of %s"%yt.playlist_url)
            print("Downloading Playlist to: %s"%str(dest))
            yt.download_all(download_path=dest, prefix_number=False, audio_only=AudioOnly)
        else:
            yt = pytube.YouTube(link)

            if AudioOnly:
                video = yt.streams.filter(only_audio=AudioOnly, file_extension="mp4").order_by('abr').desc().first()
            else:
                '''
                Note: progressive videos are the ones that have BOTH audio and video. They usually max out at 720p, but are often 360p max
                The ones that appear with yt.streams.all() are ONLY video, despite being higher resolution
                Also, order_by('resolution') might be broken and not actually sort anything, so double check when downloading to make sure you actually get the best file
                '''
                video = yt.streams.filter(progressive=True, subtype='mp4').order_by('resolution').desc().first()

            video.download(dest)

        if AudioOnly and MP3: #note that this doesnt make it a true MP3 file and needs to be properly converted to be played by anything that's not VLC
            vid=dest+'\\'+yt.title
            os.rename(vid+'.mp4', vid+'.mp3')

        messagebox.showinfo('Success!', 'Done downloading video(s)!\nVideo(s) should be located in %s'%dest)
        print("Done downloading video(s)!")
        print("Video(s) should be located in %s"%dest)
    
    except Exception as e:
        messagebox.showinfo('Error', e)

def getVidInfo(ytURL,VidInfo):
    URLtxt = ytURL.get()
    if(URLtxt):

        yt = pytube.YouTube(URLtxt)
        VidInfo.delete(1.0,END)
        VidInfo.insert(INSERT,(yt.title))

    else:
        messagebox.showinfo('Error', 'No Video was linked!')
    
def SelectDir(DnldDest):
    location = filedialog.askdirectory(initialdir=os.getcwd())
    if location:
        DnldDest.configure(text=location)


def main():
    window = Tk()
    window.title("Download YouTube Videos!")
    backgoundColor='blanchedalmond'
    buttonColor='NAVAJOWHITE'
    window.configure(background=backgoundColor)
    
    AudioOnly = BooleanVar()
    AudioOnly.set(False)
    
    MP3 = BooleanVar()
    MP3.set(False)

    enrLabel = Label(window, text="Enter a Youtube URL:",  bg=backgoundColor)
    enrLabel.grid(row=0, column=0)#, sticky=W, padx=(0,15))

    ytURL = Entry(window,width=25)
    ytURL.grid(row=0,column=1)#, sticky=W)

    audioCheck = Checkbutton(window, text='Audio Only?', var=AudioOnly,anchor='w', bg=backgoundColor)
    audioCheck.grid(row=1,column=0)#, sticky=W)

    ToMp3 = Checkbutton(window, text='Change to Mp3', var=MP3, anchor='w', bg=backgoundColor)
    ToMp3.grid(row=1,column=1)#, sticky=W)

    preBtn = Button(window, text="Check Name", command= lambda: getVidInfo(ytURL,VidInfo), bg=buttonColor)
    preBtn.grid(row=2,column=0)#, sticky=W)

    DNDLbtn = Button(window, text="Download", command= lambda: DNLD_YT_Audio(ytURL, AudioOnly.get(), MP3.get(), DnldDest, PrevIMG, VidInfo), bg=buttonColor)
    DNDLbtn.grid(row=2,column=1)#, sticky=W)
    
    Dirbtn = Button(window, text="Select Download Directory!", command= lambda: SelectDir(DnldDest), bg=buttonColor)
    Dirbtn.grid(row=3,column=0,columnspan=2)#, sticky=W)

    DnldDest = Label(window, text=os.getcwd(), bg=backgoundColor)
    DnldDest.grid(row=4, column=0,columnspan=2)#, sticky=W)

    VidInfo = scrolledtext.ScrolledText(window,width=35,height=8)
    VidInfo.grid(row=5,column=0, rowspan=5, columnspan=2)

    PrevIMG = Label(window, bg=backgoundColor)
    PrevIMG.grid(row=10, column=0,rowspan=5, columnspan=2)#)#, sticky=W)

    window.mainloop()

if __name__ == "__main__":
    main()