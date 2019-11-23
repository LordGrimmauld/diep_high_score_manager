import keyboard
from PIL import ImageGrab
import time
from typing import Optional
from ctypes import windll, create_unicode_buffer
import json
import subprocess
import os
from datetime import datetime

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    return buf.value if buf.value else None


try:
    with open("highscores.json", "r") as f:
        highscores = json.load(f)
except FileNotFoundError as e:
    with open("highscores.json", "w") as f:
        json.dump({}, f)
        highscores = {}


blockkeys = "wasdepuml1234567"  # keys that might block the combination of l + alt + prtscn


def take_pic():
    if "diep.io" in getForegroundWindowTitle():
        [keyboard.block_key(k) for k in blockkeys]
        keyboard.press("l")
        time.sleep(.1)
        keyboard.press_and_release("alt+prtscn")
        time.sleep(.05)
        keyboard.release("l")
        [keyboard.unblock_key(k) for k in blockkeys]
        time.sleep(.1)
        img = ImageGrab.grabclipboard()
        time.sleep(.1)
        img2 = img.crop((3*img.width//7, 13*img.height//14, 4*img.width//7, img.height))
        for x in range(img2.width):
            for y in range(img2.height):
                p = img2.getpixel((x, y))
                img2.putpixel((x, y), (0, 0, 0) if all(map(lambda x: x > 185, p)) and not all(map(lambda x: 207 > x > 195, p)) and p not in [(198, 198, 198), (205, 205, 205), (202, 202, 202)] else (0xff, 0xff, 0xff))
        img2.save("testimg.png", "PNG")
        time.sleep(.1)
        prc = subprocess.run("Tesseract-OCR\\tesseract.exe testimg.png stdout", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = prc.stdout.strip().split(b"\r\n")
        _score, _class = None, None
        for l in text:
            if b"Score" in l.strip():
                _score = int(l.strip().split()[1].decode().replace(",", "").replace(".", ""))
            elif l.strip().startswith(b"Lvl "):
                _class = l.strip().split()[2].decode()
        if _score is not None and _class is not None:
            print(_class, "with", _score)
            if _class in highscores:
                if _score > highscores[_class][0]:
                    if highscores[_class][1] in os.listdir("highscores"):
                        os.remove("highscores\\" + highscores[_class][1])
                else:
                    return
            filename = _class + "-" + str(_score) + "-" + datetime.now().strftime("%m~%d~%Y-%H~%M") + ".png"
            highscores[_class] = (_score, filename)
            img.save("highscores\\" + filename, "PNG")
            with open("highscores.json", "w") as f:
                json.dump(highscores, f)
        else:
            print(text)
            take_pic()  # Fixme: maybe not a good idea...
        # Imgur??? https://steemit.com/programming/@synapse/how-to-upload-images-to-imgur-using-python


keyboard.add_hotkey("p", take_pic)

