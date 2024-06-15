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
        self.excel_index = 2  # 记录当前处理excel中的第几行，便于错误处理，第一行不读取，索引从2开始
        # 设置速度
        if self.music.empty or self.music.iloc[0, 0] != 's':
            raise MusicException("乐谱格式有误")
        if self.music.iloc[0, 2] <= 0:
            raise MusicException("乐谱速度需大于0")
        self.speed = self.music.iloc[0, 2]
        self.music = self.music.drop(0)
        self.excel_index += 1
        # 从Excel中读取乐名，若Excel中未设置乐名，则以Excel文件名作为默认乐名
        self.name = self._get_name(file_path)
        # 简谱转换至键盘谱
        try:
            self._check()  # 合法性检验
            self._transfer()  # 数据转换
            print("乐谱准备完成")
        except MusicException as e:
            print(e)  # 格式有误，打印错误信息

    # 解析乐曲名
    def _get_name(self, file_path):
        name = None
        # 优先从Excel中读取乐名
        if self.music.empty or self.music.iloc[0, 0] == 'n':
            name = self.music.iloc[0, 1]
            self.music = self.music.drop(1)
            self.excel_index += 1
        # 无法从Excel中读取到乐名，将Execl文件名作为默认乐名
        if name is None:
            name = file_path.split('/')[-1].split('.')[0].replace('_', ' ')
        return name

    # 数据合法性检验
    def _check(self):
        exception_info = []
        for index, row in self.music.iterrows():
            try:
                self._split_identifier(row['标记'])
            except:
                exception_info.append("\n\t第{}行'标记'数据有误".format(self.excel_index))
            try:
                self._number_notation_to_key_notation(row['音符'])
            except:
                exception_info.append("\n\t第{}行'音符'数据有误".format(self.excel_index))
            try:
                self._check_interval(row['间隔'])
            except:
                exception_info.append("\n\t第{}行'停顿时长'数据有误".format(self.excel_index))
            self.excel_index += 1
        if exception_info:
            raise MusicException("读取失败，对照下列信息请检查Excel中数据格式:" + "".join(exception_info))

    # 乐谱格式转换
    def _transfer(self):
        self.music['标记'] = self.music['标记'].apply(self._split_identifier)
        self.music['音符'] = self.music['音符'].apply(self._number_notation_to_key_notation)

    # 定义第一列"标记"的分割规则
    def _split_identifier(self, identifier):
        if identifier:
            return str(identifier).split(",")

    # 定义第二列"音符"的转换规则
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

        try:
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
        except:
            raise MusicException("转换乐谱音符时出现错误")

    # 定义第三列"间隔"的检查规则
    def _check_interval(self, interval):
        if interval <= 0:
            raise MusicException("音符间隔需大于0")


# 异常类型
class MusicException(Exception):
    def __init__(self, message):
        super().__init__(message)


if __name__ == '__main__':
    music = Music('resource/test.xlsx')
    df = music.music
    # print(music.name)
