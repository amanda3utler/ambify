# ambify
### *vibe your life*
An automatic ambient music player for your Spotify playlists.

## Installation
Necessary dependencies include streamlit, pygame, numpy, pandas, Pillow, time, requests, and spotipy.

Git clone or download locally and run:

```
pip install .
```
from within the home directory (ambify/).
To launch the application in the same directory, run:
```
streamlit run interface.py
```
## Use
Ambify uses the Spotify API to acquire information on a user's playlists and automatically generate an appropriate "vibe" for the playlist in the form of visual panels and audio.

Using the streamlit interface, enter a spotify username. **If** your username does not appear to be valid and an error arises, enter the last section of the spotify user URI string, formatted as spotify:user:yourusername. To access this substring (yourusername in my example), select the more info dots under your profile, and after the holding option key, select "Copy Spotify URI". 

After succesfully entering a username, enter a public playlist name in the playlist box (case-sensitive) and select **Get my ambience!**. For private playlist access, you can paste in the **full** playlist URI accessed similarly to above.

Entering **RANDOM!** in the playlist box will output a random audio, but visuals are not currently suppported for this feature at the moment. 

Pressing **Stop Audio** stops the playing of audio. Entering **Get my ambience!** again will restart the audio for the same playlist or a new playlist (if new playlist entered). Visuals remain in this scenario. 

Ambify also returns a suggested volume level for each ambient audio (suggested for when headphones are being used).

Stopping the audio with **Stop Audio** before exiting is recommended.
## Citations
All audio purchased from: https://www.freetousesounds.com/



