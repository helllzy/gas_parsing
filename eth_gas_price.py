import time

from threading import Thread
from pystray import Icon, Menu, MenuItem
from web3 import Web3
from PIL import Image, ImageFont, ImageDraw


def reload_icon(icon: Icon) -> None:
    draw_image()
    time.sleep(0.5)
    icon.icon = img


def reload_forever() -> None:
    while is_running:
        try:
            reload_icon(icon)
            time.sleep(2)
        except:
            pass


def draw_image(size=55, location=(0,0)) -> None:
    while True:
        try:
            web3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))
            global img
            gas = round(web3.eth.gas_price//10**9)
            img = Image.new('RGBA', (64, 64), color = (0,0,0,0))
            
            if gas >= 100:
                size = 40
                location = (-1,5)
            
            fnt = ImageFont.truetype("arial.ttf", size)
            ImageDraw.Draw(img).text(location, str(gas), font=fnt, fill=(255,255,245))
            break
        except:
            pass


def exit_app() -> None:
    icon.stop()
    global is_running
    is_running = False


if __name__ == '__main__':
    is_running = True

    draw_image()

    icon = Icon(
        'ETH_GAS_PRICE',
        icon=img,
        menu=Menu(
            MenuItem("Reload", lambda _: reload_icon(icon)),
            MenuItem("Exit", exit_app))
        )

    t = Thread(target=reload_forever)

    t.start()

    icon.run()
