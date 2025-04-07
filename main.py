import os
import sys
import threading
import tkinter as tk
if os.name == "nt": from lib import pywinstyles
from lib import ffmpeg
from tkinter import ttk
from tkinter import filedialog,messagebox
from pytubefix import YouTube
from pytubefix.cli import on_progress


def main() -> None:
    root=tk.Tk()
    root.tk.call("source","lib/ftheme/forest-dark.tcl") 
    ttk.Style().theme_use("forest-dark")

    root.option_add("*tearOff", False)
    root.title("Yet Another YT Downloader")
    width = 640
    height = 480
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(0, 0)
    root.iconphoto(False,tk.PhotoImage(file=resource_path("icon/icon.png"))) 

    link_input,destination=tk.StringVar(),tk.StringVar()
    progressvar=tk.DoubleVar(value=0.0)

    if os.name == "nt":
        pywinstyles.change_header_color(root, color="#313131")
        pywinstyles.change_border_color(root, color="#123123")

    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=1)
    root.columnconfigure(index=2, weight=1)
    root.rowconfigure(index=0, weight=1)
    root.rowconfigure(index=1, weight=1)
    root.rowconfigure(index=2, weight=1)
    root.rowconfigure(index=3, weight=1)

    paned = ttk.PanedWindow(root)
    paned.grid(row=0, column=0,padx=(10, 10), pady=(10, 10), sticky="nsew", rowspan=4,columnspan=3)
    pane_1 = ttk.Frame(paned)
    paned.add(pane_1, weight=1)

    notebook = ttk.Notebook(pane_1)

    tab_1 = ttk.Frame(notebook)
    notebook.add(tab_1, text="Downloader")
    tab_2 = ttk.Frame(notebook)
    notebook.add(tab_2, text="Credits")
    notebook.pack(expand=True, fill="both", padx=5, pady=5)

    #TAB 1
    tab_1.columnconfigure(index=0, weight=1)
    tab_1.columnconfigure(index=1, weight=1)
    tab_1.columnconfigure(index=2, weight=1)
    tab_1.rowconfigure(index=0, weight=1)
    tab_1.rowconfigure(index=1, weight=1)
    tab_1.rowconfigure(index=2, weight=1)
    tab_1.rowconfigure(index=3, weight=1)

    labellink=tk.Label(tab_1,text="Link",padx=10,pady=10,font=("Arial",20),fg="#287444")
    labellink.grid(row=0, column=0,padx=(10, 10), pady=(10, 10), sticky="nsew")
    labellink1=tk.Label(tab_1,text="Path",padx=10,pady=10,font=("Arial",20),fg="#287444")
    labellink1.grid(row=1, column=0,padx=(10, 10), pady=(10, 10), sticky="nsew")

    progress = ttk.Progressbar(tab_1, value=0, variable=progressvar, length=500)
    progress.grid(row=3, column=1, padx=(10, 10), pady=(10, 10), sticky="se",columnspan=3)

    root.linkinput= ttk.Entry(tab_1,width=40,textvariable=link_input,font="Arial")
    root.linkinput.grid(row=0,column=1)

    root.dest=ttk.Entry(tab_1,width=40,textvariable=destination,font="Arial")
    root.dest.grid(row=1,column=1)

    dirbrowse=ttk.Button(tab_1,command=lambda: browse_files(destination),text="Browse")
    dirbrowse.grid(row=1,column=2,padx=12)

    fileformat = tk.IntVar(value=1)

    radio_1 = ttk.Radiobutton(tab_1, text="MP4", variable=fileformat, value=1)
    radio_1.grid(row=2, column=0, padx=5, pady=10, sticky="e")
    radio_2 = ttk.Radiobutton(tab_1, text="M4A", variable=fileformat, value=2)
    radio_2.grid(row=2, column=1, padx=5, pady=10, sticky="w")
    radio_3 = ttk.Radiobutton(tab_1, text="MP3", variable=fileformat, value=3)
    radio_3.grid(row=2, column=1, padx=75, pady=10, sticky="w")
    #radio_4 = ttk.Radiobutton(tab_1, text="MOV", variable=fileformat, value=4)
    #radio_4.grid(row=2, column=1, padx=145, pady=10, sticky="w")

    downloadbutton=ttk.Button(tab_1,text="Download",command= lambda: download(link_input,destination,fileformat,progress))
    downloadbutton.grid(row=3,column=0,sticky="sw")

    #TAB 1 FINISH

    #TAB 2
    tab_2.columnconfigure(index=0, weight=1)
    tab_2.columnconfigure(index=1, weight=1)
    tab_2.columnconfigure(index=2, weight=1)
    tab_2.rowconfigure(index=0, weight=1)
    tab_2.rowconfigure(index=1, weight=1)
    tab_2.rowconfigure(index=2, weight=1)
    tab_2.rowconfigure(index=3, weight=1)

    labellink=tk.Label(tab_2,text="Use this tool with responsibility mind Copyright Laws.",font=("Arial",15),fg="#ff0000")
    labellink.grid(row=0, column=0, sticky="nw",columnspan=2)

    labellink=tk.Label(tab_2,text="Credits:\n\nPytubefix by JuanBindez on git\nForest-ttk-theme by rdbende on git\nPy-window-styles by Akascape on git\nFfmpeg-python by kkroening on git",font=("Arial Bold",10),fg="#287444")
    labellink.grid(row=1, column=1, sticky="nsw")


    labellink=tk.Label(tab_2,text="Version : 1.1",padx=10,pady=10,font=("Arial Bold",10),fg="#287444")
    labellink.grid(row=3, column=0,padx=(10, 10), pady=(10, 10), sticky="sw")
    labellink1=tk.Label(tab_2,text=f"Os type : {str(os.name)}",padx=10,pady=10,font=("Arial Bold",10),fg="#287444")
    labellink1.grid(row=3, column=2, sticky="se",padx=(10, 10), pady=(10, 10))
    #TAB 2 FINISH

    root.mainloop()

