import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from typing import Callable, Optional
from dotenv import load_dotenv

class GUI:
    def __init__(self, controller_callback: Callable[[str], None], env_var_set):
        self.controller_callback = controller_callback
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta la ventana principal inicialmente

        self.env_var_set = env_var_set
        self.spotifyId = tk.StringVar()
        self.spotifySecret = tk.StringVar()

        self._setup_path_selection_window()
    
    #-------------------------------------SETUPS--------------------------------------
    def _setup_path_selection_window(self):
        """Ventana para selección de path"""
        self.path_window = tk.Toplevel()
        self.path_window.title("Selección de Path")
        self.path_window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self.path_var = tk.StringVar()
        
        ttk.Label(self.path_window, text="Path seleccionado:").pack(pady=5)
        ttk.Entry(self.path_window, textvariable=self.path_var, width=50).pack(pady=5)
        

        ttk.Button(self.path_window, text="Seleccionar Directorio",
                 command=self._select_directory).pack(pady=5)
        ttk.Button(self.path_window, text="Confirmar",
                 command=self._confirm_path_selection).pack(pady=10)
    
    def _setup_action_window(self, path: str):
        """Ventana secundaria con acciones para el path seleccionado"""
        self.action_window = tk.Toplevel()
        self.action_window.title(f"Bienvenido a TonyDownloader")
        ttk.Label(self.action_window,text="¿Que quieres hacer?").pack(pady=5)
        self.action_window.geometry("400x400")
        self.action_window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Frame principal
        main_frame = ttk.Frame(self.action_window)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Panel de información
        info_frame = ttk.LabelFrame(main_frame, text="Información del Path")
        info_frame.pack(fill='x', pady=5)
        ttk.Label(info_frame, text=f"Path seleccionado:\n{path}").pack()
        
        # Panel de acciones
        action_frame = ttk.LabelFrame(main_frame, text="Acciones disponibles")
        action_frame.pack(fill='both', expand=True, pady=5)
        
        # Botones de acción
        ttk.Button(action_frame, text="Descargar Playlist de Spotify",
                 command=self._check_Spotify).pack(pady=5)
        ttk.Button(action_frame, text="Descargar Canción",
                 command=self._setup_song_selection_window).pack(pady=5)
        ttk.Button(action_frame, text="Proximamente",
                 command=lambda: self._send_action("report", path)).pack(pady=5)
        
        # Panel de opciones
        config_frame = ttk.LabelFrame(main_frame, text="Configuración")
        config_frame.pack(fill='both', expand=True, pady=5)

        # Botón de API spotify
        ttk.Button(config_frame, text="API keys",
                 command=self._change_API_keys).pack(pady=5)

        # Panel abort
        abort_frame = ttk.LabelFrame(main_frame)
        abort_frame.pack(fill="both",expand="True",pady=5)

        # Botón de regreso
        ttk.Button(abort_frame, text="Cambiar ruta de descarga",
                 command=self._return_to_path_selection).pack(pady=10)
        
        # Botón de quit
        ttk.Button(abort_frame, text="Salir",
                 command=self._on_close).pack(padx=5)
    
    def _setup_playlistSpot_window(self):
        """Ventana para selección de playlist"""
        self.playlistSpot_window = tk.Toplevel()
        self.playlistSpot_window.title("Seleccionar la playlist")
        self.playlistSpot_window.protocol("WM_DELETE_WINDOW", self._return_to_action_selection_from_playlist)
        
        self.urlSpot_var = tk.StringVar()
        
        ttk.Label(self.playlistSpot_window, text="URL o ID de la Playlist").pack(pady=5)
        ttk.Entry(self.playlistSpot_window, textvariable=self.urlSpot_var, width=50).pack(pady=5)
        
        ttk.Button(self.playlistSpot_window, text="Confirmar",
                 command=self._confirm_playlistSpot_selection).pack(pady=10)
    
    def _setup_song_selection_window(self):
        """Ventana para selección de canción"""
        self.song_selection_window = tk.Toplevel()
        self.song_selection_window.title("Seleccionar la canción")
        self.song_selection_window.protocol("WM_DELETE_WINDOW", self._return_to_action_selection_from_song)
        
        # Main frame
        main_frame = ttk.Frame(self.song_selection_window)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Panel de Selección por nombre y artistas
        name_art_frame = ttk.LabelFrame(main_frame, text="Busqueda por nombre y artistas")
        name_art_frame.pack(fill='both', expand=True, pady=5)
        
        self.name_song_var = tk.StringVar()
        self.artists_var = tk.StringVar()

        label = ttk.Label(name_art_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_song = ttk.Entry(name_art_frame, textvariable=self.name_song_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        label = ttk.Label(name_art_frame, text="Artistas:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        artists = ttk.Entry(name_art_frame, textvariable=self.artists_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(name_art_frame, text="Confirmar",
                 command=self._confirm_name_artists_selection,).grid(row=2,columnspan=2, sticky="ew")
        
    def _setup_loading_window(self,title,desc):

        self.loading_window = tk.Toplevel()
        self.loading_window.title(title)
        self.loading_window.protocol("WM_DELETE_WINDOW", lambda: self.throwError("ERROR","Espere a que termine el proceso"))
        self.loading_window.geometry("300x80")
        
        ttk.Label(self.loading_window,text=desc).pack(padx=5,pady=5)
        ttk.Progressbar(self.loading_window, mode='indeterminate').pack(pady=10, padx=20, fill=tk.X)

    def _setup_env_var_window(self):
        """Ventana para introducir ID y Secret de Spotify"""
        self.env_var_window = tk.Toplevel()
        self.env_var_window.title("Introduce tu ID y tu SECRET de la API de Spotify")
        self.env_var_window.protocol("WM_DELETE_WINDOW", self._return_to_action_selection_from_env_var)
        
        # Main frame
        main_frame = ttk.Frame(self.env_var_window)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        label = ttk.Label(main_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_song = ttk.Entry(main_frame, textvariable=self.spotifyId, width=30).grid(row=0, column=1, padx=5, pady=5)

        label = ttk.Label(main_frame, text="SECRET:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        artists = ttk.Entry(main_frame, textvariable=self.spotifySecret, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(main_frame, text="Guardar",
                 command=self._save_env_var,).grid(row=2,columnspan=2, sticky="ew")
    #-------------------------------------HELPERS--------------------------------------
    def _select_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
    
    def _confirm_path_selection(self):
        path = self.path_var.get()
        if path:
            self.path_window.withdraw()  # Oculta la ventana de selección
            self._setup_action_window(path)  # Muestra la ventana de acciones
            self.controller_callback("path:"+path)  # Notifica al controlador
    
    def _confirm_playlistSpot_selection(self):
        url = self.urlSpot_var.get()
        if url:
            self.playlistSpot_window.destroy()  # Oculta la ventana de selección
            self.action_window.deiconify()
            self.controller_callback("urlSpot:"+url)  # Notifica al controlador
    
    def _confirm_name_artists_selection(self):
        name = self.name_song_var.get()
        artists = self.artists_var.get()
        if name and artists:
            self.song_selection_window.destroy()  # Oculta la ventana de selección
            self.action_window.deiconify()
            self.controller_callback("name_arts:"+name+":"+artists)  # Notifica al controlador
    
    def _check_Spotify(self):
        if self.env_var_set:
            self._setup_playlistSpot_window()
        else:
            messagebox.showinfo("Antes...","Debes introducir tus claves de la API de Spotify.")
            self._setup_env_var_window()

    def _save_env_var(self):
        self._send_action("save_env",self.spotifyId.get()+":"+self.spotifySecret.get())
        self.env_var_set = True
        self.env_var_window.destroy()
    
    def _load_spot_env_var(self,id,secret):
        self.spotifyId.set(id)
        self.spotifySecret.set(secret)     

    def _send_action(self, action: str, arg: str):
        """Envía una acción al controlador"""
        print(f"Enviando acción al controlador: {action} {arg}")
        # Aquí normalmente llamarías a un método del controlador
        self.controller_callback(f"{action}:{arg}")
    
    def _return_to_path_selection(self):
        """Vuelve a la ventana de selección de path"""
        self.action_window.destroy()
        self.path_window.deiconify()
    
    def _return_to_action_selection_from_playlist(self):
        """Vuelve a la ventana de selección de acción"""
        self.playlistSpot_window.destroy()
        self.action_window.deiconify()

    def _return_to_action_selection_from_song(self):
        """Vuelve a la ventana de selección de acción"""
        self.song_selection_window.destroy()
        self.action_window.deiconify()
    
    def _return_to_action_selection_from_env_var(self):
        self.env_var_window.destroy()
        self.action_window.deiconify()
        
    def _on_close(self):
        """Maneja el cierre de la ventana"""
        self.root.quit()
    
    def _change_API_keys(self):
        self._send_action("load_API_keys","")
        self._setup_env_var_window() 

    #-------------------------------------PUBLIC FUNCTs--------------------------------------
    def run(self):
        self.root.mainloop()
    
    def throwError(self, title: str,desc: str):
        messagebox.showerror(title, desc)
    
    def throwInfo(self, title: str, desc: str):
        messagebox.showinfo(title, desc)

    def throwLoadingWindow(self,title: str, desc: str):
        self._setup_loading_window(title,desc)
    
    def deleteLoadingWindow(self):
        self.loading_window.destroy()
