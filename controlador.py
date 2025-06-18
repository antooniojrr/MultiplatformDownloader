from gui import GUI
import downloader as dl
import threading
import os

class Controlador:
    def __init__(self,with_gui: bool = True):
        self.current_path = None
        self.env_file=".env"
        if with_gui:
            if self._check_env_var():
                self.gui = GUI(self._handle_gui_events,True)
            else:
                self.gui = GUI(self._handle_gui_events,False)
        else:
            self.gui = None
                        
    def _handle_gui_events(self, event_data: str):
        """Maneja todos los eventos provenientes de la GUI"""
        match event_data:

            case str() as s if s.startswith("path:"):
                self.current_path = event_data.split(":")[1]
                print(f"Path recibido en controlador: {event_data.split(':')[1]}")
                
            case str() as s if s.startswith("urlSpot:"):
                urlSpot = ""
                aux = event_data.split(":")
                urlSpot = [urlSpot + aux[i] for i in range(1,len(aux))]

                print(f"URL de playlist Spotify recibida en controlador: {urlSpot}")
                self.gui.throwLoadingWindow("Descargando","Espere mientras se descarga su Playlist")

                thread = threading.Thread(target=lambda: self._playlist_from_spotify(urlSpot), daemon=True)
                thread.start()
            
            case str() as s if s.startswith("name_arts:"):
                name = event_data.split(":")[1]
                artists = event_data.split(":")[2]
                print(f"Nombre de canción recibida en controlador: {name}")
                print(f"Artistas recibidos en controlador: {artists}")
                
                self.gui.throwLoadingWindow("Descargando","Espere mientras se descarga su canción")

                thread = threading.Thread(target=lambda: self._song_with_name_artist(name,artists), daemon=True)
                thread.start()
            
            case str() as s if s.startswith("save_env:"):
                id = event_data.split(":")[1]
                secret = event_data.split(":")[2]
                print(f"Variables de entorno recibidas en controlador:\n{id}\n{secret}")
                self._save_env_var(id,secret)
            
            case str() as s if s.startswith("load_API_keys:"):
                self._load_env_var()
                
    def _load_env_var(self):
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                variables = {}
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            variables[key.strip()] = value.strip()
                self.gui._load_spot_env_var(variables["CLIENT_ID"],variables["CLIENT_SECRET"])
    
    def _save_env_var(self,id,secret):
        try:
            with open(self.env_file, 'w') as f:
                f.write(f"CLIENT_ID={id}\n")
                f.write(f"CLIENT_SECRET={secret}\n")
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def _check_env_var(self):
        """Verifica si CLIENT_ID y CLIENT_SECRET ya están definidos en el archivo .env"""
        try:
            # Si el archivo no existe, las variables tampoco
            if not os.path.exists(self.env_file):
                return False

            with open(self.env_file, 'r') as f:
                content = f.read()

            # Verifica si ambas variables están definidas
            has_client_id = "CLIENT_ID=" in content
            has_client_secret = "CLIENT_SECRET=" in content

            return has_client_id and has_client_secret

        except Exception as e:
            print(f"Error al verificar el archivo .env: {e}")
            return False

    def _playlist_from_spotify(self, url: str):
        
        good = dl.playlist_from_Spotify(url,self.current_path)
        self.gui.deleteLoadingWindow()
        if not good:
            self.gui.throwError("ERROR","Fallo descargando la playlist")
        else:
            self.gui.throwInfo("EXITO","La playlist se ha descargado correctamente")
    
    def _song_with_name_artist(self, name: str, artists:str):
        
        good = dl.descargar_cancion(name,artists,self.current_path)
        if self.gui:
            self.gui.deleteLoadingWindow()
            if not good:
                self.gui.throwError("ERROR","Fallo descargando la canción")
            else:
                self.gui.throwInfo("EXITO","La canción se ha descargado correctamente")
    
    def _yt_sc_with_url(self, url: str):
        dl.descargar_con_url(url,self.current_path)

    def iniciar_aplicacion(self):
        self.gui.run()
    
    def set_current_path(self, path: str):
        self.current_path = path