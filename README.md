# 自动弹奏风物之诗琴

## 概述

本项目旨在实现在原神中自动使用风物之诗琴演奏乐曲的功能。项目使用 Excel 文件存储乐曲信息，通过 Python 脚本读取曲谱并在游戏中自动演奏这些乐曲。

## 目录结构

项目主要包含以下目录：

1. **resource**：包含以 Excel 文件存储的乐曲曲谱。
2. **src**：包含项目的源代码。

## 项目文件

### resource 目录

- 该目录下的每个Excel文件对应一首乐曲，文件中包括音高、速度、节奏和歌词等信息。目前已改编的乐曲包括：
  - **轻涟**
  - **天空之城**

### src 目录

- **music.py**：定义了 Music 类。
    - **Music 类**：读取并转换存储在 Excel 文件中的乐曲信息。
      - 读取并校验乐曲格式，当某行乐谱格式有误时，将给出友好的报错信息。
      - 将简谱转换为原神的键盘谱。

- **player.py**：定义了 Player 类。
  - **Player 类**：实现自动演奏诗琴的功能。
    - 使用 pyautogui 模拟键盘输入。
    - 通过时间戳控制节奏。
    - 支持琶音、变速、同步显示歌词和角色移动等功能。

- **main.py**：基于 Player 类实现了一些额外功能。
  - 自动启动原神游戏。
  - 启动守护线程监听 esc 键输入以手动中止演奏。

## 使用方法

1. **设置环境**：
    - 确保已安装 Python 和所需的依赖包，基于 player.py 演奏需要安装：
      - `pandas`
      - `pyautogui`
    - 使用 main.py 演奏需要额外安装：
      - `pynput` 

2. **准备乐谱**：
    - 将乐谱文件放置在 resource 目录中，确保文件格式为 .xlsx 或 .xls 。

3. **修改参数**：
   - 修改 player.py 或 mian.py 代码 Music('music_path') 中的 music_path 为你的乐谱位置
   - 如果使用 main.py 实现自动启动原神的功能，请将代码中 start_Genshin() 函数中的 Genshin_path 修改为你的原神程序位置

4. **运行脚本**：
   - 使用管理员身份执行 main.py 脚本启动程序：
     ```sh
     python src/main.py
     ```
   - 或使用管理员身份执行 player.py 脚本实现基础的演奏功能：
     ```sh
     python src/player.py
     ```

## 贡献

欢迎大家提供更多的乐曲曲谱。请遵循现有的曲谱格式以确保兼容性。可以fork本项目并提交pull request。

## 致谢

特别感谢乐曲曲谱的原作作者。 resource 目录中的每个乐谱文件都包含有关原作的信息。
  - 轻涟
    - 原风物之诗琴谱：B站[@指尖灬旋律丿](https://space.bilibili.com/76052941?spm_id_from=333.976.0.0)
    - 原谱链接：https://www.bilibili.com/read/cv27651860/?spm_id_from=333.999.collection.opus.click
    - 改编：[JianX0917](https://github.com/JianX0917)
  - 天空之城
    - 原风物之诗琴谱：[人人钢琴网](https://www.everyonepiano.cn/)
    - 原谱链接：https://www.everyonepiano.cn/Piano-15237.html#
    - 改编：[JianX0917](https://github.com/JianX0917)

## 未来计划

- 添加更多的乐谱。
- 改进程序的功能和性能。

---

感谢您使用本项目。希望它能提升您在游戏中的音乐体验。祝您演奏愉快！

---

**联系方式**：
如有任何问题或建议，请在GitHub仓库中打开issue。

## 许可

本项目使用MIT许可证。请参阅 [LICENSE](LICENSE.txt) 文件了解更多详情。
