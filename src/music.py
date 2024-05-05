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
        self.name = file_path.split('/')[-1].split('.')[0].replace('_', ' ')
        # 设置速度
        if self.music.empty or self.music.iloc[0, 0] != 's':
            raise ValueError("乐谱格式有误")
        if self.music.iloc[0, 2] <= 0:
            raise ValueError("乐谱速度有误")
        self.speed = self.music.iloc[0, 2]
        self.music = self.music.drop(0)
        # 简谱转换至键盘谱
        self._notation_conversion()
        print("乐谱准备完成")

    def _notation_conversion(self):
        self.music['音符'] = self.music['音符'].apply(self._number_notation_to_key_notation)

    def _number_notation_to_key_notation(self, number_notation):
        if pd.isnull(number_notation):
            return
        number_notation = number_notation.split(",")
        key_notation = []
        for musical_notes in number_notation:
            key_notation.append(self._dic[musical_notes])
        return key_notation


if __name__ == '__main__':
    music = Music('resource/轻涟.xlsx')
    df = music.music
    print(music.name)
