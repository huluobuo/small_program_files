import turtle
import copy

import os
import sys

# Python解释器工作目录
base_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(base_dir)
# -----------------------------------------------------------------
# 1.基本信息区，放置游戏相关的一些信息
size = 70
'''
0-空   1-大帅哥   2-墙壁   3-大帅哥   4-钻石  5-老8  
'''
level_n = 1
level1 = [[0, 0, 1, 1, 1, 0],
          [0, 0, 1, 3, 1, 1],
          [1, 1, 1, 4, 3, 1],
          [1, 4, 2, 2, 4, 1],
          [1, 2, 2, 4, 3, 1],
          [0, 1, 1, 1, 1, 1]]
level2 = [[0, 1, 1, 1, 1, 1, 3, 1],
          [0, 1, 1, 2, 2, 2, 4, 1],
          [1, 1, 4, 5, 2, 2, 2, 1],
          [1, 3, 4, 2, 2, 2, 2, 1],
          [1, 1, 5, 2, 2, 2, 2, 1],
          [0, 1, 1, 1, 1, 1, 3, 1]]
levels = [level1, level2]
grid = copy.deepcopy(levels[level_n - 1])
width = len(grid[0])
height = len(grid)
origin_x = -(width-1) / 2 * size
origin_y = (height-1) / 2 * size
# 角色初始位置
players = [[1, 3], [4, 1]]
player_x = players[level_n - 1][0]
player_y = players[level_n - 1][1]
# 0: 游戏结束,   1：过关,   2：游戏进行中
result = 2

# ------------------------------------------------------------
# 2.功能模块区，主要放置函数
def draw(pen, img, x, y):
    '''使用画笔pen，前往坐标（x，y），绘制外观img'''
    global origin_x, origin_y, size
    pen.goto(origin_x + x * size, origin_y - y * size)
    pen.shape(img)
    pen.stamp()

def move_up():
    '''角色上移'''
    global player_x, player_y, grid
    # 显示结果后，禁止角色移动
    if result != 2:
        return
    player_y -= 1
    # 移动范围
    if player_y < 0:
        player_y += 1
        return
    elif grid[player_y][player_x] == 1:
        player_y += 1
        return
    # 改变地形，更新地图信息
    change_grid()

def move_down():
    '''角色下移'''
    global player_x, player_y, grid
    # 显示结果后，禁止角色移动
    if result != 2:
        return
    player_y += 1
    # 移动范围
    if player_y >= height:
        player_y -= 1
        return
    elif grid[player_y][player_x] == 1:
        player_y -= 1
        return
    # 改变地形，更新地图信息
    change_grid()

def move_left():
    '''角色左移'''
    global player_x, player_y, grid
    # 显示结果后，禁止角色移动
    if result != 2:
        return
    player_x -= 1
    # 移动范围
    if player_x < 0:
        player_x += 1
        return
    elif grid[player_y][player_x] == 1:
        player_x += 1
        return
    # 改变地形，更新地图信息
    change_grid()

def move_right():
    '''角色右移'''
    global player_x, player_y, grid
    # 显示结果后，禁止角色移动
    if result != 2:
        return
    player_x += 1
    # 移动范围
    if player_x >= width:
        player_x -= 1
        return
    elif grid[player_y][player_x] == 1:
        player_x -= 1
        return
    # 改变地形，更新地图信息
    change_grid()

def change_grid():
    '''改变地形，更新地图信息'''
    global grid, player_x, player_y
    if grid[player_y][player_x] == 2:
        grid[player_y][player_x] = 3
    elif grid[player_y][player_x] == 3:
        grid[player_y][player_x] = 4
    show_result()

def show_result():
    '''现实游戏输赢结果'''
    global result, grid, player_x, player_y
    if grid[player_y][player_x] == 4:
        result = 0
    else:
        for i in grid:
            if 2 in i:
                result = 2
                break
        else:
            result = 1

def next_level():
    '''按下回车进入下一关，或者重置当前关卡'''
    global result, level_n, grid, player_x, player_y, width, height, origin_x, origin_y, size
    if result == 1:
        level_n += 1
    result = 2
    grid = copy.deepcopy(levels[level_n - 1])
    width = len(grid[0])
    height = len(grid)
    origin_x = 0 - size * (width - 1) / 2
    origin_y = 0 + size * (height - 1) / 2
    player_x = players[level_n-1][0]
    player_y = players[level_n-1][1]

def blink():
    global result, level_n, grid, player_x, player_y, width, height, height, origin_x, origin_y, origin_y, size
    if level_n ==1:
        if player_x == 3 and player_y == 2:
            player_x = 4
            player_y = 4
        elif player_x == 4 and player_y == 4:
            player_x = 3
            player_y = 2
# ------------------------------------------------------------
# 3.操作事件区，放置键鼠操作相关的内容
turtle.onkey(move_up, 'Up')
turtle.onkey(move_down, 'Down')
turtle.onkey(move_left, 'Left')
turtle.onkey(move_right, 'Right')
turtle.onkey(next_level, 'Return')
turtle.listen()

# ------------------------------------------------------------
# 4.场景素材区，添加游戏画面相关的素材
grid_shapes = ['空.gif', '大帅哥_71x70.gif', '墙壁.gif', '大帅哥_71x70.gif', '钻石.gif', '老8_52x70.gif']
for i in grid_shapes:
    turtle.addshape(i)
turtle.addshape('大帅哥_71x70.gif')
result_shapes = ['成功.gif', '失败.gif', '空.gif']
for i in result_shapes:
    turtle.addshape(i)

# ------------------------------------------------------------
# 5.画面绘制区，绘制场景用的画笔，绘制场景的代码
p = turtle.Pen()
p.penup()
p.hideturtle()

turtle.tracer(False)
while True:
    p.clear()
    for i in range(width):
        for j in range(height):
            draw(p, grid_shapes[grid[j][i]], i, j)
    draw(p, '大帅哥_71x70.gif', player_x, player_y)
    draw(p, result_shapes[result], (width - 1) / 2, (height - 1) / 2)
    turtle.update()

turtle.done()