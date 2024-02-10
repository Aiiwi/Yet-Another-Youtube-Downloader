import tkinter as tk
from tkinter import filedialog,messagebox
from pytube import YouTube
import os
import sys

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
#:D
def resource_path(relative_path):
    """Thanks to a response on stack this func helps for building the program with pyinstaller"""
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Window(object):
    def __init__(self,root) -> None:
        """Constructor of the root of the window obj"""

        self.__root=root
        self.link_input,self.destination=tk.StringVar(),tk.StringVar()
        self.__filter=tk.IntVar()
        self.__list=tk.BooleanVar()
        root.iconphoto(False,tk.PhotoImage(file=resource_path("splash\\favicon.png"))) 
        root.geometry("550x260")
        root.title("Yet Another Youtube Downloader!")
        root.config(bg="darkseagreen")
        root.resizable(0,0)
        
    def face(self) -> None:
        """Widgets that create on the window like the title and labels"""

        title=tk.Label(self.__root,text="Yet another Youtube Downloader",padx=10,pady=10,font=("Impact",20),bg="darkseagreen",fg="black",)
        title.grid(row=1,column=0,padx=10,pady=10,columnspan=3)

        link_label=tk.Label(self.__root,text="Youtube link :",bg="darkseagreen2",fg="black",font="Arial",padx=4,pady=4,borderwidth=5,highlightthickness=1)
        link_label.grid(row=3,column=0,padx=4,pady=4)

        destination_label=tk.Label(self.__root,text="Video destination :",bg="darkseagreen2",fg="black",font="Arial",padx=4,pady=4,borderwidth=5,highlightthickness=1)
        destination_label.grid(row=4,column=0,padx=4,pady=4)

        radio1=tk.Radiobutton(self.__root,text="Mp4",padx=3,pady=3,variable=self.__filter,value=1,bg="darkseagreen",activebackground="darkseagreen",font="Arial")
        radio1.grid(row=5,column=2,padx=3,pady=3)
        radio1=tk.Radiobutton(self.__root,text="Mp3",padx=3,pady=3,variable=self.__filter,value=0,bg="darkseagreen",activebackground="darkseagreen",font="Arial")
        radio1.grid(row=6,column=2,padx=3,pady=3)
    
    def inputs(self) -> None:
        """This method builds the inputs labels of the downloader and the browse button"""

        self.__root.linkinput= tk.Entry(self.__root,width=40,textvariable=self.link_input,font="Arial")
        self.__root.linkinput.grid(row=3,column=1,pady=4,padx=4,columnspan=2)

        self.__root.dest=tk.Entry(self.__root,width=30,textvariable=self.destination,font="Arial")
        self.__root.dest.grid(row=4,column=1,pady=4,padx=4)

        dirbrowse=tk.Button(self.__root,text="Browse",command=self.browse,width=5,bg="cyan",padx=5,pady=2.5,font="Arial")
        dirbrowse.grid(row=4,column=2,padx=10,pady=5)

        downloadbut=tk.Button(self.__root,text="Download",command=self.download,width=10,bg="cyan",padx=10,pady=5,font="Arial")
        downloadbut.grid(row=5,column=1,padx=10,pady=5)

    def browse(self) -> None:
        """Browse button method that opens a window to ask your desired download dir path"""

        self.dwdir=str(filedialog.askdirectory(initialdir="Your Dir Path",title="Choose video directory..."))
        self.destination.set(self.dwdir)
    
    def download(self) -> None:
        """This method is the responsible to download your video based on the choice of a mp3 or mp4"""
        #Problem: The mp3 is just a renamed mp4 and may cause problems!
        ytlink=self.link_input.get()
        folder_destination=self.destination.get()
        buttonvar=self.__filter.get()
        try:
            if buttonvar==1:
                #Mp4 download 
                YouTube(ytlink).streams.get_highest_resolution().download(folder_destination)
            elif buttonvar==0:
                #Mp3 download 

                mp3=YouTube(ytlink).streams.filter(only_audio=True).first()
                downmp3=mp3.download(folder_destination)
                base, ext = os.path.splitext(os.path.basename(downmp3))
                mp3_filename = (base+" audio") + ".mp3"
                os.rename(os.path.join(folder_destination, downmp3), os.path.join(folder_destination, mp3_filename))

        except Exception as exp:
            #Message box for error logging
            messagebox.showerror("An error has occured! <╥﹏╥>",f"Error:{str(exp)}")
        else:
            #Message box for a successful download
            messagebox.showinfo("Success! ﾉ(•◡•)ﾉ","Your video has been downloaded! If you didn't choose a path don't worry the folder of this program is the default one for the downloads! :D")
    
    def mainloop(self) -> None:
        """window maintainer"""
        self.__root.mainloop()