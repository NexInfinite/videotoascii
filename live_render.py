import os
import time
import cursor
from datetime import datetime as dt
from threading import Thread
from colours import Colours
from PIL import Image
from pynput import keyboard

import mss
from sty import fg, bg


def render_image_thread(thread):
    global fps, img, stopped, out, image_buffer, reset, start, last_second, has_started
    local_frames = 0
    desired_image_buffer = framerate
    while not stopped:
        if reset:
            local_frames = 0
            reset = False

        if has_started:
            if last_second > 0:
                desired_image_buffer = framerate * (last_second + 1)

        if has_started and image_buffer < desired_image_buffer:
            # Changing width and height to make it easier to render ascii art
            height = int(mon["height"] / 30)
            width = int(mon["width"] / 30)

            # Resizing images with height, width and saving it#
            sct_img = sct.grab(mon)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img = img.resize((width, height), Image.ANTIALIAS)
            pix = img.load()
            display_frame("\n".join(get_full_frame(0, 0, height, width, [], pix)), thread)

            # Incrementing counters if image has saved!
            image_buffer += 1
            local_frames += 1
            fps += 1
    return


def get_x_frame(x, y, height, width, outputs, pix):
    # Render each column (x) of an image using recursion.
    if x == width - 2:
        return outputs  # <-- The classic recursion ocr question (this is where the recursion occurs)
    else:
        # Anyway, here we render the row with different ascii characters based on their brightness
        # ascii_outputs = {51: "--", 70: "++", 130: "**", 180: "==", 255: "##"}
        if watching_video:
            ascii_outputs = {51: "--", 70: "++", 130: "**", 180: "==", 255: "##"}
        else:
            ascii_outputs = {50: ["  ", fg.white],
                             70: ["..", fg.li_grey],
                             130: ["--", fg.li_grey],
                             230: ["~~", fg.grey],
                             240: ["++", fg.da_black],
                             255: ["  ", fg.black]}
        r, g, b = pix[x, y]
        brightness = sum([r, g, b]) / 3
        for output in ascii_outputs:
            if brightness <= output:
                # Appending to full frame and colouring each "pixel" of ascii characters according to pil
                if watching_video:
                    outputs.append(fg(r, g, b) + ascii_outputs[output] + fg.rs)
                    return get_x_frame(x + 1, y, height, width, outputs, pix)
                else:
                    outputs.append(bg(r, g, b) + ascii_outputs[output][1] + ascii_outputs[output][0] + fg.rs + bg.rs)
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


def timing_module():
    global stopped, start_all_threads, reset, start, last_second, has_started
    last_second = 0
    start = dt.now()

    while True:
        if round(dt.now().microsecond / 1000000, 2) == 0 and not has_started:
            start = dt.now()
            has_started = True

        if (dt.now() - start).seconds >= last_second + 1 and has_started:
            last_second += 1
            reset = True


def display_frame(item, thread):
    # Rendering an output as 1 message to try cut down on delays.
    output = f"{Colours.FAIL}{Colours.BOLD}{Colours.UNDERLINE}Information{Colours.END}" \
             f"\n{Colours.WARNING}{Colours.BOLD}Rendered on thread: {thread}{Colours.END}" \
             f"\n{Colours.WARNING}{Colours.BOLD}Video mode (Right Shift to Toggle)? {watching_video}{Colours.END}" \
             f"\n{Colours.GREEN}{Colours.BOLD}{(dt.now() - start)}{Colours.END}" \
             f"\n{item}" \
             f"\nMade by NexInfinite on Youtube and Github"
    clear = "\n" * 100
    os.system(f"echo '{clear}{output}'")


def input_checker(key):
    global watching_video

    if key == keyboard.Key.shift_r:
        if watching_video:
            watching_video = False
        else:
            watching_video = True


if __name__ == "__main__":
    # creating arguments
    mon = {"top": 0, "left": 0, "width": 1920, "height": 1080}

    # Creating the queue
    fps = 0
    image_buffer = 0
    framerate = 30

    sct = mss.mss()
    last_time = dt.now()

    stopped = False
    watching_video = False
    reset = False
    has_started = False

    print("Clearing last test")
    for i in range(10000):
        try:
            os.remove(f"/mnt/9E827B67827B42B7/Desktop/Coding/asciiartlive/frames/frame{i}.jpg")
        except:
            pass

    # Handling keyboard inputs
    listener = keyboard.Listener(
        on_press=input_checker)
    listener.start()

    # Creating multi-threads
    video_capture_thread_0 = Thread(target=render_image_thread, args=[0])
    video_capture_thread_1 = Thread(target=render_image_thread, args=[1])
    video_capture_thread_2 = Thread(target=render_image_thread, args=[2])
    video_capture_thread_3 = Thread(target=render_image_thread, args=[3])

    # Starting multi-threads
    sleep_time = 1 / 8
    print("Starting thread 0")
    time.sleep(sleep_time)
    video_capture_thread_0.start()
    print("Starting thread 1")
    time.sleep(sleep_time)
    video_capture_thread_1.start()
    print("Starting thread 2")
    time.sleep(sleep_time)
    video_capture_thread_2.start()
    print("Starting thread 3")
    time.sleep(sleep_time)
    video_capture_thread_3.start()

    # Timing module (this ends everything)
    try:
        cursor.hide()
        timing_module()
    except:
        cursor.show()
        stopped = True
        video_capture_thread_0.join()
        video_capture_thread_1.join()
