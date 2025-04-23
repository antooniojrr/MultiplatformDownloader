import yt_dlp
import os
import json

def descargar_cancion(nombre, artista, carpeta='descargas'):
    # Configurar opciones de descarga
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(carpeta, f'%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'default_search': 'ytsearch1:',
    }

    # Crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)

    # Buscar y descargar
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            resultado = ydl.download([f"{nombre} {artista} official audio"])
            print("\n✅ Descarga completada")
            return True
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return False

def descargar_con_url(url,carpeta ="descargas"):
    # Configurar opciones de descarga
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(carpeta, f'%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'default_search': 'ytsearch1:',
    }

    # Crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)

    # Buscar y descargar
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            resultado = ydl.download([url])
            print("\n✅ Descarga completada")
            return True
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return False

def descargar_todo(carpeta='descargas'):

    with open("data/songs.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    
    for s in datos:
        nombre = s["name"]
        artistas = s["artists"]
        descargar_cancion(nombre,artistas,carpeta)
    
    os.remove("data/songs.json")


def playlist_from_Spotify(url,carpeta):
    os.system(f"node spot_to_json.js \"${url}\" p")
    try:
        descargar_todo(carpeta)
        print("\n✅DESCARGAS COMPLETADAS✅")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def song_from_Spotify(url,carpeta):
    os.system(f"node spot_to_json.js \"${url}\" s")
    try:
        descargar_todo(carpeta)
        print("\n✅DESCARGA COMPLETADA✅")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

