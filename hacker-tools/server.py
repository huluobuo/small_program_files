import socket
import threading




def handle_client(conn, addr):
    print(f"客户端已连接: {addr}")
    try:
        while True:
            # 发送命令给客户端
            command = input("请输入要发送给客户端的命令: ")  # 从控制台输入命令
            conn.send(command.encode('utf-8'))  # 发送命令
            if command.lower() in ['exit', 'quit']:
                break  # 退出循环
            data = conn.recv(1024)  # 接收客户端的响应
            print(f"来自 {addr} 的响应: {data.decode('utf-8', errors='replace')}")  # 使用 'replace' 处理无效字节
    except Exception as e:
        print(f"处理客户端 {addr} 时出现异常: {e}")
    finally:
        conn.close()
        print(f"与 {addr} 的连接已关闭")


def main():
    host = '192.168.0.110'
    port = 8000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # 允许多个连接
    print(f"服务端正在 {host}:{port} 监听...")
    while True:
        conn, addr = server.accept()
        print(f"客户端 {addr} 已连接。")
        # 为每个客户端连接创建一个新线程
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == '__main__':
    main()