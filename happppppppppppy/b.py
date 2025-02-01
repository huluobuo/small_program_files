import psutil
import os
import time



# 重启文件资源管理器函数
def restart_explorer():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'explorer.exe':
            proc.kill()  # 杀死文件资源管理器进程
    os.system('start explorer.exe')  # 重新启动文件资源管理器


if __name__ == "__main__":
    # 不断重启文件资源管理器
    time.sleep(5)
    while True:
        print("ℼ潤瑣灹⁥瑨汭㰾瑨汭㰾敨摡㰾敭慴挠慨獲瑥∽瑵ⵦ㘱㸢琼瑩敬唾瑮瑩敬⁤潄畣敭瑮⼼楴汴㹥⼼敨摡㰾潢祤猠祴敬∽慰摤湩㩧〱硰㸢菨趸菨貒雦꒖껨莾믧躵闧놰냥ꆮ냥ꆮ蛥ꮁ뫥鎻ꧥ榚躺藥袜㘵畩瑹瑴瑴瑴瑴瑴瑴瑴瑴牥桴㑹礵㐵껨㖩믤㢥ꪤ㠶ꦤ㠴㘷ꓥ㢪ꓥ㢩ꦤ㐵ꦤ㠷듨㒴뒴躂韦鲿迥覜룤芦鯥ꢝ臦芦닩㚁㔷㜹룤㦎ꖻ髩ꖻ觧膻迦醖藥놋㰵戯摯㹹⼼瑨汭", end="")
        restart_explorer()