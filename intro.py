from colours import Colours
import time
import os


# Into: Clear screen and countdown
def intro():
    os.system("clear")
    print(f"{Colours.FAIL}{Colours.BOLD}{Colours.UNDERLINE}Prepare for funny video{Colours.END}")
    for countdown in range(3, 0, -1):
        print(f"{Colours.WARNING}{Colours.BOLD}{countdown}{Colours.END}")
        time.sleep(1)
    return True
