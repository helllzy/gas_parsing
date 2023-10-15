import time

from threading import Thread
from pystray import Icon, Menu, MenuItem
import requests
from PIL import Image, ImageFont, ImageDraw


def reload_icon(icon):
    draw_image()
    time.sleep(0.5)
    icon.icon = img


def reload_forever():
    while is_running:
        try:
            reload_icon(icon)
            time.sleep(2)
        except:
            pass


def draw_image():
    while True:
        try:
            global img
            url = 'https://alpha-mainnet.starknet.io/feeder_gateway/get_block?blockNumber=latest'
            response = requests.get(url)
            gas = str(round(int(response.json()["gas_price"], 16)//10**9, 0))
            img = Image.new('RGBA', (64, 64), color = (0,0,0,0))
            fnt = ImageFont.truetype("arial.ttf", 55)
            ImageDraw.Draw(img).text((0,0), gas, font=fnt, fill=(0,255,245))
            break
        except:
            pass


def exit_app():
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
