from controlador import Controlador
import argparse

def main():
    parser = argparse.ArgumentParser(description="Spotify Downloader")
    parser.add_argument("path", nargs="?", help="Ruta de descarga")
    parser.add_argument("--url", nargs="?", help="URL o ID de canción/playlist/album")
    parser.add_argument("--name", help="Nombre de la canción")
    parser.add_argument("--artist", help="Artista de la canción")

    args = parser.parse_args()
    app = Controlador(not (args.url or (args.name and args.artist)))

    if args.path:
        app.set_current_path(args.path)
        # URL
        if args.url:
            # Spotify
            if "open.spotify" in args.url:
                if "playlist" in args.url:
                    app._playlist_from_spotify(args.url)
                elif "album" in args.url:
                    print("HACERLO")
                elif "track" in args.url:
                    print("HACERLO")
                else:
                    print("ERROR con la URL de Spotify")
            elif "youtube.com" in args.url or "soundcloud.com" in args.url:
                app._yt_sc_with_url(args.url)
            else:
                print("ERROR: No se reconoce el tipo de URL o ID proporcionado")
        # Nombre y artista
        elif args.name and args.artist:
            app._song_with_name_artist(args.name, args.artist)
            
        else:
            app.iniciar_aplicacion()

if __name__ == "__main__":
    main()