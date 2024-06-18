# -*- coding: utf-8 -*-
"""
Created on Sun May  5 23:07:02 2024
@author: jian0917
"""

import logging
import subprocess
import threading
from multiprocessing import Process

import pyautogui
# import msvcrt  # 该库只能在Windows平台上使用，遂未使用，使用pynput代替
from pynput.keyboard import Key, Listener

from music import Music
from player import Player


# 启动原神的应用程序
def _run_Genshin_exe(Genshin_path):
    print("原神，启动！")
    subprocess.run(Genshin_path)


# 进入原神游戏
def start_Genshin():
    Genshin_path = "D:\Download\原神\Genshin Impact\Genshin Impact Game\YuanShen.exe"
    try:
        p = Process(target=_run_Genshin_exe, args=[Genshin_path])  # 另开一个进程来启动原神，因为subprocess.run()会阻塞
        p.start()  # 启动进程
        pyautogui.sleep(10)
        p.terminate()  # 结束该进程
        pyautogui.sleep(20)
        pyautogui.click()
        pyautogui.sleep(20)
    except FileNotFoundError:
        logging.error("路径错误，请输入正确的程序路径")


# 监听键盘esc，若esc摁下，提前终止player的演奏;选择esc键作为提前结束的信号是保留了诗琴的esc退出的操作逻辑
def _esc_listener(player):
    # 使用一个守护线程来监听键盘esc键的输入，如果esc被摁下，提前终止演奏
    def on_press(key):
        try:
            if key == Key.esc:
                player.is_stopped = True
        except AttributeError:
            pass

    def on_release(key):
        try:
            if key == Key.esc:
                return False  # 停止监听
        except AttributeError:
            pass

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# 演奏乐曲并启动守护线程监听esc键
def start_play_music():
    global player
    # 创建一个守护线程来监听esc，当esc摁下时终止演奏
    keyboard_thread = threading.Thread(target=_esc_listener, args=[player], daemon=True)
    keyboard_thread.start()
    # 演奏
    player.start_play()
    player.play()
    if player.is_stopped:
        player.is_stopped = False
        print("手动停止演奏")
    else:  # 当没有提前终止时才自动摁下esc退出诗琴界面
        player.stop_play()


if __name__ == '__main__':
    player = Player()
    player.get_music(Music('resource/天空之城.xlsx'))
    start_Genshin()
    start_play_music()
    pyautogui.sleep(3)
    player.get_music(Music('resource/轻涟.xlsx'))
    start_play_music()
