from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageDraw
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

# 加载MNIST数据集
print("加载MNIST数据集...")
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 数据预处理
print("数据预处理...")
x_train = x_train / 255.0
x_test = x_test / 255.0

# 构建神经网络模型
print("构建神经网络模型...")
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),  # 输入层，将28x28的图像展平
    keras.layers.Dense(128, activation='relu'),   # 隐藏层，128个神经元
    keras.layers.Dense(10, activation='softmax')  # 输出层，10个数字的概率分布
])


# 这个取消注释就行，但没必要

## 编译模型
#print("编译模型...")
#model.compile(optimizer='adam',
#              loss='sparse_categorical_crossentropy',
#              metrics=['accuracy'])

## 训练模型
#print("训练模型...")
#model.fit(x_train, y_train, epochs=5)

## 评估模型
#print("评估模型...")
#test_loss, test_accuracy = model.evaluate(x_test, y_test)
#print(f"\n测试准确率: {test_accuracy:.4f}")

# 创建绘图界面类
class DrawingApp:
    def __init__(self, model):
        self.root = tk.Tk()
        self.root.title("手写数字识别")
        
        # 设置中文字体
        self.chinese_font = FontProperties(fname='./fonts/SimHei.ttf')
        plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 左侧绘图区域
        draw_frame = ttk.Frame(main_frame)
        draw_frame.grid(row=0, column=0, padx=10)
        
        # 创建画布
        self.canvas = tk.Canvas(draw_frame, width=280, height=280, bg='white', 
                              relief='ridge', bd=2)
        self.canvas.grid(row=0, column=0, pady=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(draw_frame)
        btn_frame.grid(row=1, column=0, pady=5)
        
        clear_button = ttk.Button(btn_frame, text="清除", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 添加保存和加载模型按钮
        save_button = ttk.Button(btn_frame, text="保存模型", command=self.save_model)
        save_button.pack(side=tk.LEFT, padx=5)
        
        load_button = ttk.Button(btn_frame, text="加载模型", command=self.load_model)
        load_button.pack(side=tk.LEFT, padx=5)
        
        # 右侧概率显示区域
        prob_frame = ttk.Frame(main_frame)
        prob_frame.grid(row=0, column=1, padx=10)
        
        # 使用Matplotlib创建概率条形图
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas_prob = FigureCanvasTkAgg(self.fig, master=prob_frame)
        self.canvas_prob.get_tk_widget().pack()
        
        # 初始化概率图
        self.bars = self.ax.bar(range(10), np.zeros(10))
        self.ax.set_ylim(0, 1)
        self.ax.set_title('数字概率分布', fontproperties=self.chinese_font, fontsize=12)
        self.ax.set_xlabel('数字', fontproperties=self.chinese_font, fontsize=10)
        self.ax.set_ylabel('概率', fontproperties=self.chinese_font, fontsize=10)
        # 设置x轴刻度
        self.ax.set_xticks(range(10))
        self.ax.set_xticklabels(range(10))
        
        # 绘图相关变量
        self.image = Image.new('L', (280, 280), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.last_x = None
        self.last_y = None
        self.model = model
        
        # 绑定鼠标事件
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset_coordinates)
        self.canvas.bind('<B1-Motion>', lambda e: (self.paint(e), self.predict_digit()))
        
        # 设置样式
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TFrame', background='#f0f0f0')
        
        self.root.mainloop()
    
    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x and self.last_y:
            # 在画布上绘制
            self.canvas.create_line((self.last_x, self.last_y, x, y), 
                                  fill='black', width=15, 
                                  capstyle=tk.ROUND, smooth=True)
            # 在图像上绘制
            self.draw.line([self.last_x, self.last_y, x, y], 
                          fill='black', width=15)
        self.last_x = x
        self.last_y = y
    
    def reset_coordinates(self, event):
        self.last_x = None
        self.last_y = None
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new('L', (280, 280), 'white')
        self.draw = ImageDraw.Draw(self.image)
        # 清空概率图
        self.ax.clear()
        self.ax.set_ylim(0, 1)
        self.ax.set_title('数字概率分布', fontproperties=self.chinese_font, fontsize=12)
        self.ax.set_xlabel('数字', fontproperties=self.chinese_font, fontsize=10)
        self.ax.set_ylabel('概率', fontproperties=self.chinese_font, fontsize=10)
        self.bars = self.ax.bar(range(10), np.zeros(10))
        # 设置x轴刻度
        self.ax.set_xticks(range(10))
        self.ax.set_xticklabels(range(10))
        
        self.canvas_prob.draw()
    
    def predict_digit(self):
        # 调整图像大小为28x28
        img = self.image.resize((28, 28))
        # 转换为numpy数组并反转颜色（因为MNIST数据集是黑底白字）
        img_array = np.array(img)
        img_array = 255 - img_array  # 反转颜色
        # 归一化
        img_array = img_array / 255.0
        # 添加批次维度
        img_array = img_array.reshape(1, 28, 28)
        # 预测
        prediction = self.model.predict(img_array, verbose=0)[0]
        
        # 更新概率条形图
        self.ax.clear()  # 清除之前的图形
        self.ax.set_ylim(0, 1)
        self.ax.set_title('数字概率分布', fontproperties=self.chinese_font, fontsize=12)
        self.ax.set_xlabel('数字', fontproperties=self.chinese_font, fontsize=10)
        self.ax.set_ylabel('概率', fontproperties=self.chinese_font, fontsize=10)
        
        # 重新绘制条形图
        self.bars = self.ax.bar(range(10), prediction)
        
        # 设置x轴刻度
        self.ax.set_xticks(range(10))
        self.ax.set_xticklabels(range(10))
        
        # 添加数值标签
        for bar in self.bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height*100:.0f}%',  # 转换为百分比并去除小数
                        ha='center', va='bottom')
        
        self.canvas_prob.draw()

    def save_model(self):
        """保存模型到文件"""
        file_path = filedialog.asksaveasfilename(defaultextension=".h5", 
                                                   filetypes=[("H5 Files", "*.h5"), ("All Files", "*.*")])
        if file_path:  # 确保用户选择了文件
            try:
                self.model.save(file_path)
                tk.messagebox.showinfo("成功", f"模型已保存到 {file_path}")
            except Exception as e:
                tk.messagebox.showerror("错误", f"保存模型时出错：{str(e)}")
    
    def load_model(self):
        """从文件加载模型"""
        file_path = filedialog.askopenfilename(filetypes=[("H5 Files", "*.h5"), ("All Files", "*.*")])
        if file_path:  # 确保用户选择了文件
            try:
                self.model = keras.models.load_model(file_path)
                tk.messagebox.showinfo("成功", f"模型已从 {file_path} 加载")
            except Exception as e:
                tk.messagebox.showerror("错误", f"加载模型时出错：{str(e)}")

# 训练完模型后启动绘图界面
def main():
    # 加载MNIST数据集并训练模型
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    
    # 数据预处理
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    
    # 构建神经网络模型
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    
    # 编译模型
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # 训练模型
    model.fit(x_train, y_train, epochs=5)
    
    # 启动绘图界面
    app = DrawingApp(model)

if __name__ == "__main__":
    main()