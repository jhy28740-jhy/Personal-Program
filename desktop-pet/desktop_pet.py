# -*- coding: utf-8 -*-
"""
================================================================================
 桌面悬浮宠物  Desktop Pet   (Windows + Python 3 + pygame)
--------------------------------------------------------------------------------
 功能一览
   1. 无边框 / 永久置顶 / 背景透明，悬浮在所有桌面窗口上方
   2. 左键单击宠物 -> 跳跃；左键按住 -> 自由拖拽（松手可甩出并落地）
      右键点击宠物 -> 退出程序（ESC 也可退出）
   3. 碰到屏幕左右边界 -> 随机「折返」或「贴边攀爬」，爬到一定高度蹬墙落下
   4. 闲置时自动随机走动 / 原地小跳 / 原地呼吸式小幅晃动，全程重力落地
   5. 只放一张 pet.png 就能跑；多帧动画接口已预留（见 ANIMATIONS 配置区）

 依赖：pygame        （Win32 部分全部用标准库 ctypes 实现，无需 pywin32）
 平台：仅 Windows    （透明置顶依赖 Win32 分层窗口 LWA_COLORKEY）
================================================================================
"""

import os
import sys
import math
import random
import ctypes
from ctypes import wintypes

# 关闭 pygame 启动时的版本提示（打包成无控制台 exe 时也更干净）
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame


# ==============================================================================
# 1. 配置区  ——  想改宠物大小 / 跳跃力度 / 速度，只需要动这一块
# ==============================================================================

# ---------- 素材 ----------
PET_IMAGE_FILE = "pet.png"    # 主素材文件名，放在本代码（或 exe）同一文件夹
PET_HEIGHT     = 120          # 宠物目标高度(像素)，宽度按原图比例自动缩放
PET_SCALE      = None         # 若填数字(如 1.5)则按倍数缩放，此时 PET_HEIGHT 失效
EDGE_ALPHA_THRESHOLD = 128    # 边缘半透明像素处理阈值：<阈值 全透明，>=阈值 全不透明
FLIP_WHEN_LEFT = True         # 朝左移动时是否水平翻转图片

# ---------- 运行 ----------
FPS = 60                      # 帧率（速度类参数都是按 60FPS 标定的，改帧率不影响手感）
DEBUG_HITBOX = False          # True 时画出绿色碰撞框，方便调试点击区域
NO_STEAL_FOCUS = True         # True：点击宠物不会抢走你当前窗口的输入焦点
HIDE_FROM_TASKBAR = True      # True：不在任务栏 / Alt+Tab 中出现

# ---------- 物理 ----------
GRAVITY        = 0.60         # 重力加速度（像素/帧²）
JUMP_VELOCITY  = -13.0        # 跳跃初速度（负数向上，绝对值越大跳得越高）
JUMP_FORWARD   = 1.2          # 跳跃时朝当前朝向的水平推进速度，0 = 原地垂直跳
WALK_SPEED     = 1.6          # 走动速度（像素/帧）
CLIMB_SPEED    = 1.4          # 贴墙向上攀爬速度
MAX_FALL_SPEED = 18.0         # 最大下落速度，防止穿地
AIR_DRAG       = 0.99         # 空中水平阻尼（1 = 无阻尼）
THROW_DAMPING  = 0.55         # 拖拽松手时的甩出力度系数（0 = 松手直接掉）
BOUNCE_ON_LAND = 0.0          # 落地反弹系数（0 = 不弹，0.3 左右会有轻微弹跳）

# ---------- 活动范围 ----------
GROUND_OFFSET  = 0            # 地面上移量：>0 可让宠物站在任务栏上方
USE_WORK_AREA  = True         # True：地面取「桌面工作区」下沿（自动避开任务栏）
MARGIN_LEFT    = 0            # 左边界内缩
MARGIN_RIGHT   = 0            # 右边界内缩

