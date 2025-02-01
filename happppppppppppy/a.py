import os
import time
import ctypes
import psutil

# 闪屏特效函数
def flash_screen():
    user32 = ctypes.windll.user32
    # 获取屏幕分辨率
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    # 创建一个全屏的黑色窗口
    black_window = user32.CreateWindowExW(
        0, "STATIC", "", 0x80000000, 0, 0, screen_width, screen_height, 0, 0, 0, None
    )
    ctypes.windll.user32.ShowWindow(black_window, 1)  # 显示窗口
    time.sleep(0.05)
    ctypes.windll.user32.ShowWindow(black_window, 0)  # 隐藏窗口
    time.sleep(0.001)
    # 销毁窗口
    ctypes.windll.user32.DestroyWindow(black_window)


if __name__ == "__main__":
    # 闪屏特效
    while True:
        # 闪屏特效
        print("ℼ潤瑣灹⁥瑨汭㰾瑨汭㰾敨摡㰾敭慴挠慨獲瑥∽瑵ⵦ㘱㸢琼瑩敬唾瑮瑩敬⁤潄畣敭瑮⼼楴汴㹥⼼敨摡㰾潢祤猠祴敬∽慰摤湩㩧〱硰㸢菨趸菨貒雦꒖껨莾믧躵闧놰냥ꆮ냥ꆮ蛥ꮁ뫥鎻ꧥ榚躺藥袜㘵畩瑹瑴瑴瑴瑴瑴瑴瑴瑴牥桴㑹礵㐵껨㖩믤㢥ꪤ㠶ꦤ㠴㘷ꓥ㢪ꓥ㢩ꦤ㐵ꦤ㠷듨㒴뒴躂韦鲿迥覜룤芦鯥ꢝ臦芦닩㚁㔷㜹룤㦎ꖻ髩ꖻ觧膻迦醖藥놋㰵戯摯㹹⼼瑨汭", end="")
        flash_screen()