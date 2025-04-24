from gui import GUI
import downloader as dl
import threading

class Controlador:
    def __init__(self):
        self.gui = GUI(self._handle_gui_events)
        self.current_path = None
    
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
                
                
    
    def _playlist_from_spotify(self, url: str):
        
        good = dl.playlist_from_Spotify(url,self.current_path)
        self.gui.deleteLoadingWindow()
        if not good:
            self.gui.throwError("ERROR","Fallo descargando la playlist")
        else:
            self.gui.throwInfo("EXITO","La playlist se ha descargado correctamente")
    
    def _song_with_name_artist(self, name: str, artists:str):
        
        good = dl.descargar_cancion(name,artists,self.current_path)
        self.gui.deleteLoadingWindow()
        if not good:
            self.gui.throwError("ERROR","Fallo descargando la canción")
        else:
            self.gui.throwInfo("EXITO","La canción se ha descargado correctamente")
    
    def _process_path(self, path: str):
        print(f"Procesando archivos en: {path}")
        # Tu lógica de procesamiento aquí
    
    def _generate_report(self, path: str):
        print(f"Generando reporte para: {path}")
        # Tu lógica de generación de reportes aquí
    
    def _open_in_explorer(self, path: str):
        print(f"Abriendo en explorador: {path}")
        # Lógica para abrir en el explorador del sistema
    
    def iniciar_aplicacion(self):
        self.gui.run()