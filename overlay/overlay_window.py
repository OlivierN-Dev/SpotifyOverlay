import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import requests
from io import BytesIO
from spotify_api import get_current_track, sp
import threading
import time


def ms_to_time(ms):
    if not ms:
        return "00:00"
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Crée un rectangle avec coins arrondis"""
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    
    return canvas.create_polygon(points, **kwargs, smooth=True)

def create_circular_image(image, size):
    """Crée une image circulaire"""
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(image, (0, 0))
    output.putalpha(mask)
    
    return output


class OverlayWindow:
    def __init__(self):
        self.running = True
        self.root = tk.Tk()
        self.root.title("Spotify Overlay")

        # Dimensions légèrement agrandies
        window_width = 450
        window_height = 160
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) - 40
        y = 50
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Fond gradient sombre moderne
        self.root.configure(bg="#1a1a1a")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        
        # Rendre le fond transparent (Windows)
        try:
            self.root.attributes("-transparentcolor", "#1a1a1a")
        except:
            pass

        # Canvas principal pour le fond avec effet glassmorphism
        self.bg_canvas = tk.Canvas(self.root, width=window_width, height=window_height, 
                                   bg="#1a1a1a", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)
        
        # Fond avec dégradé simulé
        create_rounded_rectangle(self.bg_canvas, 5, 5, window_width-5, window_height-5, 
                                radius=20, fill="#282828", outline="#404040", width=1)

        # Variables Tkinter
        self.song_var = tk.StringVar()
        self.artist_var = tk.StringVar()
        self.progress_var = tk.StringVar()

        # Canvas album avec ombre
        self.album_canvas = tk.Canvas(self.root, width=120, height=120, 
                                      bg="#282828", highlightthickness=0)
        self.album_canvas.place(x=20, y=20)
        
        # Ombre pour l'album
        self.album_shadow = self.album_canvas.create_oval(5, 5, 115, 115, 
                                                          fill="#000000", outline="")
        
        self.blank_image = tk.PhotoImage(width=110, height=110)
        self.album_image = self.album_canvas.create_oval(5, 5, 115, 115, 
                                                         fill="#3a3a3a", outline="#1DB954", width=2)
        self.album_photo = self.album_canvas.create_image(60, 60, image=self.blank_image)

        # Frame pour les textes
        info_frame = tk.Frame(self.root, bg="#282828")
        info_frame.place(x=155, y=20)

        # Labels avec style moderne
        self.song_label = tk.Label(info_frame, textvariable=self.song_var, 
                                   font=("Segoe UI", 13, "bold"), 
                                   fg="#ffffff", bg="#282828", anchor="w", width=20)
        self.song_label.pack(anchor="w", pady=(0, 2))
        
        self.artist_label = tk.Label(info_frame, textvariable=self.artist_var, 
                                     font=("Segoe UI", 10), 
                                     fg="#b3b3b3", bg="#282828", anchor="w", width=20)
        self.artist_label.pack(anchor="w", pady=(0, 10))
        
        # Barre de progression stylisée
        self.progress_canvas = tk.Canvas(info_frame, width=250, height=4, 
                                        bg="#404040", highlightthickness=0)
        self.progress_canvas.pack(anchor="w", pady=(0, 5))
        
        self.progress_bar_bg = self.progress_canvas.create_rectangle(0, 0, 250, 4, 
                                                                     fill="#404040", outline="")
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 4, 
                                                                  fill="#1DB954", outline="")
        
        self.progress_label = tk.Label(info_frame, textvariable=self.progress_var, 
                                      font=("Segoe UI", 9), 
                                      fg="#b3b3b3", bg="#282828", anchor="w")
        self.progress_label.pack(anchor="w")

        # Contrôles avec style Spotify
        controls_frame = tk.Frame(self.root, bg="#282828")
        controls_frame.place(x=155, y=115)

        # Bouton suivant (maintenant à gauche) - Désactivé sans Premium
        self.next_canvas = tk.Canvas(controls_frame, width=32, height=32, 
                                 bg="#282828", highlightthickness=0)
        self.next_canvas.pack(side=tk.LEFT, padx=5)
        self.next_canvas.create_oval(2, 2, 30, 30, fill="#2a2a2a", outline="#3a3a3a", width=1)
        self.next_canvas.create_polygon(12, 16, 20, 12, 20, 20, fill="#555555")
        self.next_canvas.create_rectangle(20, 12, 22, 20, fill="#555555")

        # Bouton play/pause - Désactivé sans Premium
        self.pause_canvas = tk.Canvas(controls_frame, width=36, height=36, 
                                  bg="#282828", highlightthickness=0)
        self.pause_canvas.pack(side=tk.LEFT, padx=5)
        self.pause_circle = self.pause_canvas.create_oval(2, 2, 34, 34, 
                                                       fill="#2a2a2a", outline="#3a3a3a", width=2)
        self.pause_icon1 = self.pause_canvas.create_rectangle(13, 11, 16, 25, fill="#555555")
        self.pause_icon2 = self.pause_canvas.create_rectangle(20, 11, 23, 25, fill="#555555")

        # Bouton précédent (maintenant à droite) - Désactivé sans Premium
        self.prev_canvas = tk.Canvas(controls_frame, width=32, height=32, 
                                 bg="#282828", highlightthickness=0)
        self.prev_canvas.pack(side=tk.LEFT, padx=5)
        self.prev_canvas.create_oval(2, 2, 30, 30, fill="#2a2a2a", outline="#3a3a3a", width=1)
        self.prev_canvas.create_polygon(20, 16, 12, 12, 12, 20, fill="#555555")
        self.prev_canvas.create_rectangle(10, 12, 12, 20, fill="#555555")

        # Indicateur volume
        volume_canvas = tk.Canvas(controls_frame, width=60, height=32, 
                                 bg="#282828", highlightthickness=0)
        volume_canvas.pack(side=tk.LEFT, padx=10)
        volume_canvas.create_text(30, 16, text="♪", font=("Segoe UI", 16), 
                                 fill="#1DB954")

        # Bouton fermer modernisé
        self.close_btn = tk.Canvas(self.root, width=24, height=24, 
                                  bg="#282828", highlightthickness=0, cursor="hand2")
        self.close_btn.place(x=window_width-34, y=10)
        self.close_btn.create_oval(2, 2, 22, 22, fill="#404040", outline="#555555", width=1)
        self.close_btn.create_line(8, 8, 16, 16, fill="#ffffff", width=2)
        self.close_btn.create_line(16, 8, 8, 16, fill="#ffffff", width=2)
        self.close_btn.bind("<Button-1>", lambda e: self.on_close())

        # Fermeture propre
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Lancer le thread de mise à jour
        threading.Thread(target=self.update_loop_thread, daemon=True).start()

        # Lancer Tkinter
        self.root.mainloop()

    def toggle_play_pause(self):
        """Basculer entre lecture et pause"""
        try:
            track = get_current_track()
            if track["is_playing"]:
                sp.pause_playback()
            else:
                sp.start_playback()
        except Exception as e:
            print(f"Erreur play/pause: {e}")

    def skip_next(self):
        """Passer à la piste suivante"""
        try:
            sp.next_track()
        except Exception as e:
            print(f"Erreur skip next: {e}")

    def skip_previous(self):
        """Revenir à la piste précédente"""
        try:
            sp.previous_track()
        except Exception as e:
            print(f"Erreur skip previous: {e}")

    def on_close(self):
        self.running = False
        self.root.destroy()

    def update_loop_thread(self):
        while self.running:
            try:
                track = get_current_track()
                self.root.after(0, lambda t=track: self.update_ui(t))
            except:
                pass
            time.sleep(1)

    def update_ui(self, track):
        if not self.running:
            return

        if track["name"] is None:
            self.song_var.set("Aucune musique en cours")
            self.artist_var.set("Lancez Spotify")
            self.progress_var.set("00:00 / 00:00")
            self.progress_canvas.coords(self.progress_bar, 0, 0, 0, 4)
        else:
            # Tronquer si trop long
            song_name = track["name"][:30] + "..." if len(track["name"]) > 30 else track["name"]
            artist_name = track["artist"][:35] + "..." if len(track["artist"]) > 35 else track["artist"]
            
            self.song_var.set(song_name)
            self.artist_var.set(artist_name)
            self.progress_var.set(f"{ms_to_time(track['raw_progress'])} / {ms_to_time(track['raw_duration'])}")

            # Mise à jour barre de progression
            if track['raw_duration'] > 0:
                progress_ratio = track['raw_progress'] / track['raw_duration']
                bar_width = int(250 * progress_ratio)
                self.progress_canvas.coords(self.progress_bar, 0, 0, bar_width, 4)

            # Télécharger et afficher l'image album en cercle
            try:
                response = requests.get(track["image"])
                img = Image.open(BytesIO(response.content)).resize((110, 110), Image.Resampling.LANCZOS)
                
                # Créer image circulaire
                circular_img = create_circular_image(img, 110)
                tk_img = ImageTk.PhotoImage(circular_img)
                
                self.album_canvas.itemconfig(self.album_photo, image=tk_img)
                self.album_canvas.img = tk_img
            except:
                pass