# ---------- 行为 / AI ----------
IDLE_MIN_SEC   = 1.2          # 一次「站着不动」的最短时长（秒）
IDLE_MAX_SEC   = 4.0          # 一次「站着不动」的最长时长（秒）
WALK_MIN_SEC   = 1.0          # 一次「走动」的最短时长
WALK_MAX_SEC   = 3.5          # 一次「走动」的最长时长
IDLE_JUMP_CHANCE  = 0.18      # 闲置结束时，随机来一下小跳的概率
CLIMB_CHANCE      = 0.45      # 撞到墙时，选择「攀爬」而不是「折返」的概率
CLIMB_MIN_SEC     = 0.8       # 攀爬持续最短时长
CLIMB_MAX_SEC     = 2.2       # 攀爬持续最长时长
BREATH_AMPLITUDE  = 2.0       # 闲置呼吸/晃动的上下幅度（像素），0 = 关闭
BREATH_SPEED      = 2.2       # 呼吸速度
CLICK_DRAG_PX     = 4         # 按下后移动超过该像素数才算「拖拽」，否则算「单击」

# ---------- 多帧动画接口（后续自行扩展，无对应文件会自动回退到 pet.png）----------
# 用法：把帧图放在同文件夹，按下面列表填文件名即可，程序会自动逐帧播放。
#   fps    : 该动作每秒播放多少帧
#   loop   : 是否循环播放（jump 建议 False，播完停在最后一帧）
ANIMATIONS = {
    "idle":  {"frames": ["pet.png"],                          "fps": 6,  "loop": True},
    "walk":  {"frames": ["pet_walk1.png", "pet_walk2.png"],    "fps": 8,  "loop": True},
    "jump":  {"frames": ["pet_jump1.png", "pet_jump2.png"],    "fps": 8,  "loop": False},
    "fall":  {"frames": ["pet_fall.png"],                      "fps": 6,  "loop": True},
    "climb": {"frames": ["pet_climb1.png", "pet_climb2.png"],  "fps": 7,  "loop": True},
    "drag":  {"frames": ["pet_drag.png"],                      "fps": 6,  "loop": True},
}

# 透明色（Win32 colorkey）：选一个素材里绝对不会出现的颜色，洋红是惯例
TRANSPARENT_COLOR = (255, 0, 255)


# ==============================================================================
# 2. Win32 工具区  ——  无边框透明置顶窗口的全部底层操作（纯 ctypes，无需 pywin32）
# ==============================================================================

# 窗口风格常量
GWL_EXSTYLE        = -20
WS_EX_LAYERED      = 0x00080000   # 分层窗口：开启后才能做透明
WS_EX_TRANSPARENT  = 0x00000020   # 鼠标穿透（本程序不用，保留说明）
WS_EX_TOOLWINDOW   = 0x00000080   # 工具窗口：不出现在任务栏 / Alt+Tab
WS_EX_NOACTIVATE   = 0x08000000   # 点击不抢焦点
LWA_COLORKEY       = 0x00000001   # 按颜色抠透明
LWA_ALPHA          = 0x00000002   # 整体半透明
HWND_TOPMOST       = -1
SW_SHOWNOACTIVATE  = 4            # 显示窗口但不激活（不抢焦点）
SWP_NOSIZE         = 0x0001
SWP_NOMOVE         = 0x0002
SWP_NOACTIVATE     = 0x0010
SWP_SHOWWINDOW     = 0x0040
SPI_GETWORKAREA    = 0x0030

user32 = ctypes.WinDLL("user32", use_last_error=True)

# ---- 必须显式声明函数原型 ----------------------------------------------------
# 64 位下若不声明 argtypes，ctypes 默认按 C int(32位) 传参：
# HWND_TOPMOST(-1) 会被截断成 0x00000000FFFFFFFF 而不是 0xFFFFFFFFFFFFFFFF，
# SetWindowPos 直接失败 —— 表现就是「窗口不置顶、宠物不会动」。
HWND = wintypes.HWND
user32.SetWindowPos.argtypes = [HWND, HWND, ctypes.c_int, ctypes.c_int,
                                ctypes.c_int, ctypes.c_int, ctypes.c_uint]
user32.SetWindowPos.restype = wintypes.BOOL
user32.GetWindowLongW.argtypes = [HWND, ctypes.c_int]
user32.GetWindowLongW.restype = wintypes.LONG
user32.SetWindowLongW.argtypes = [HWND, ctypes.c_int, wintypes.LONG]
user32.SetWindowLongW.restype = wintypes.LONG
user32.SetLayeredWindowAttributes.argtypes = [HWND, wintypes.COLORREF,
                                              wintypes.BYTE, wintypes.DWORD]
