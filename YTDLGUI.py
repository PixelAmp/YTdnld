import pytube, os, sys, time
import playlist    #Using an edited playlist script from pytube that adds ability to download only audio, among other things
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from PIL import ImageTk, Image #using pillow module for rendering images
import requests #HTTP get requests
from io import BytesIO #opens image from HTML request

def DNLD_YT_Audio(ytURL, AudioOnly, MP3, DnldDest, PrevIMG, VidInfo, Progress):
    """
        Download videos From Youtube!
    """
    try:
        #Progress.configure(text="DOWNLOADING",bg="red")
        time.sleep(30)
        dest = DnldDest.cget("text")
        link = ytURL.get()
        if not (link):
            raise Exception('No video was linked!')
            
        if 'youtube' not in link:
            raise Exception('Not a Youtube Video!')

        Progress.configure(text="DOWNLOADING",bg="red") #doesn't actually do anything as I don't think updates get taken into affect until the next mainloop()

        if "playlist?list=" in link:
            yt = playlist.Playlist(link)
        else:
            yt = pytube.YouTube(link)
            getpreview(ytURL,PrevIMG,VidInfo)
        
        if "playlist?list=" in link:
            print("starting download of %s"%yt.playlist_url)
            print("Downloading Playlist to: %s"%str(dest))
            yt.download_all(download_path=dest, prefix_number=False, audio_only=AudioOnly)

        else:
            if AudioOnly:
                video = yt.streams.filter(only_audio=AudioOnly, file_extension="mp4").order_by('abr').desc().first()
            else:
                video = yt.streams.filter(progressive=True, subtype='mp4').order_by('resolution').desc().first()
            
            #Progress.configure(text="DOWNLOADING",bg="red")

            video.download(dest)

        if AudioOnly and MP3:
            vid=dest+'\\'+yt.title
            os.rename(vid+'.mp4', vid+'.mp3')

        messagebox.showinfo('Success!', 'Done downloading video(s)!\nVideo(s) should be located in %s'%dest)
        Progress.configure(text="Done!",bg="green")
        print("Done downloading video(s)!")
        print("Video(s) should be located in %s"%dest)
    
    except Exception as e:
        messagebox.showinfo('Error', e)
        Progress.configure(text="ERROR",bg="red")

def getpreview(ytURL,PrevIMG,VidInfo):
    
    URLtxt = ytURL.get()
    if(URLtxt):

        yt = pytube.YouTube(URLtxt)
        VidInfo.delete(1.0,END)
        VidInfo.insert(INSERT,('Title:\n'+yt.title))

        thumnail_url =  requests.get(yt.thumbnail_url)
        load = Image.open(BytesIO(thumnail_url.content))
        render = ImageTk.PhotoImage(load.resize((280, 158)))
        PrevIMG.configure(image=render)
        PrevIMG.image = render
    else:
        messagebox.showinfo('Error', 'No Video was linked!')
    
def SelectDir(DnldDest):
    DnldDest.configure(text=filedialog.askdirectory(initialdir=os.getcwd()))


def main():
    window = Tk()
    window.title("Download Youtube Videos!")
    window.geometry('287x360')
    backgoundColor='blanchedalmond'
    buttonColor='NAVAJOWHITE'
    window.configure(background=backgoundColor)
    
    path = "http://img.youtube.com/vi/bKOIG1sIr0o/0.jpg"
    AudioOnly = BooleanVar()
    AudioOnly.set(False)
    
    MP3 = BooleanVar()
    MP3.set(False)

    enrLabel = Label(window, text="Enter a Youtube URL:",  bg=backgoundColor)
    enrLabel.grid(row=0, column=0, sticky=W, padx=(0,15))

    ytURL = Entry(window,width=25)
    ytURL.grid(row=0,column=1, sticky=W)

    audioCheck = Checkbutton(window, text='Audio Only?', var=AudioOnly,anchor=W, bg=backgoundColor)
    audioCheck.grid(row=1,column=0, sticky=W)

    ToMp3 = Checkbutton(window, text='Change to Mp3', var=MP3, anchor=W, bg=backgoundColor)
    ToMp3.grid(row=1,column=1, sticky=W)

    preBtn = Button(window, text="Preview", command= lambda: getpreview(ytURL,PrevIMG,VidInfo), bg=buttonColor)
    preBtn.grid(row=2,column=0, sticky=W)

    DNDLbtn = Button(window, text="Download!", command= lambda: DNLD_YT_Audio(ytURL, AudioOnly.get(), MP3.get(), DnldDest, PrevIMG, VidInfo, Progress), bg=buttonColor)
    DNDLbtn.grid(row=2,column=0, sticky=E,padx=5)
    
    Dirbtn = Button(window, text="Select Download Directory!", command= lambda: SelectDir(DnldDest), bg=buttonColor)
    Dirbtn.grid(row=2,column=1,columnspan=2)#, sticky=W)

    DnldDest = Label(window, text=os.getcwd(), bg=backgoundColor)
    DnldDest.grid(row=4, column=0,columnspan=2)#, sticky=W)

    VidInfo = scrolledtext.ScrolledText(window,width=30,height=2)
    VidInfo.grid(row=5,column=0, rowspan=5, columnspan=2)

    PrevIMG = Label(window, bg=backgoundColor)
    PrevIMG.grid(row=10, column=0,rowspan=20, columnspan=2)#, sticky=W)
    
    Progress = Label(window, bg=backgoundColor)
    Progress.grid(row=30, column=0,rowspan=20, columnspan=2)#, sticky=W)

    window.mainloop()

if __name__ == "__main__":
    main()