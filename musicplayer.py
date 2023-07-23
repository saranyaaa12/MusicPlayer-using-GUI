#APPLYING CLASS METHOD and FUNCTIONS for each set

import os
import pickle
import tkinter as tk
from tkinter import filedialog, PhotoImage
from pygame import mixer

class MusicPlayer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current_item = 0
        self.paused = True
        self.played = False

        self.createFrames()

        self.frame1Widgets()
        self.frame2Widgets()
        self.frame3Widgets()

    # frame1 - Image, Song name; 
    # frame2 - Controls, Browse button; 
    # frame3 - Songslist
    def createFrames(self):
        self.frame1 = tk.LabelFrame(self, bg="#333333", bd=0)
        self.frame1.config(width=480, height=400)
        self.frame1.grid(row=0, column=0)

        self.frame2 = tk.LabelFrame(self, bg="#333333", bd=0, fg="#333333")
        self.frame2.config(width=480, height=100)
        self.frame2.grid(row=1, column=0)

        self.frame3 = tk.LabelFrame(self, bg="#333333", text=f"Playlist - {str(len(self.playlist))}", 
                                    font=("times new roman", 15, "bold"), bd=4, fg='#ffffff', relief=tk.GROOVE)
        self.frame3.config(width=480, height=140)
        self.frame3.grid(row=2, columnspan=5, column=0)


    def frame1Widgets(self):
        self.canvas = tk.Label(self.frame1, image= mainimage)
        self.canvas.configure(width=480, height=350)
        self.canvas.grid(row=0, column=0)
        
        self.songname = tk.Label(self.frame1, font=("times new roman",15, "bold"), bg="#333333", fg="#ffffff")
        self.songname['text'] = "MP3 Music Player"
        self.songname.configure(width=30, height=2)
        self.songname.grid(row=1, column=0)

    def frame2Widgets(self):

        self.browse = tk.Button(self.frame2, bg="#333333", fg="#ffffff")
        self.browse['text'] = "Browse Songs"
        self.browse['command'] = self.retrieveSongs
        self.browse.grid(row=1, column=0, padx=5, pady=5)
    
        self.replay = tk.Button(self.frame2, image=buttonReplay, width=55, height=55, bd=0, bg="#333333")
        self.replay['command'] = self.replaySong
        self.replay.grid(row=0, column=0, padx=15, pady=5)

        self.previous = tk.Button(self.frame2, image=buttonPrevious, width=55, height=55, bd=0, bg="#333333")
        self.previous['command'] = self.previousSong
        self.previous.grid(row=0, column=1, padx=15, pady=5)

        self.pause = tk.Button(self.frame2, image=buttonPlay, width=55, height=55, bd=0, bg="#333333")
        self.pause['command'] = self.pauseSongs
        self.pause.grid(row=0, column=2, padx=15, pady=5)

        self.next = tk.Button(self.frame2, image=buttonNext, width=55, height=55, bd=0, bg="#333333")
        self.next['command'] = self.nextSong
        self.next.grid(row=0, column=3, padx=15, pady=5)

        self.volume1 = tk.DoubleVar()
        self.slider = tk.Scale(self.frame2, from_=0, to=10, orient=tk.HORIZONTAL, bg="#333333", fg="#ffffff")
        self.slider['variable'] = self.volume1
        self.slider.set(7)
        mixer.music.set_volume(0.7)
        self.slider['command'] = self.changeVolume
        self.slider.grid(row=0, column=4, padx=11, pady=5)

    
    def frame3Widgets(self):
        
        self.scrollBar = tk.Scrollbar(self.frame3, orient=tk.VERTICAL)
        self.scrollBar.grid(row=0, column=1, sticky='ns')
        self.list = tk.Listbox(self.frame3, selectmode=tk.SINGLE, width=76,
                               yscrollcommand=self.scrollBar.set,
                               selectbackground="#333333")
        self.displaySongs()
        self.list.config(height=6)
        self.list.bind("<Double-1>", self.playSongs)
        self.scrollBar.config(command=self.list.yview)
        self.list.grid(row=0, column=0)
        

    def displaySongs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def retrieveSongs(self):
        self.songList = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    path = (root_ + '/' + file).replace("\\", "/")
                    self.songList.append(path)
        

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songList, f)

        self.playlist = self.songList
        self.frame3['text'] = f"Playlist - {str(len(self.playlist))}"
        self.list.delete(0, tk.END)
        self.displaySongs()

    def playSongs(self, event=None):
        if event is not None:
            self.current_item = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        mixer.music.load(self.playlist[self.current_item])

        self.pause['image'] = buttonPause
        self.paused = False
        self.played = True
        self.songname['anchor'] = 'w'
        self.songname['text'] = os.path.basename(self.playlist[self.current_item])
        self.list.activate(self.current_item)

        self.list.itemconfigure(self.current_item, bg="sky blue")
        mixer.music.play()

    def pauseSongs(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = buttonPlay
        else:
            if self.played == False:
                self.playSongs()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = buttonPause

    def previousSong(self):
        if self.current_item > 0:
            self.current_item -= 1
        else:
            self.current_item = 0
        self.list.itemconfigure(self.current_item + 1, bg="white")
        self.playSongs()

    def nextSong(self):
        if self.current_item < (len(self.playlist) - 1):
            self.current_item += 1
        else:
            self.current_item = 0
        self.list.itemconfigure(self.current_item - 1, bg="white")
        self.playSongs()

    def replaySong(self):
        if self.current_item is not None:
            mixer.music.load(self.playlist[self.current_item])
            self.list.itemconfigure(self.current_item, bg="sky blue")
            mixer.music.play()

    def changeVolume(self, event=None):
        self.v = self.volume1.get()
        mixer.music.set_volume(self.v / 10)
    

root = tk.Tk()
root.title("Music Player")
root.geometry("480x650+250+50")
root.configure(background='#333333')
root.resizable(False,False)


mainimage = PhotoImage(file= "musicIcons/music1.png")
buttonReplay = PhotoImage(file= "musicIcons/replay1.png")
buttonPrevious = PhotoImage(file= "musicIcons/backward1X100.png")
buttonPlay = PhotoImage(file= "musicIcons/play.png")
buttonPause = PhotoImage(file= "musicIcons/pause.png")
buttonNext = PhotoImage(file= "musicIcons/forward1X100.png")


musicApp = MusicPlayer(root)
musicApp.mainloop()