# TV-Advertisements-Detection
The aim of this project is to detecte the begenning and the end of a commercial break in a given TV Channel. Our approche consists in searching the "Jingle", of the used channel, in a video stream. To this end we use the Orb (Oriented FAST and Rotated BRIEF) algorithme, inculded in OpenCv, in order to check how a video stream frame match with the Jingle. The project contains two scripts which are explained in the following.

1- extract_advertisements.py: The interest of this script is to extracts a commerial break between two "Jingle".
usage: python3 exctract_advertisements.py ../Videos/test_resized.ts ../Frames_channels/ENTV.jpg

2- time_advertisements.py: The aim of this script is to write in the csv file "time_ads.csv" when the jingle appears.
usage: python3 time_advertisements.py ../Videos/test_resized.ts ../Frames_channels/ENTV.jpg

Please see the documations of each script for more details.

### Mise a jout de la raspberry