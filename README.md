# Video To ASCII
A python generator that converts youtube videos to ascii art in your console. 
> This has not been tested for windows!

# Example
### Normal mode
![Gif Not Loaded](nonvideomode.gif)

### Video mode
![Gif Not Loaded](videomode.gif)

### CLI 
![Gif Not Loaded](cli.gif)

To see the full video click [here](https://www.youtube.com/watch?v=x2CgemU_bmQ)!

# How to use
Download the project as a zip, extract everything and then run the command below. Make sure to include `frames`.
### Installation
run `pip3 install youtube_dl opencv-python sty cursor pillow mss`
### Basic Command
`python3 ascii.py`

### Arguments
- `--framerate` this was used in the old version, may not work as of now
- `--buffer` buffer the whole video before rendering, this will freeze at "Buffering x/x" until done (recommended to be off)
- `--video_mode` changes to video mode if True

# Todo
- [x] Add CLI
- [x] Allow for other modes
- [x] Make it easier to use
- [x] Allow screen capture real time
- [ ] Allow for windows

