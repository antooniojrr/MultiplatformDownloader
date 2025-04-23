
const axios = require('axios'); // Axios must be installed: npm install axios
require('dotenv').config();     // DotEnv must be installed: npm install dotenv
const fs = require('fs');
const path = require('path');

const clientId = process.env.CLIENT_ID;
const clientSecret = process.env.CLIENT_SECRET;

// Función principal
async function getPlaylistTracks(playlistIdentifier) {
  try {
    // Extraer ID de la playlist (ya sea de URL o ID directo)
    const playlistId = extractPlaylistId(playlistIdentifier);
    
    // Obtener token de acceso
    const accessToken = await getSpotifyToken();
    
    // Obtener las canciones
    const tracks = await fetchPlaylistTracks(playlistId, accessToken);
    
    // Formatear resultado
    const formattedTracks = tracks.map(track => ({
      name: track.track.name,
      artists: track.track.artists.map(artist => artist.name).join(', '),
      duration_ms: track.track.duration_ms,
      id: track.track.id
    }));
    
    return formattedTracks;
  } catch (error) {
    console.error('Error:', error.message);
    return [];
  }
}

// Helper para extraer el ID de la playlist
function extractPlaylistId(identifier) {
  // Si es una URL
  if (identifier.includes('spotify.com')) {
    const urlParts = identifier.split('/');
    const playlistPart = urlParts.find(part => part.includes('playlist'));
    if (!playlistPart) throw new Error('URL de playlist no válida');
    
    const idPart = urlParts[urlParts.indexOf(playlistPart) + 1];
    return idPart.split('?')[0]; // Eliminar parámetros de consulta
  }
  // Si ya es un ID
  return identifier;
}

// Obtener token de acceso de Spotify
async function getSpotifyToken() {
  const authString = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');
  
  const response = await axios.post('https://accounts.spotify.com/api/token', 
    'grant_type=client_credentials',
    {
      headers: {
        'Authorization': `Basic ${authString}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  
  return response.data.access_token;
}

// Obtener todas las canciones de la playlist (maneja paginación)
async function fetchPlaylistTracks(playlistId, accessToken, limit = 100) {
  let tracks = [];
  let url = `https://api.spotify.com/v1/playlists/${playlistId}/tracks?limit=${limit}`;
  
  while (url) {
    const response = await axios.get(url, {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    
    tracks = tracks.concat(response.data.items);
    url = response.data.next; // URL para la siguiente página (si existe)
  }
  
  return tracks;
}

// Helper para extraer el ID de la canción
function extractSongId(identifier) {
  // Si es una URL
  if (identifier.includes('spotify.com')) {
    const urlParts = identifier.split('/');
    const trackPart = urlParts.find(part => part.includes('track'));
    if (!trackPart) throw new Error('URL de canción no válida');
    
    const idPart = urlParts[urlParts.indexOf(trackPart) + 1];
    return idPart.split('?')[0]; // Eliminar parámetros de consulta
  }
  // Si ya es un ID
  return identifier;
}

// ARREGLAR
// Función principal para obtener los datos de la canción
async function getTrackInfo(trackId) {
  try {
    trackId = extractSongId(trackId);
    const accessToken = await getSpotifyToken();
    if (!accessToken) throw new Error('No se pudo obtener token de acceso');

    const response = await axios.get(
      `https://api.spotify.com/v1/track/${trackId}`,
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      }
    );

    const trackData = response.data;
    return {
      name: trackData.name,
      artists: trackData.artists.map(artist => artist.name).join(', '),
      album: trackData.album.name,
      release_date: trackData.album.release_date,
      duration_ms: trackData.duration_ms,
      spotify_url: trackData.external_urls.spotify
    };
  } catch (error) {
    console.error('Error al obtener información de la canción:', error.message);
    return null;
  }
}

/**
 * Guarda los datos en un archivo JSON (lo crea si no existe)
 * @param {Array} data - Datos a guardar
 * @param {string} filename - Nombre del archivo
 * @returns {Promise<boolean>} - True si se guardó correctamente
 */
async function saveToFile(data, filename = 'data/songs.json') {
    try {
        const dirname = path.dirname(filename);

        // Leer archivo existente si hay
        let existingData = [];
        if (fs.existsSync(filename)) {
            const fileContent = fs.readFileSync(filename, 'utf8');
            existingData = JSON.parse(fileContent);
        }

        // Crear directorio si no existe
        if (dirname && !fs.existsSync(dirname)) {
            fs.mkdirSync(dirname, { recursive: true });
        }

        // Convertir a JSON con formato legible combinando los datos
        const combinedData = [...existingData, ...data];
        const content = JSON.stringify(combinedData, null, 2);
        
        // Escribir archivo
        fs.writeFileSync(filename, content, 'utf8');
        
        console.log(`✅ Playlist guardada en: ${path.resolve(filename)}`);
        return true;
    } catch (error) {
        console.error('❌ Error al guardar el archivo:', error.message);
        return false;
    }
}

/**
 * Función principal que orquesta el proceso
 */
async function main() {
    try {
        // Obtener argumentos de la línea de comandos
        const [url, mode, outputFile = 'data/songs.json'] = process.argv.slice(2);

        switch(mode){
          case 'p':
            console.log(`🎵 Obteniendo canciones de la playlist...`);
            const tracks = await getPlaylistTracks(url);
            
            if (tracks.length === 0) {
                console.log('⚠️ No se encontraron canciones en la playlist');
                process.exit(0);
            }

            console.log(`📝 Encontradas ${tracks.length} canciones. Guardando...`);
            
            await saveToFile(tracks, outputFile);
            break;
          
          case 's':
            console.log(`🎵 Obteniendo información de la canción...`);
            const track = await getTrackInfo(url)
            console.log("EXITO\n\t"+track.name+" - "+track.artists)

            await saveToFile(track, outputFile);
            break;
        }
        
    } catch (error) {
        console.error('🔥 Error:', error.message);
        process.exit(1);
    }
}

// Ejecutar solo si es el archivo principal
if (require.main === module) {
    main();
}