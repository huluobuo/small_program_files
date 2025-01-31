import tkinter as tk
from tkinter import ttk
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers   # ？？？
import tensorflow as tf
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.font_manager as fm



class TextRecognizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("手写字母识别")
        
        # 设置中文字体
        self.font_path = './fonts/SimHei.ttf'
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置画布大小
        self.width = 400
        self.height = 400
        self.drawing = False
        self.last_x = None
        self.last_y = None
        
        # 创建模型
        self.model = self._create_model()
        
        self._init_ui()
        
    def _init_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建画布
        self.canvas = tk.Canvas(main_frame, width=self.width, height=self.height, 
                              bg='white', cursor='cross')
        self.canvas.grid(row=0, column=0, rowspan=2)
        
        # 创建结果显示区域
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=0, column=1, padx=10)
        
        # 使用SimHei字体
        label = ttk.Label(result_frame, text="实时识别结果")
        label.pack()
        try:
            label.configure(font=(self.font_path, 14, 'bold'))
        except:
            label.configure(font=('SimHei', 14, 'bold'))
        
        # 创建matplotlib图形
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # 设置matplotlib的字体
        font_prop = fm.FontProperties(fname=self.font_path)
        self.ax.set_title('识别概率分布', fontproperties=font_prop)
        self.ax.set_ylabel('概率 (%)', fontproperties=font_prop)
        
        self.canvas_plt = FigureCanvasTkAgg(self.fig, master=result_frame)
        self.canvas_plt.draw()
        self.canvas_plt.get_tk_widget().pack(pady=5)
        
        # 初始化条形图
        self.bars = None
        
        # 创建样式
        style = ttk.Style()
        style.configure('Custom.TButton', font=('SimHei', 10))

        # 使用自定义样式的按钮
        clear_button = ttk.Button(result_frame, text="清除", command=self.clear_canvas, style='Custom.TButton')
        clear_button.pack(pady=5)
        
        # 绑定鼠标事件
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        
        # 创建画布背景图像
        self.image = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.image)
        
        # 添加延迟识别的变量
        self.recognize_after_id = None
        
    def _create_model(self):
        # 创建简单的CNN模型
        model = keras.Sequential([
            layers.Input(shape=(28, 28, 1)),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dense(52, activation="softmax")
        ])
        
        model.compile(optimizer="adam",
                     loss="sparse_categorical_crossentropy",
                     metrics=["accuracy"])
        return model
    
    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
    
    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            if self.last_x and self.last_y:
                self.canvas.create_line(self.last_x, self.last_y, x, y,
                                     width=15, fill='black', capstyle=tk.ROUND,
                                     smooth=True)
                self.draw.line([self.last_x, self.last_y, x, y],
                             fill='black', width=15)
            self.last_x = x
            self.last_y = y
            
            # 取消之前的延迟识别
            if self.recognize_after_id:
                self.root.after_cancel(self.recognize_after_id)
            
            # 设置新的延迟识别（100毫秒后执行）
            self.recognize_after_id = self.root.after(100, self.recognize)
    
    def stop_drawing(self, event):
        self.drawing = False
        self.last_x = None
        self.last_y = None
        self.recognize()  # 停止绘制时立即进行一次识别
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.image)
        # 清除图表
        self.ax.clear()
        font_prop = fm.FontProperties(fname=self.font_path)
        self.ax.set_title('识别概率分布', fontproperties=font_prop)
        self.ax.set_ylabel('概率 (%)', fontproperties=font_prop)
        self.canvas_plt.draw()
    
    def _preprocess_image(self):
        # 调整图像大小并转换为灰度
        img_array = np.array(self.image.convert('L').resize((28, 28)))
        # 归一化
        normalized = img_array / 255.0
        return normalized
    
    def recognize(self):
        # 预处理图像
        image = self._preprocess_image()
        
        # 进行预测
        predictions = self.model.predict(np.expand_dims(image, axis=(0, -1)), verbose=0)[0]
        
        # 获取所有字母的概率
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        probabilities = [(letter, prob * 100) for letter, prob in zip(letters, predictions)]
        probabilities.sort(key=lambda x: x[1], reverse=True)
        
        # 更新图表
        self.ax.clear()
        top_n = 5  # 显示前5个结果
        
        letters_show = [p[0] for p in probabilities[:top_n]]
        probs_show = [p[1] for p in probabilities[:top_n]]
        
        # 创建条形图
        bars = self.ax.bar(letters_show, probs_show)
        
        # 在条形上方显示具体数值
        font_prop = fm.FontProperties(fname=self.font_path)
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom',
                        fontproperties=font_prop)
        
        self.ax.set_title('Top 5 识别结果', fontproperties=font_prop)
        self.ax.set_ylabel('概率 (%)', fontproperties=font_prop)
        self.ax.set_ylim(0, 100)  # 设置y轴范围为0-100%
        
        # 更新图表
        self.canvas_plt.draw()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    recognizer = TextRecognizer()
    recognizer.run()