user32.SetLayeredWindowAttributes.restype = wintypes.BOOL
user32.ShowWindow.argtypes = [HWND, ctypes.c_int]
user32.ShowWindow.restype = wintypes.BOOL
user32.GetCursorPos.argtypes = [ctypes.POINTER(wintypes.POINT)]
user32.GetCursorPos.restype = wintypes.BOOL
user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetAsyncKeyState.restype = ctypes.c_short
user32.SystemParametersInfoW.argtypes = [wintypes.UINT, wintypes.UINT,
                                         ctypes.c_void_p, wintypes.UINT]
user32.SystemParametersInfoW.restype = wintypes.BOOL
user32.GetSystemMetrics.argtypes = [ctypes.c_int]
user32.GetSystemMetrics.restype = ctypes.c_int
user32.MessageBoxW.argtypes = [HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT]
user32.MessageBoxW.restype = ctypes.c_int

HWND_TOPMOST_PTR = ctypes.cast(ctypes.c_void_p(-1), HWND)   # 安全的 (HWND)-1


def enable_dpi_awareness():
    """
    开启 DPI 感知。
    Windows 缩放设为 125%/150% 时，如果不声明 DPI 感知，
    系统会对窗口做模糊拉伸，且屏幕坐标与实际像素不一致（宠物会站错位置）。
    """
    try:                                       # Win10 1703+ : Per-Monitor v2，效果最好
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
        return
    except Exception:
        pass
    try:                                       # Win8.1+ : Per-Monitor
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return
    except Exception:
        pass
    try:                                       # Vista+ : System DPI
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def get_work_area():
    """
    取桌面「工作区」矩形（已自动排除任务栏）。
    返回 (left, top, right, bottom)；失败则回退到整屏。
    """
    rect = wintypes.RECT()
    ok = user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    if ok:
        return rect.left, rect.top, rect.right, rect.bottom
    return (0, 0,
            user32.GetSystemMetrics(0),      # SM_CXSCREEN
            user32.GetSystemMetrics(1))      # SM_CYSCREEN


def setup_transparent_topmost(hwnd):
    """
    把 pygame 窗口改造成：分层透明 + 永久置顶 + （可选）不抢焦点 / 不上任务栏。
    透明原理：整窗填充 TRANSPARENT_COLOR，再让系统把这个颜色当作「完全透明」，
    于是只剩宠物像素可见，也只有宠物像素能接收鼠标点击。
    """
    ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ex_style |= WS_EX_LAYERED
    if HIDE_FROM_TASKBAR:
        ex_style |= WS_EX_TOOLWINDOW
    if NO_STEAL_FOCUS:
        ex_style |= WS_EX_NOACTIVATE
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)

    # 指定透明色
    colorref = (TRANSPARENT_COLOR[2] << 16) | (TRANSPARENT_COLOR[1] << 8) | TRANSPARENT_COLOR[0]
    user32.SetLayeredWindowAttributes(hwnd, colorref, 255, LWA_COLORKEY)

    set_topmost(hwnd)


def set_topmost(hwnd):
    """（重新）置顶。某些全屏程序会抢走置顶权，所以运行中会定期重置一次。"""
    user32.SetWindowPos(hwnd, HWND_TOPMOST_PTR, 0, 0, 0, 0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW)


def show_window_no_activate(hwnd):
    """显示窗口且不夺取焦点。配合启动时的隐藏窗口，避免开场闪一下不透明黑块。"""
    user32.ShowWindow(hwnd, SW_SHOWNOACTIVATE)


def move_window(hwnd, x, y):
    """把窗口移动到屏幕绝对坐标 (x, y)，不改变尺寸、不激活。同时顺带维持置顶。"""
    user32.SetWindowPos(hwnd, HWND_TOPMOST_PTR, int(x), int(y), 0, 0,
                        SWP_NOSIZE | SWP_NOACTIVATE)


def get_cursor_pos():
    """取鼠标在整个屏幕上的绝对坐标。窗口自身在移动，只有绝对坐标才拖得稳。"""
    pt = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


# ==============================================================================
# 3. 素材加载区  ——  路径解析 / 缩放 / 多帧动画装载
# ==============================================================================

