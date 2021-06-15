# Made by NexInfinite
# Project started 10/06/21
# ASCII Art
# This is one big file, I hate it; working on a multi file system but am a lil lazy

# Imports
# Local imports
import youtubedl_saver as ydls
from colours import Colours
from intro import intro

# External imports
import cv2
import os
import sys
import argparse
import time
from threading import Thread
import datetime
from sty import fg
import cursor
from PIL import Image


# Frame renderer
def render_frame():
    global buffer, queue, inverted, global_width, global_height, image_buffer, rendered_images

    while True:
        # Read next image from video
        _success, _image = vidcap.read()
        if _success:
            # If there is still a frame render it and add it to frames
            resize_image(_image)
        elif not _success and not rendered_images:
            # else start threads, making sure to only run this once
            rendered_images = True
            for thread in range(3):
                # Starting a thread and running it 3 times
                render_frame_thread = Thread(target=render_frame_buffer, args=[thread])
                render_frame_thread.start()
        elif frames == total_frames:
            # Once video is over do this!
            os.remove("video")
            print(f"{Colours.FAIL}{Colours.BOLD}{Colours.UNDERLINE}Goodbye!{Colours.END}")
            sys.exit()


def resize_image(_image):
    global buffer, queue, inverted, global_width, global_height, image_buffer
    # Changing the height and width of the image
    height = int(global_width / 10)
    width = int(global_height / 10)
    # Saving it as a smaller image
    resized_image = cv2.resize(_image, (height, width))
    cv2.imwrite(f"frames/frame{image_buffer}.jpg", resized_image)
    image_buffer += 1


def render_frame_buffer(thread):
    global image_buffer, buffer
    # Rendering an ascii image and adding to the queue
    for frame in range(image_buffer):
        if frame % 3 == thread:
            # Using mod so that they render in sync
            _img = Image.open(f"frames/frame{frame}.jpg")

            width, height = _img.size
            pix = _img.load()

            # Get the frame and add it to the queue (using recursion)
            queue[frame] = "\n".join(get_full_frame(0, 0, height, width, [], pix))
            os.remove(f"frames/frame{frame}.jpg")
            buffer += 1


def get_x_frame(x, y, height, width, outputs, pix):
    # Render each column (x) of an image using recursion.
    if x == width - 2:
        return outputs  # <-- The classic recursion ocr question (this is where the recursion occurs)
    else:
        # Anyway, here we render the row with different ascii characters based on their brightness
        ascii_outputs = {51: "--", 70: "++", 130: "**", 180: "==", 255: "##"}
        r, g, b = pix[x, y]
        brightness = sum([r, g, b]) / 3
        for output in ascii_outputs:
            if brightness <= output:
                # Appending to full frame and colouring each "pixel" of ascii characters according to pil
                outputs.append(fg(r, g, b)+ascii_outputs[output]+fg.rs)
                return get_x_frame(x + 1, y, height, width, outputs, pix)


def get_full_frame(x, y, height, width, full_frame, pix):
    # More recursion, this time for each row (y)
    if y == height - 2:
        return full_frame
    else:
        # adding to full frame
        x_frame = "".join(get_x_frame(0, y, height, width, [], pix))
        full_frame.append(x_frame)
        return get_full_frame(x, y + 1, height, width, full_frame, pix)


# Framerate handler
def run_queue():
    global queue, framerate, frames, frame_begin_time, begin_time, restart
    # This bit is a bit messy, this is what controls the queue
    # Setting up some variables to stop repeats in the loop!
    start = False
    lock = False
    timer = False
    # Used for the second timer, means it wont repeat 1000s of times a second; after all we are in a while True loop
    checker_second = 0
    while True:
        if len(queue) >= total_frames * buffer_amount - 1 and rendered_images:
            # Checks when the images are fully rendered, then allows for ascii to start being generated
            start = True

        if frames == total_frames:
            # Checks if the everything is over
            return

        if (len(queue) >= total_frames * buffer_amount - 1 or start) and lock:
            if not timer:
                # Begins the timer, we only want this to happen once, a couple other things start now
                # Variables to stop repeating
                start = True
                timer = True

                # Timings used to space out frames, this is very important
                begin_time = datetime.datetime.now()
                frame_begin_time = datetime.datetime.now()

                # Starting the seconds timer, this is what actually displays the frames, this is explained below
                render_second_thread = Thread(target=render_second)
                render_second_thread.start()

            # Gets the datetime, this is what allows for second resets; this bit is a little complicated so prepare for comment hell.
            # When displaying frames for one second you would think it makes sense to take 1/framerate to space them out. This works
            # but you need to remember to account for time taken to do calculations, this all adds up and before you know it you're 10
            # seconds behind. There also may be things that 1 second only render 20 frames instead; this could be because of an external
            # script or a slow pc. We don't want to be behind so we trigger a reset code every second; this allows the queue to catch
            # up to the point its meant to be, this is what the following code is for!
            checker = datetime.datetime.now() - begin_time
            if round(checker.microseconds / 1000000, 1) == 0 and checker_second < checker.seconds:
                # This checks if its the start of a second, we then change the checker_second so that this only happens once in this particular second.
                # Setting restart to true allows the above comments to occur in the render_second_thread
                restart = True
                checker_second = checker.seconds
        elif not start:
            os.system(f"clear && echo '{Colours.GREEN}{Colours.BOLD}Buffering: {image_buffer}/{round(total_frames)} (Rendering all images, it works somehow :P){Colours.END}'")
        elif not lock:
            intro()
            lock = True


