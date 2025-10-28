# MultiplatformDownloader

An audio downloader compatible with various websites. It includes functionality to read Spotify playlists and download the songs (not directly from Spotify, but by searching for them on other sources).

**This project has been developed for personal and practice purposes only.**

## 🚀 Features

* **Audio Download:** Allows downloading audio files from multiple web platforms.
* **Spotify Integration:** Reads Spotify playlists (via a helper script) to identify the songs to download.
* **Graphical Interface:** Features a GUI (Graphical User Interface) for ease of use.

## 🛠️ Technologies Used

* **Python:** Main language for the backend and application logic.
* **JavaScript:** Used in the `spot_to_json.js` script to process playlist information.

## 📂 Repository Structure

* `main.py`: Main entry point to run the application.
* `gui.py`: Defines the graphical user interface.
* `downloader.py`: Contains the logic for managing audio downloads.
* `controlador.py`: Acts as a controller/intermediary between the GUI and the download logic.
* `spot_to_json.js`: Helper script to extract Spotify playlist information.

## 🏁 Getting Started (Suggestion)

1.  Clone the repository:
    ```bash
    git clone [https://github.com/antooniojrr/MultiplatformDownloader.git](https://github.com/antooniojrr/MultiplatformDownloader.git)
    cd MultiplatformDownloader
    ```
2.  Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    Apart from this, it is necessary to have the JS libraries "axios" and "dotenv" installed as well.   

3.  Get your Spotify API's Client ID and Client Secret at:
    https://developer.spotify.com/dashboard

4.  Run the application and enter your obtained credentials:
    ```bash
    python main.py
    ```

## ⚠️ Disclaimer

This software is intended for personal and educational use only. The user is solely responsible for how they use this tool. The developers are not responsible for any misuse that may infringe on copyright.
