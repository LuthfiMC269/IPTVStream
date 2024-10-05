import vlc
import time
import tkinter as tk
from tkinter import messagebox
import threading

player = None
stop_thread = False

channel1 = "https://cdn.gunadarma.ac.id/streams/ugtv/ingestugtv_high.m3u8"
channel2 = "https://video.detik.com/transtv/smil:transtv.smil/chunklist_w1637227557_b744100_sleng.m3u8"
channel3 = "https://live.cnbcindonesia.com/livecnbc/smil:cnbctv.smil/master.m3u8"


def playstream(m3u8_url):
    global player
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(m3u8_url)
    player.set_media(media)
    player.set_hwnd(framevid.winfo_id())  # framevid.winfo_id, id dari inisialisasi framevid (initialize frame kanan)
    player.play()

    time.sleep(1)

    # Keep checking if the player is still playing
    while not stop_thread:
        state = player.get_state()
        if state in [vlc.State.Ended, vlc.State.Error]:  # Stream ended or error
            print("Stream ended or encountered an error.")
            break
        elif state == vlc.State.Playing:  # Stream is playing
            print("Playing audio...")
        time.sleep(1)  # Check every second


def start_stream(url):
    m3u8_url = url
    stream_thread = threading.Thread(target=playstream, args=[m3u8_url,])
    stream_thread.start()


def change_channel(channel):
    m3u8_url = channel
    if player:
        player.stop()
    start_stream(m3u8_url)


# Initialize window
Window = tk.Tk()
Window.title("IPTV Preview Test Lmcpsite.my.id")
Window.geometry("1600x800")
Window.resizable()

# Initialize Frame Kanan
framevid = tk.Frame(Window, bg="#000000")
framevid.place(relx=0.10, y=0, relwidth=0.9, relheight=1)

# Initialize Frame Kiri
frametombol = tk.Frame(Window, bg="#373737")
frametombol.place(relx=0.0, y=0, relwidth=0.10, relheight=1)

# Text
text1 = tk.Label(frametombol, text="IPTV", bg="#373737", fg="white", font=("Poppins-bold", 25, "bold"))
text1.place(relx=0.5, rely=0.05, anchor="center")
# Tombol
btn_chn1 = tk.Button(frametombol, text="UGTV", font=("Helvetica", 15), fg="#FFFFFF", bg="#4CAF50",
                     activebackground="#45a049", command=lambda: change_channel(channel1))
btn_chn1.place(relx=0.5, rely=0.10, anchor="center")
btn_chn2 = tk.Button(frametombol, text="TransTV", font=("Helvetica", 15), fg="#FFFFFF", bg="#4CAF50",
                     activebackground="#45a049", command=lambda: change_channel(channel2))
btn_chn2.place(relx=0.5, rely=0.18, anchor="center")
btn_chn3 = tk.Button(frametombol, text="CNBC Indonesia", font=("Helvetica", 15), fg="#FFFFFF", bg="#4CAF50",
                     activebackground="#45a049", command=lambda: change_channel(channel3))
btn_chn3.place(relx=0.5, rely=0.26, anchor="center")


def on_closing():  # Pencet tombol X di Window
    global player, stop_thread
    if player:
        if messagebox.askokcancel("Quit", "Do you want to quit?", icon=messagebox.WARNING):
            stop_thread = True
            player.stop()
            Window.destroy()
        return
    Window.destroy()


Window.protocol("WM_DELETE_WINDOW", on_closing)
Window.mainloop()
