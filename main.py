import os
import downloader as dl

if __name__ == "__main__":

    print("🎵🎵🎵Bienvenido a ToniDownloader🎵🎵🎵")

    dpath = input("Antes de nada, introduzca el path de descarga:\n")

    opt = ""
    while opt != "quit":
        opt = input("\nIntroduzca:\n\t\
                    - \'S\' si quiere descargar una canción\n\t\
                    - \'P\' si quiere descargar una playlist\n\t\
                    - \'QUIT\' si quiere finalizar\n").lower()

        match opt:
            case "p":
                id_playlist = input("Introduzca la URL o el ID de la playlist de Spotify que te gustaría descargar: ")
                dl.playlist_from_Spotify(id_playlist,dpath)
            case "s":
                tmp = ""
                while(tmp != "s" and tmp != "n"): 
                    tmp = input("¿Quiere buscarla por nombre y artistas? (S/N): ").lower()
                
                if tmp == "s":
                    nombre = input("Introduzca el nombre de la canción: ")
                    artistas = input("Introduzca los artistas separados por , : ")
                    dl.descargar_cancion(nombre,artistas,dpath)

                elif tmp == "n":
                    url = input("Introduzca la URL a la canción: ")
                    dl.descargar_con_url(url,dpath)
        
            
             



