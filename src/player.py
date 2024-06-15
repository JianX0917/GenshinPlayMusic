# -*- coding: utf-8 -*-
"""
Created on Sun May  5 23:07:02 2024
@author: jian0917
"""
import pandas as pd
import pyautogui

from music import Music


class Player:
    def __init__(self):
        self._interval = None
        self.speed = None
        self._music = None
        self.music_name = None
        print("演奏者就绪")

    def get_music(self, music):
        self._music = music.music
        self.speed = music.speed
        self._interval = 60 / self.speed
        self.music_name = music.name
        print("准备演奏: 《" + self.music_name + "》\n")

    def _update_speed(self, speed):
        # TODO : if speed <= 0 : raise ValueError("非法速度值") 
        self.speed = speed
        self._interval = 60 / speed

    def play(self):
        # TODO : if not self._music or not self._interval :raise PlayerError("异常提示")
        print("开始演奏: 《" + self.music_name + "》\n")
        for i in range(len(self._music)):
            row = self._music.iloc[i]
            if "s" in row.iloc[0]:  # 变速
                self._update_speed(row.iloc[2])
                continue
            if "a" in row.iloc[0]:  # 琶音
                self._play_arpeggio(row.iloc[1], row.iloc[2], row.iloc[3])
                continue
            self._play_one_row(row.iloc[1], row.iloc[2], row.iloc[3])

    def _play_one_row(self, keys, pause, lyrics):
        if keys:
            pyautogui.hotkey(keys)  # 弹奏音符
        if not pd.isnull(lyrics):
            print(lyrics, end="", flush=True)  # 打印歌词
        if pause:
            pyautogui.sleep(pause * self._interval)  # 停顿

    def _play_arpeggio(self, keys, pause, lyrics):
        keys_num = len(keys)
        arpeggio_interval = min(0.02, pause * self._interval / keys_num)  # 0.02时自定义的琶音间隔
        pyautogui.typewrite(keys, interval=arpeggio_interval)
        print(lyrics, end="", flush=True)  # 打印歌词
        pyautogui.sleep(pause * self._interval - arpeggio_interval * keys_num)  # 剩余停顿

    def move(self, direction, time):
        direction_to_key = {"left": 'a', "right": 'd', "forward": 'w', "backward": 's'}
        # TODO : if direction not in direction_to_key : raise PlayerError("移动方向非法")
        # TODO : if time <= 0 : raise PlayerError("移动时长非法")
        pyautogui.press("ctrl")  # 切换为行走模式
        pyautogui.keyDown(direction_to_key[direction])
        pyautogui.sleep(time)
        pyautogui.keyUp(direction_to_key[direction])
        pyautogui.press("ctrl")  # 切换回跑步模式

    def start_play(self):
        pyautogui.press("z")

    def stop_play(self):
        pyautogui.press("esc")


if __name__ == '__main__':
    music = Music('resource/轻涟.xlsx')
    player = Player()
    player.get_music(music)
    pyautogui.sleep(5)
    # player.move("backward", 3)
    player.start_play()
    pyautogui.sleep(2)
    player.play()
    player.stop_play()