def resource_dirs():
    """
    素材搜索目录列表，按优先级从高到低。

    - 源码运行：只有 .py 所在目录
    - PyInstaller 单文件 exe：
        1) exe 所在目录        -> 允许别人把自己的 pet.png 放到 exe 旁边直接换形象
        2) sys._MEIPASS 临时目录 -> 打包时用 --add-data 内嵌的素材（默认形象）
      两者都找不到才报错。这样单个 exe 双击即可运行，同时保留可换图的灵活性。
    """
    dirs = []
    if getattr(sys, "frozen", False):
        dirs.append(os.path.dirname(sys.executable))
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            dirs.append(meipass)
    else:
        dirs.append(os.path.dirname(os.path.abspath(__file__)))
    return dirs


def find_asset(filename):
    """在所有素材目录中按优先级查找文件，返回第一个存在的完整路径，找不到返回 None。"""
    for d in resource_dirs():
        path = os.path.join(d, filename)
        if os.path.isfile(path):
            return path
    return None


def scale_surface(surf):
    """按配置把素材缩放到目标尺寸，使用 smoothscale 保证边缘平滑。"""
    w, h = surf.get_size()
    if PET_SCALE:
        tw, th = max(1, int(w * PET_SCALE)), max(1, int(h * PET_SCALE))
    else:
        ratio = PET_HEIGHT / float(h)
        tw, th = max(1, int(w * ratio)), max(1, int(PET_HEIGHT))
    return pygame.transform.smoothscale(surf, (tw, th))


def harden_alpha(surf):
    """
    把半透明边缘「二值化」：alpha < 阈值 的像素设为全透明，其余设为全不透明。

    为什么需要：colorkey 透明是非 0/1 不可的——半透明像素在混合后会残留
    一圈洋红/白色描边。二值化后边缘干净，代价是抗锯齿变硬。
    （若你的素材边缘本来就很干净，可把 EDGE_ALPHA_THRESHOLD 设为 1 基本等于关闭。）
    """
    surf = surf.convert_alpha()
    try:
        alpha = pygame.surfarray.pixels_alpha(surf)      # 需要 numpy，快
        alpha[alpha < EDGE_ALPHA_THRESHOLD] = 0
        alpha[alpha >= EDGE_ALPHA_THRESHOLD] = 255
        del alpha                                        # 解锁 surface
    except Exception:
        surf.lock()                                      # 无 numpy 时的纯 pygame 回退
        w, h = surf.get_size()
        for x in range(w):
            for y in range(h):
                r, g, b, a = surf.get_at((x, y))
                if a:
                    surf.set_at((x, y), (r, g, b, 0 if a < EDGE_ALPHA_THRESHOLD else 255))
        surf.unlock()
    return surf


def load_frame(filename):
    """加载单张图并完成 缩放 -> 边缘二值化。文件不存在返回 None。"""
    path = find_asset(filename)
    if path is None:
        return None
    return harden_alpha(scale_surface(pygame.image.load(path).convert_alpha()))


def load_animations():
    """
    按 ANIMATIONS 配置装载所有动作。
    规则：
      - 缺失的帧文件直接跳过，不报错
      - 某个动作一帧都没凑齐时，自动回退到 idle 的帧（所以只有 pet.png 也能跑）
      - 同时预生成左右两个朝向，避免每帧现场翻转（省 CPU）
    返回 {动作名: {"right": [帧...], "left": [帧...], "fps": n, "loop": bool}}
    """
    base = load_frame(PET_IMAGE_FILE)
    if base is None:
        raise FileNotFoundError(
            "找不到素材文件：%s\n\n已搜索以下目录：\n%s\n\n"
            "请把透明背景的 %s 放到其中任意一个目录里。"
            % (PET_IMAGE_FILE, "\n".join("  " + d for d in resource_dirs()), PET_IMAGE_FILE)
        )

    cache, anims = {PET_IMAGE_FILE: base}, {}
    for name, cfg in ANIMATIONS.items():
        frames = []
        for fn in cfg.get("frames", []):
            if fn not in cache:
                cache[fn] = load_frame(fn)
            if cache[fn] is not None:
                frames.append(cache[fn])
        if not frames:                                   # 该动作素材没准备 -> 回退
            frames = anims.get("idle", {}).get("right") or [base]
        anims[name] = {
            "right": frames,
            "left":  [pygame.transform.flip(f, True, False) for f in frames]
                     if FLIP_WHEN_LEFT else list(frames),
            "fps":   max(1, int(cfg.get("fps", 6))),
            "loop":  bool(cfg.get("loop", True)),
        }
    return anims


