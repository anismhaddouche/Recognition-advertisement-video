# TV-Advertisements-Detection

The aim of this project is to detect the beginning and the end of a commercial break in a given TV Channel. Our approche consists in searching the "Jingle", of the used channel, in a video stream. To this end we use the Orb(Oriented FAST and Rotated BRIEF) algorithm, included in OpenCv, in order to check how a video stream frame match with the Jingle. The project contains two scripts which are explained in the following.

## extract_advertisements.py
The interest of this script is to extracts a commerial break between two "Jingle".
usage: python3 exctract_advertisements.py ../Videos/test_resized.ts ../Frames_channels/ENTV.jpg

## time_advertisements.py
The aim of this script is to write in the csv file "time_ads.csv" when the jingle appears.
usage: python3 time_advertisements.py ../Videos/test_resized.ts ../Frames_channels/ENTV.jpg

Please see the documentions of each script for more details.


