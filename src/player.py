from music import Music
import pandas as pd
import pyautogui

class Player:
    def __init__(self):
        print("演奏者就绪")

    def get_music(self, music):
        self._music = music.music
        self._speed = music.speed
        self._interval = 60 / self._speed
        print("准备演奏: 《" + music.name + "》\n")

    def _update_speed(self, speed):
        self.speed = speed
        self.interval = 60 / speed

    def play(self):
        for i in range(len(self._music)):
            row = self._music.iloc[i]
            if row.iloc[0] == "s":  # 变速
                self._update_speed(row.iloc[2])
                continue
            self._play_one_row(row.iloc[1], row.iloc[2], row.iloc[3])

    def _play_one_row(self, keys, pause, lyrics):
        if keys is None:
            return
        pyautogui.typewrite(keys)
        pyautogui.sleep(pause * self._interval)
        if not pd.isnull(lyrics):
            print(lyrics, end="", flush=True)

    def move(self, direction, time):
        direction_to_key = {"left": 'a', "right": 'd', "forward": 'w', "backward": 's'}
        pyautogui.press("ctrl")
        pyautogui.keyDown(direction_to_key[direction])
        pyautogui.sleep(time)
        pyautogui.keyUp(direction_to_key[direction])

    def start_play(self):
        pyautogui.press("z")

    def stop_play(self):
        pyautogui.press("z")


if __name__ == '__main__':
    music = Music('resource/轻涟.xlsx')
    player = Player()
    player.get_music(music)
    pyautogui.sleep(5)
    # player.move("backward", 3)
    player.start_play()
    pyautogui.sleep(1)
    player.play()