def browse_files(destination) -> None:
    dwdir=str(filedialog.askdirectory(initialdir="Your Dir Path",title="Choose directory..."))
    destination.set(dwdir)

def download(link_input,destination,fileformat,progress):
    ytlink=link_input.get()
    folder_destination=destination.get()
    buttonvar=fileformat.get()

    try:
        if buttonvar==1:
            #Mp4 download 
            if folder_destination=="" or ytlink=="":
                raise Exception(" Download Path or link not set!")
            else:
                threading.Thread(target=highest_video_res,args=(ytlink,folder_destination),daemon=True).start()

        elif buttonvar==2:
            #M4a download
            if folder_destination=="" or ytlink=="":
                raise Exception(" Download Path or link not set!")
            else:
                YouTube(ytlink, on_progress_callback = on_progress).streams.get_audio_only().download(folder_destination)
        elif buttonvar==3:
            #Mp3 download
            if folder_destination=="" or ytlink=="":
                raise Exception(" Download Path or link not set!")
            else:
                file=YouTube(ytlink, on_progress_callback = on_progress).streams.get_audio_only().download(folder_destination)
                ffmpeg_conv(folder_destination,file,".mp3")
        elif buttonvar==4:
            messagebox.showinfo("Sorry! <╥﹏╥>","Not yet implemented im finding some problems!")
            #MOV download
            #if folder_destination=="":
                #raise Exception("Download Path not set!")
            #else:
                #highest_video_res(ytlink,folder_destination,True,".mov")

    except Exception as exp:
        #Message box for error logging
        messagebox.showerror("An error occured! <╥﹏╥>",f"Error:{str(exp)}")
    else:
        #Message box for a successful download
        progress.step(90.0)
        messagebox.showinfo("Success! ﾉ(•◡•)ﾉ","Your video has been downloaded! If you didn't choose a path the default folder is the downloads one!")

def ffmpeg_conv(resides,file,newext):
    base, ext = os.path.splitext(os.path.basename(file))
    (
	ffmpeg.input(resides+"/"+base+ext)
	.output(resides+"/"+base+newext)
	.run()
    )
    if os.path.exists(resides+"/"+base+ext):
        os.remove(resides+"/"+base+ext)

def highest_video_res(ytlink,folder_destination,*args,**kwargs):
    video_stream = YouTube(ytlink, on_progress_callback = on_progress).streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
    audio_stream = YouTube(ytlink, on_progress_callback = on_progress).streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

    video_stream.download(output_path=folder_destination)
    audio_stream.download(filename='audio.mp4',output_path=folder_destination)

    i_video=ffmpeg.input(folder_destination+"/"+video_stream.title+".mp4")
    i_audio=ffmpeg.input(folder_destination+"/audio.mp4")
    filemp4=ffmpeg.concat(i_video,i_audio,v=1,a=1).output(folder_destination+"/"+video_stream.title+"1.mp4").run()

    if os.path.exists(folder_destination+"/"+video_stream.title+"1.mp4") and os.path.exists(folder_destination+"/audio.mp4") :
        os.remove(folder_destination+"/"+video_stream.title+".mp4")
        os.remove(folder_destination+"/audio.mp4")

    if args:
        ffmpeg_conv(folder_destination,filemp4,kwargs) #qua esplode tutto dice cose di tumpla ma mi sono cagato il cazzo
    else:
        pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

main()