# -*- coding: utf-8 -*-
"""
Created on Sun May  5 23:07:02 2024
@author: jian0917
"""

from music import Music


def start_Genshin():
    pass


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    music = Music('../resource/轻涟.xlsx')
    df = music.music
    print(df)