# Rendering 1 second of playtime
def render_second():
    global queue, framerate, frames, frame_begin_time, begin_time, restart
    # setting time delay and the amount of frames we have rendered so far in this second
    time_delay = (duration / total_frames)
    render_frames = 0
    while True:
        if restart:
            # This is where the restart happens, if this is triggered it deletes all frames not rendered from the queue!
            not_rendered = framerate - (render_frames % framerate)
            if framerate > not_rendered > 0:
                for _ in range(not_rendered):
                    try:
                        queue.pop(frames)
                        frames += 1
                    except IndexError:
                        # This will ONLY occur if its the end of the video, so we can say Goodbye!
                        print(f"{Colours.FAIL}{Colours.BOLD}{Colours.UNDERLINE}Goodbye!{Colours.END}")
                        pass
            # Resetting variables so that it doesn't trigger multiple times in 1 second.
            render_frames = 0
            restart = False
            pass
        else:
            try:
                if render_frames < framerate:
                    # Popping the queue, this is incredibly useful to cut down on memory usage
                    # We also increment frames and rendered frames
                    item = queue.pop(frames)
                    frames += 1
                    render_frames += 1

                    # Sleeping, this also accounts for the time taken for the frame to be rendered and other things slowing down your pc
                    sleep = time_delay - ((datetime.datetime.now() - frame_begin_time).microseconds / 1000000)
                    if sleep > 0:
                        # Cant sleep a negative amount of time!
                        time.sleep(sleep)
                    # Starting the new time and finally outputting a frame
                    frame_begin_time = datetime.datetime.now()
                    display_frame(item)
            except:
                # Again this only happens once the video is over, we can say goodbye at this point!
                print(f"{Colours.FAIL}{Colours.BOLD}{Colours.UNDERLINE}Goodbye!{Colours.END}")
                return


def display_frame(item):
    # Rendering an output as 1 message to try cut down on delays.
    output = f"{Colours.FAIL}{Colours.BOLD}{Colours.UNDERLINE}Information about the video{Colours.END}" \
             f"\n{Colours.WARNING}{Colours.BOLD}Tabbing out may crash this, stopping the program is a bit buggy, may need to spam ctrl c till it stops.{Colours.END}" \
             f"\n{Colours.GREEN}{Colours.BOLD}Frame {frames}/{buffer} at {framerate}fps ({total_frames} frames in total){Colours.END}" \
             f"\n{Colours.GREEN}{Colours.BOLD}{(datetime.datetime.now() - begin_time)}/{datetime.timedelta(seconds=duration)}{Colours.END}" \
             f"\n{item}" \
             f"\nMade by NexInfinite on Youtube and Github"
    clear = "\n" * global_height
    os.system(f"echo '{clear}{output}'")


if __name__ == "__main__":
    # Get all the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("vid", help="Where the video is located", type=str)
    parser.add_argument("--framerate", dest="framerate", help="Frame rate (Default 30)", type=int, default=30)
    parser.add_argument("--buffer", dest="buffer", help="Buffer amount 0-1", type=float, default=0)
    args = parser.parse_args()

    # Process arguments
    if args.vid.lower().startswith("https://"):
        # Getting video information
        video_location, framerate, total_frames, duration = ydls.save_file(args.vid)
        vidcap = cv2.VideoCapture(video_location)
        success, image = vidcap.read()

        # Getting timing information
        begin_time = datetime.datetime.now()
        frame_begin_time = datetime.datetime.now()

        # Setting up values
        # Boolean values
        restart = False
        rendered_images = False
        # Integer values
        frames = 1
        popped = 1
        image_buffer = 0
        buffer = 0
        buffer_amount = args.buffer
    else:
        print("Needs to be a youtube video!")
        sys.exit()
    queue = {}
    cv2.imwrite(f"frames/frameTEST.jpg", image)
    img = Image.open(f"frames/frameTEST.jpg")
    global_width, global_height = img.size

    try:
        # Hiding cursor
        cursor.hide()

        # Creating threads
        queue_thread = Thread(target=run_queue)
        render_thread = Thread(target=render_frame)

        # Starting threads
        render_thread.start()
        queue_thread.start()

        # Ending threads
        render_thread.join()
        queue_thread.join()
    except:
        # Show the cursor
        cursor.show()

        # Cleaning up video
        os.remove("video")
        for i in total_frames:
            try:
                os.remove(f"frames/frame{i}.jpg")
            except:
                pass

        # Saying bai!
        print(f"{Colours.FAIL}{Colours.BOLD}{Colours.UNDERLINE}Goodbye!{Colours.END}")
        sys.exit()
