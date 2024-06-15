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

    # 加载乐谱
    def get_music(self, music):
        self._music = music.music
        self.speed = music.speed
        self._interval = 60 / self.speed
        self.music_name = music.name
        print("准备演奏: 《" + self.music_name + "》\n")

    # 更新速度值
    def _update_speed(self, speed):
        if speed <= 0:
            raise PlayerException("更新速度值 {} 非法".format(speed))
        self.speed = speed
        self._interval = 60 / speed

    # 演奏乐曲
    def play(self):
        if self._music is None:
            raise PlayerException("未获得乐谱,无法演奏")
        if not self._interval:
            raise PlayerException("未设置演奏速度,无法演奏")
        print("开始演奏: 《" + self.music_name + "》\n")
        for i in range(len(self._music)):
            row = self._music.iloc[i]
            # 根据该行的标识符决定该行处理方式
            if "s" in row.iloc[0]:  # 变速
                self._update_speed(row.iloc[2])
            elif "a" in row.iloc[0]:  # 演奏琶音
                self._play_arpeggio(row.iloc[1], row.iloc[2], row.iloc[3])
            else:  # 正常演奏
                self._play_one_row(row.iloc[1], row.iloc[2], row.iloc[3])

    # 弹奏一行
    def _play_one_row(self, keys, pause, lyrics):
        if keys:
            pyautogui.hotkey(keys)  # 弹奏音符
        if not pd.isnull(lyrics):
            print(lyrics, end="", flush=True)  # 打印歌词
        if pause:
            pyautogui.sleep(pause * self._interval)  # 停顿

    # 弹奏琶音
    def _play_arpeggio(self, keys, pause, lyrics):
        keys_num = len(keys)
        arpeggio_interval = min(0.02, pause * self._interval / keys_num)  # 0.02时自定义的琶音间隔
        pyautogui.typewrite(keys, interval=arpeggio_interval)
        if not pd.isnull(lyrics):
            print(lyrics, end="", flush=True)  # 打印歌词
        pyautogui.sleep(pause * self._interval - arpeggio_interval * keys_num)  # 剩余停顿

    # 控制人物走路
    def walk(self, direction, time):
        direction_to_key = {"left": 'a', "right": 'd', "forward": 'w', "backward": 's'}
        pyautogui.press("ctrl")  # 切换为行走模式
        try:
            pyautogui.keyDown(direction_to_key[direction])
        except KeyError:
            raise PlayerException("移动方向 {} 非法".format(direction))
        try:
            pyautogui.sleep(time)
        except ValueError:
            raise PlayerException("移动时长 {} 非法".format(time))
        pyautogui.keyUp(direction_to_key[direction])
        pyautogui.press("ctrl")  # 切换回跑步模式

    # 打开风物之诗琴
    def start_play(self):
        pyautogui.press("z")

    # 关闭风物之诗琴
    def stop_play(self):
        pyautogui.press("esc")


# 异常类型
class PlayerException(Exception):
    def __init__(self, message):
        super().__init__(message)


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
