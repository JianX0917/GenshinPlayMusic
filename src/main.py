# -*- coding: utf-8 -*-
"""
Created on Sun May  5 23:07:02 2024
@author: jian0917
"""

import subprocess
from multiprocessing import Process

import pyautogui

from music import Music
from player import Player


# 启动原神的应用程序
def open_Genshin_exe():
    Genshin_path = "D:\Download\原神\Genshin Impact\Genshin Impact Game\YuanShen.exe"
    print("原神，启动！")
    subprocess.run(Genshin_path)


def start_Genshin():
    p = Process(target=open_Genshin_exe)  # 另开一个进程来启动原神，因为subprocess.run()会阻塞
    p.start()  # 启动进程
    pyautogui.sleep(10)
    p.terminate()  # 结束该进程
    pyautogui.sleep(20)
    print("点了一下")
    pyautogui.click()
    pyautogui.sleep(20)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    music = Music('resource/轻涟.xlsx')
    player = Player()
    player.get_music(music)
    start_Genshin()
    player.start_play()
    player.play()
    player.stop_play()