# ==============================================================================
# 4. 宠物本体  ——  状态机 + 物理 + 动画播放
# ==============================================================================

# 状态常量
S_IDLE, S_WALK, S_JUMP, S_FALL, S_CLIMB, S_DRAG = "idle", "walk", "jump", "fall", "climb", "drag"


class Pet:
    def __init__(self, anims, win_size, bounds):
        self.anims = anims
        self.win_w, self.win_h = win_size

        # 活动边界：(左, 上, 右, 下) 均为窗口左上角可取的屏幕坐标范围
        self.left, self.top, self.right, self.bottom = bounds

        # 位置 / 速度（浮点，保证低速移动也平滑）
        self.x = float((self.left + self.right) // 2)
        self.y = float(self.bottom)
        self.vx = 0.0
        self.vy = 0.0

        self.facing = 1            # 1 朝右，-1 朝左
        self.state = S_IDLE
        self.timer = 0.0           # 当前行为剩余时间（秒）
        self.anim_index = 0        # 当前帧序号
        self.anim_time = 0.0       # 当前帧已播放时长
        self.breath_phase = 0.0    # 呼吸动作相位

        # 拖拽相关
        self.pressed = False       # 左键是否按下
        self.dragging = False      # 是否已判定为拖拽
        self.press_screen = (0, 0) # 按下瞬间的鼠标屏幕坐标
        self.grab_offset = (0, 0)  # 鼠标相对窗口左上角的抓取偏移
        self.last_drag_pos = None  # 上一帧位置，用于计算甩出速度
        self.draw_pos = (self.x, self.y)   # 上一帧真实绘制坐标，供像素级命中判定使用

        self.pick_idle_behavior()

    # ------------------------------------------------------------------ 工具
    @property
    def on_ground(self):
        """是否站在地面上（留 0.5px 容差，避免浮点误差导致的抖动）。"""
        return self.y >= self.bottom - 0.5

    def set_state(self, state):
        """切换状态并重置动画播放进度（同状态重复调用不会打断动画）。"""
        if self.state != state:
            self.state = state
            self.anim_index = 0
            self.anim_time = 0.0

    def update_bounds(self, bounds):
        """分辨率 / 任务栏变化时刷新活动范围，并把宠物拉回可视区域。"""
        self.left, self.top, self.right, self.bottom = bounds
        self.x = min(max(self.x, self.left), self.right)
        self.y = min(self.y, self.bottom)

    # -------------------------------------------------------------- 行为决策
    def pick_idle_behavior(self):
        """随机决定「站一会儿」还是「走一段」——闲置 AI 的核心。"""
        if random.random() < 0.5:
            self.set_state(S_IDLE)
            self.vx = 0.0
            self.timer = random.uniform(IDLE_MIN_SEC, IDLE_MAX_SEC)
        else:
            self.set_state(S_WALK)
            self.facing = random.choice((-1, 1))
            self.vx = WALK_SPEED * self.facing
            self.timer = random.uniform(WALK_MIN_SEC, WALK_MAX_SEC)

    def jump(self, forward=True):
        """起跳。只有站在地面上才生效，避免空中连跳。"""
        if not self.on_ground:
            return
        self.vy = JUMP_VELOCITY
        self.vx = JUMP_FORWARD * self.facing if forward else 0.0
        self.set_state(S_JUMP)
        self.timer = 0.0

    def start_climb(self, wall_dir):
        """开始贴墙攀爬。wall_dir: -1 左墙，1 右墙。"""
        self.facing = wall_dir
        self.vx = 0.0
        self.vy = -CLIMB_SPEED
        self.set_state(S_CLIMB)
        self.timer = random.uniform(CLIMB_MIN_SEC, CLIMB_MAX_SEC)

    def hit_wall(self, wall_dir):
        """
        撞墙处理：按 CLIMB_CHANCE 概率选择「贴边攀爬」，否则原地折返。
        只有站在地面上才可能起爬，空中撞墙一律折返。
        """
        if self.on_ground and random.random() < CLIMB_CHANCE:
            self.start_climb(wall_dir)
        else:
            self.facing = -wall_dir
            self.vx = abs(self.vx) * self.facing if self.vx else WALK_SPEED * self.facing
            if self.state == S_WALK:
                self.timer = max(self.timer, 0.6)   # 折返后至少再走一会儿

    # ------------------------------------------------------------ 每帧更新
    def update(self, dt):
        """
        dt 为秒。所有物理参数按 60FPS 标定，这里用 k = dt * FPS 做归一化，
        因此改 FPS 不会改变移动手感。
        """
        k = dt * FPS
        self.breath_phase += dt * BREATH_SPEED

        # ---- 拖拽中：位置由鼠标直接接管，跳过物理 ----
        if self.state == S_DRAG:
            self.anim_step(dt)
            return

        # ---- 攀爬：贴住墙面向上，不受重力影响 ----
        if self.state == S_CLIMB:
            self.timer -= dt
            self.y += self.vy * k
            self.x = self.left if self.facing < 0 else self.right   # 死死贴住墙
            # 爬到顶 / 爬够时间 -> 蹬墙脱手，转为下落
            if self.y <= self.top or self.timer <= 0:
                self.y = max(self.y, self.top)
                self.facing = -self.facing
                self.vx = WALK_SPEED * self.facing
                self.vy = 0.0
                self.set_state(S_FALL)
            self.anim_step(dt)
            return

        # ---- 通用物理：重力 + 水平位移 ----
        self.vy = min(self.vy + GRAVITY * k, MAX_FALL_SPEED)
        if not self.on_ground:
            self.vx *= AIR_DRAG ** k
        self.x += self.vx * k
        self.y += self.vy * k

        # ---- 左右边界 ----
        if self.x <= self.left:
            self.x = float(self.left)
            self.hit_wall(-1)
        elif self.x >= self.right:
            self.x = float(self.right)
            self.hit_wall(1)

        # ---- 落地 ----
        if self.y >= self.bottom:
            self.y = float(self.bottom)
            if self.vy > 0 and BOUNCE_ON_LAND > 0 and self.vy * BOUNCE_ON_LAND > 1.5:
                self.vy = -self.vy * BOUNCE_ON_LAND        # 轻微弹跳
            else:
                self.vy = 0.0
                if self.state in (S_JUMP, S_FALL):         # 空中动作着陆 -> 回归日常
                    self.vx = 0.0
                    self.pick_idle_behavior()
        else:
            # 在空中：上升算 jump，下降算 fall（方便用不同帧表现）
            self.set_state(S_JUMP if self.vy < 0 else S_FALL)

        # ---- 地面行为计时 ----
        if self.on_ground and self.state in (S_IDLE, S_WALK):
            self.timer -= dt
            if self.state == S_WALK:
                self.vx = WALK_SPEED * self.facing
            if self.timer <= 0:
                if random.random() < IDLE_JUMP_CHANCE:
                    self.jump(forward=(self.state == S_WALK))
                else:
                    self.pick_idle_behavior()

        self.anim_step(dt)

    def anim_step(self, dt):
        """推进当前动作的帧序号。loop=False 时播到最后一帧停住。"""
        anim = self.anims.get(self.state) or self.anims["idle"]
        frames = anim["right"]
        if len(frames) <= 1:
            self.anim_index = 0
            return
        self.anim_time += dt
        frame_dur = 1.0 / anim["fps"]
        while self.anim_time >= frame_dur:
            self.anim_time -= frame_dur
            if self.anim_index + 1 < len(frames):
                self.anim_index += 1
            elif anim["loop"]:
                self.anim_index = 0
            else:
                self.anim_index = len(frames) - 1
                break

    def current_frame(self):
        """取当前应绘制的 Surface（已按朝向预翻转）。"""
        anim = self.anims.get(self.state) or self.anims["idle"]
        frames = anim["left"] if (self.facing < 0 and FLIP_WHEN_LEFT) else anim["right"]
        return frames[min(self.anim_index, len(frames) - 1)]

    def draw_offset_y(self):
        """闲置时的呼吸式上下微动（只影响绘制，不影响物理与碰撞）。"""
        if self.state == S_IDLE and BREATH_AMPLITUDE > 0:
            return int(round(math.sin(self.breath_phase) * BREATH_AMPLITUDE))
        return 0

    # ------------------------------------------------------- 点击命中判定
    def hit_test(self, mx, my):
        """
        判断屏幕坐标 (mx, my) 是否落在宠物「不透明像素」上。
        用真实像素而不是矩形，所以宠物轮廓外的空白区域点不到（点击会穿透到桌面）。
        draw_pos 是上一帧实际绘制的窗口左上角坐标，误差最多一帧，无感。
        """
        fx, fy = self.draw_pos
        frame = self.current_frame()
        lx = int(mx - fx - (self.win_w - frame.get_width()) // 2)
        ly = int(my - fy - (self.win_h - frame.get_height()))
        if 0 <= lx < frame.get_width() and 0 <= ly < frame.get_height():
            return frame.get_at((lx, ly)).a > 0
        return False

    # ------------------------------------------------------------ 拖拽处理
    def begin_press(self):
        """左键按下：记录抓取信息，此时还不确定是单击还是拖拽。"""
        mx, my = get_cursor_pos()
        self.pressed = True
        self.dragging = False
        self.press_screen = (mx, my)
        self.grab_offset = (mx - self.x, my - self.y)

    def update_press(self):
        """
        按住期间每帧调用（用 Win32 取绝对坐标，避免鼠标移出宠物像素后丢事件）。
        移动超过 CLICK_DRAG_PX 才升级为拖拽。
        """
        mx, my = get_cursor_pos()
        if not self.dragging:
            if abs(mx - self.press_screen[0]) + abs(my - self.press_screen[1]) <= CLICK_DRAG_PX:
                return
            self.dragging = True
            self.set_state(S_DRAG)
            self.vx = self.vy = 0.0
            self.last_drag_pos = (self.x, self.y)

        nx = mx - self.grab_offset[0]
        ny = my - self.grab_offset[1]
        # 拖拽时允许略微越界，松手后物理会把它拉回来；这里只做宽松夹取
        self.x = min(max(nx, self.left - self.win_w * 0.5), self.right + self.win_w * 0.5)
        self.y = min(max(ny, self.top - self.win_h), self.bottom + self.win_h * 0.5)

        # 用位移差算出「甩」的速度
        if self.last_drag_pos:
            self.vx = (self.x - self.last_drag_pos[0]) * THROW_DAMPING
            self.vy = (self.y - self.last_drag_pos[1]) * THROW_DAMPING
        self.last_drag_pos = (self.x, self.y)

    def end_press(self):
        """左键松开：拖拽 -> 转入下落；未拖拽 -> 判定为单击，触发跳跃。"""
        was_drag = self.dragging
        self.pressed = False
        self.dragging = False
        self.last_drag_pos = None

        if was_drag:
            self.x = min(max(self.x, self.left), self.right)
            self.y = min(max(self.y, self.top), self.bottom)
            self.set_state(S_FALL)
        else:
            self.jump(forward=True)


# ==============================================================================
# 5. 主程序
# ==============================================================================

VK_LBUTTON = 0x01
VK_RBUTTON = 0x02
VK_ESCAPE  = 0x1B


def key_down(vk):
    """
    直接问系统某个键/鼠标键是否按下。

    为什么不用 pygame 事件：本窗口带 WS_EX_NOACTIVATE（点击不抢焦点），
    永远拿不到输入焦点，SDL 默认会丢弃未聚焦窗口的鼠标/键盘事件。
    所以鼠标与热键统一走 GetAsyncKeyState 轮询，不依赖焦点，也不会丢 MOUSEUP。
    """
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)


def compute_bounds(win_w, win_h):
    """根据工作区与配置，算出窗口左上角允许的坐标范围 (left, top, right, bottom)。"""
    wl, wt, wr, wb = get_work_area() if USE_WORK_AREA else (
        0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    left  = wl + MARGIN_LEFT
    right = max(left, wr - MARGIN_RIGHT - win_w)
    top   = wt
    bottom = max(top, wb - GROUND_OFFSET - win_h)
    return left, top, right, bottom


def main():
    enable_dpi_awareness()

    pygame.init()
    pygame.display.set_caption("Desktop Pet")

    # 先建一个 1x1 的隐藏窗口：convert_alpha() 必须在「已设置视频模式」后才能调用，
    # 而窗口尺寸又取决于加载完的素材尺寸——所以分两步走。
    # HIDDEN 同时避免了开场闪现一下不透明窗口。
    pygame.display.set_mode((1, 1), pygame.NOFRAME | pygame.HIDDEN)

    anims = load_animations()                       # 素材缺失会在这里抛出可读的错误

    # 窗口取所有帧的最大尺寸，保证任何一帧都不会被裁切
    all_frames = [f for a in anims.values() for f in a["right"]]
    win_w = max(f.get_width()  for f in all_frames)
    win_h = max(f.get_height() for f in all_frames)

    # 正式窗口：NOFRAME 无边框；不用 pygame.SCALED，避免和 Win32 移动窗口冲突
    screen = pygame.display.set_mode((win_w, win_h), pygame.NOFRAME | pygame.HIDDEN)

    hwnd = pygame.display.get_wm_info()["window"]
    setup_transparent_topmost(hwnd)                 # 先把透明/置顶属性配好
    show_window_no_activate(hwnd)                   # 再显示，全程无闪烁、不抢焦点

    pet = Pet(anims, (win_w, win_h), compute_bounds(win_w, win_h))
    clock = pygame.time.Clock()

    running = True
    topmost_timer = 0.0                             # 定期重置置顶
    bounds_timer  = 0.0                             # 定期刷新工作区（应对分辨率变化）
    prev_left  = left = key_down(VK_LBUTTON)        # 上一帧按键状态，用于取「边沿」
    prev_right = key_down(VK_RBUTTON)

    try:
        while running:
            dt = clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)                      # 卡顿时限幅，防止一帧穿透地面

            # ---------------- 系统事件（主要用于兜底的 QUIT）----------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # ---------------- 鼠标 / 热键轮询（不依赖窗口焦点）----------------
            left  = key_down(VK_LBUTTON)
            right = key_down(VK_RBUTTON)
            mx, my = get_cursor_pos()

            if left and not prev_left and not pet.pressed:
                if pet.hit_test(mx, my):            # 只有点在宠物身上才响应
                    pet.begin_press()
            if pet.pressed:
                if left:
                    pet.update_press()
                else:
                    pet.end_press()                 # 松手：拖拽落地 或 判定为单击->跳跃

            if right and not prev_right and pet.hit_test(mx, my):
                running = False                     # 右键点宠物 = 退出

            if key_down(VK_ESCAPE) and pet.hit_test(mx, my):
                running = False                     # 鼠标悬停在宠物上按 ESC = 退出

            prev_left, prev_right = left, right

            # ---------------- 物理 / AI ----------------
            pet.update(dt)

            # ---------------- 窗口维护 ----------------
            topmost_timer += dt
            if topmost_timer >= 2.0:                # 每 2 秒抢回一次置顶
                topmost_timer = 0.0
                set_topmost(hwnd)

            bounds_timer += dt
            if bounds_timer >= 3.0:
                bounds_timer = 0.0
                pet.update_bounds(compute_bounds(win_w, win_h))

            # 真实窗口坐标 = 物理坐标 + 呼吸微动偏移；记录下来供下一帧命中判定
            wx = int(round(pet.x))
            wy = int(round(pet.y)) + pet.draw_offset_y()
            pet.draw_pos = (wx, wy)
            move_window(hwnd, wx, wy)

            # ---------------- 绘制 ----------------
            screen.fill(TRANSPARENT_COLOR)          # 整窗填透明色 = 全透明底
            frame = pet.current_frame()
            screen.blit(frame, ((win_w - frame.get_width()) // 2,   # 水平居中
                                win_h - frame.get_height()))        # 底部对齐
            if DEBUG_HITBOX:
                pygame.draw.rect(screen, (0, 255, 0), screen.get_rect(), 1)
            pygame.display.flip()
    finally:
        pygame.quit()                               # 无论正常退出还是异常，都干净收尾


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # 打包成无控制台 exe 后 print 看不见，所以用消息框把错误弹出来
        try:
            user32.MessageBoxW(0, str(exc), "桌面宠物 启动失败", 0x10)
        except Exception:
            print("启动失败：", exc)
        sys.exit(1)
