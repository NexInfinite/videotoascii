from __future__ import print_function, unicode_literals

import os
import subprocess
import sys

import regex
from PyInquirer import prompt, Validator, ValidationError

from colours import Colours


class UrlValidator(Validator):
    def validate(self, document):
        is_valid = regex.match(
            '^(http(s)??\:\/\/)?(www\.)?((youtube\.com\/watch\?v=)|(youtu.be\/))([a-zA-Z0-9\-_]){11}$', document.text)
        if not is_valid:
            raise ValidationError(
                message='Please enter a correct url (must be in form https://youtube.com/watch?v=VIDEO_ID)',
                cursor_position=len(document.text))


class BufferValidator(Validator):
    def validate(self, document):
        try:
            if not 0 <= float(document.text) <= 1:
                raise ValidationError(
                    message='Buffer amount must be between 0 and 1',
                    cursor_position=len(document.text))
        except ValueError:
            raise ValidationError(
                message='Buffer amount must be between 0 and 1',
                cursor_position=len(document.text))


question1 = [
    {
        'type': 'list',
        'name': 'type',
        'message': 'What do you want to do?',
        'choices': [
            'Video, this will render a youtube video.',
            'Screen, this will render your screen (screen 0) live; there is a little bit of lag and quality is reduced.'
        ]
    }
]

answers = prompt(question1)
if answers['type'].lower().startswith("video"):
    question2 = [
        {
            'type': 'input',
            'name': 'url',
            'message': 'What\'s the url?',
            'validate': UrlValidator
        },
        {
            'type': 'input',
            'name': 'buffer',
            'message': 'How much do you want to buffer (0-1)?',
            'validate': BufferValidator,
            'default': '0'
        },
        {
            'type': 'list',
            'name': 'video_mode',
            'message': 'Do you want to run this in video mode (Video mode means the characters are highlighted instead of coloured, this makes colours more vibrant)?',
            'choices': [
                'Yes',
                'No'
            ]
        }
    ]

    answers = prompt(question2)
    command = f"python3 video_render.py {answers['url']} --buffer={answers['buffer']} --video_mode={True if answers['video_mode'] == 'Yes' else False}"
else:
    command = f"python3 live_render.py"

print(f"\n\n-----------------------------------"
      f"\n{Colours.FAIL}{Colours.BOLD}PLEASE READ{Colours.END}")
print(f"The following program can lag or crash your computer, it is not designed for all computers. "
      f"If you experience any issues with your computer as a result of this program it is your fault, only run "
      f"this program if you know your pc will handle it. To end the program press CTRL + C. If this doesn't stop it "
      f"you may need to press it a couple times or send a kill signal with task manager."
      f"\n\n{Colours.FAIL}{Colours.BOLD}RUN THIS AT YOUR OWN RISK.{Colours.END}"
      f"\n\n{Colours.GREEN}Also you can use right shift to change the mode of the renderer!{Colours.END}"
      f"\n-----------------------------------\n\n")
question2 = [
    {
        'type': 'confirm',
        'name': 'warning',
        'message': 'By confirming this you are agreeing that you have read and agree to the statement above'
    }
]
if not prompt(question2)['warning']:
    print("Cannot run program as you did not agree")
    sys.exit()

try:
    print(f"Running {command}")
    os.system(command)
except Exception as e:
    print(e)
    if isinstance(e, KeyError):
        sys.exit()
    elif isinstance(e, subprocess.CalledProcessError):
        print("Goodbye!")
    else:
        print(f"Unhandled Error: {e}"
              f"\nThis could be because you don't have python installed!")
