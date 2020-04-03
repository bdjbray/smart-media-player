# smart-media-player

## Summary
A media player written with python.Users are able to use the player to play local video files.It supports multiple different video format.

## Goals
Basic goal:build a media player support the most common media format, users are able to check the videos that they watched recently</br>
Stretch goal:
1. Users are able to share the video with their friends.
2. The player could show the information about media.
3. The player could search the subtitles or lyrics for media file automatically, plus users could search and add these manually.
4. The player could recommend more songs or movies when user finsih the song or movie. 
## User Story
I am a user, I want to watch the videos that I have downloaded.</br>

I am a user, I want to browse the videos that I have watched recently.</br>

I am a user, I want to listen to music file that I have downloaded.</br>

I am a user, I want to I want to add album cover or post for music file and movie file.</br>

I am a user, I want to check more information about the song and movie like director, writer or performer baed on metadata of the file.(If the metadata lost I can also download these information manually by searching.)</br>

I am a user, I want to classify the file by genre so I can find the file more efficiently. For music file, it can be classified as pop music, folk music or R&B etc. For video file, it can be classified as drama film, cartoon or documentary etc.</br>

## Architecture 
Language:Python GUI tool:PyQt5

**Basic Architecture for player**:</br>
1. **I/O Module:** </br>
Input: URL link or local file </br>
Output: binary data.
2. **Parser&Demuxer Module:** </br>
Input: Binary data from I/O module.</br>
Output: Media information of the file, undecoded audio data and undecoded video data.
3. **Decode Module:**</br>
Input: Undecoded audio and video data package.</br>
Output: Decoded raw data of audio and video like PCM or YUV.
4. **Render Module:**</br>
Render the audio data and video data.

## Idea Example
Infuse Player on IOS</br>
![image](https://github.com/bdjbray/smart-media-player/blob/master/Images/552x414bb%20(1).png)
![image](https://github.com/bdjbray/smart-media-player/blob/master/Images/552x414bb.png)
![image](https://github.com/bdjbray/smart-media-player/blob/master/Images/infuse-5-apple-tv-title-detail-100708786-orig.jpg)