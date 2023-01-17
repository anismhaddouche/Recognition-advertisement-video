
The aim of this project is to detect the beginning and the end of a commercial break in a given TV Channel. Our approach consists in searching the `Jingle`, of the channel, in a video stream. To this end we use the `ORB` (Oriented FAST and Rotated BRIEF) algorithm, included in `OpenCv`, in order to check how a video stream frame match with the `Jingle`. The project contains two scripts which are explained in the following.

1.  `extract_advertisements.py`: The aim of this script is to extract a Commercial break between two `Jingles`.
Usage: 
        
        python3 extract_advertisements.py ../Videos/test_resized.ts ../Frames_channels/ENTV.jpg

2. `time_advertisements.py`: The aim of this script is to write in the csv file `time_ads.csv` when the `jingle` appears.
Usage:

        python3 time_advertisements.py ../Videos/test_resized.ts ../Frames_channels/ENTV.jpg

Please see the documentation of each script for more details.
