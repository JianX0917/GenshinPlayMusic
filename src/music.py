# -*- coding: utf-8 -*-
"""
Created on Sun May  5 23:07:02 2024
@author: jian0917
"""

import pandas as pd


class Music:
    # 简谱至键盘谱转换表
    _dic = {"+1": "Q", "+2": "W", "+3": "E", "+4": "R", "+5": "T", "+6": "Y", "+7": "U",
            "1": "A", "2": "S", "3": "D", "4": "F", "5": "G", "6": "H", "7": "J",
            "-1": "Z", "-2": "X", "-3": "C", "-4": "V", "-5": "B", "-6": "N", "-7": "M"}

    def __init__(self, file_path):
        # 读取Excel乐谱
        column_names = ['标记', '音符', '间隔', '歌词']
        dtype = {'标记': str, '音符': str, '间隔': float, '歌词': str}
        self.music = pd.read_excel(file_path, index_col=False, header=0, names=column_names, dtype=dtype)
        # 设置速度
        if self.music.empty or self.music.iloc[0, 0] != 's':
            raise ValueError("乐谱格式有误")
        if self.music.iloc[0, 2] <= 0:
            raise ValueError("乐谱速度有误")
        self.speed = self.music.iloc[0, 2]
        self.music = self.music.drop(0)
        # 从Excel中读取乐名，若Excel中未设置乐名，则以Excel文件名作为默认乐名
        self.name = self._get_name(file_path)
        # 简谱转换至键盘谱
        self._notation_conversion()
        # TODO:使用日志打印错误信息  使用列表记录错误信息  若列表为空  则打印乐谱准备完成 否则记录错误信息
        # TODO:记录已抛弃行数指针 用于打印错误信息时指明第几行错误
        print("乐谱准备完成")

    def _get_name(self, file_path):
        name = None
        # 优先从Excel中读取乐名
        if self.music.empty or self.music.iloc[0, 0] == 'n':
            name = self.music.iloc[0, 1]
            self.music = self.music.drop(1)
        # 无法从Excel中读取到乐名，将Execl文件名作为默认乐名
        if name is None:
            name = file_path.split('/')[-1].split('.')[0].replace('_', ' ')
        return name

    # TODO:改成手动转换，不要自动一列一列的转换了 转换的时候用try-catch捕获异常最后仪器抛出
    def _notation_conversion(self):
        self.music['标记'] = self.music['标记'].apply(self._split_identifier)
        self.music['音符'] = self.music['音符'].apply(self._number_notation_to_key_notation)

    def _split_identifier(self, identifier):
        if identifier:
            return str(identifier).split(",")
            

    def _number_notation_to_key_notation(self, number_notation):
        # 自定义排序使得低音在高音的前面，这样弹奏琶音时才是从低到高
        def sort_key(s):
            if len(s) == 0:
                return 0
            if s[0] == '-':
                return int(s[1])
            elif s[0] == '+':
                return 20 + int(s[1])
            else:
                return 10 + int(s)
        if pd.isnull(number_notation):
            return
        number_notation = number_notation.split(",")
        number_notation = sorted(number_notation, key=sort_key)
        key_notation = []
        for musical_notes in number_notation:
            if musical_notes == "0" or musical_notes == "":
                continue
            key_notation.append(self._dic[musical_notes])
        return key_notation


if __name__ == '__main__':
    music = Music('resource/轻涟.xlsx')
    df = music.music
    print(music.name)
