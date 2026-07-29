# 桌面悬浮宠物 Desktop Pet

Windows 桌面透明悬浮宠物，pygame + Win32 分层窗口实现。单文件代码，放一张 `pet.png` 即可运行。

```
desktop-pet/
├── desktop_pet.py   # 主程序（配置区在文件顶部）
├── pet.png          # 宠物素材（当前是占位图，替换成你自己的）
└── README.md
```

## 1. 环境安装

```bat
python -m pip install --upgrade pip
python -m pip install pygame numpy
```

`numpy` 是可选加速项：用于把素材边缘的半透明像素批量二值化。没装也能跑，程序会自动回退到纯 pygame 的逐像素处理（首次启动慢 1~2 秒）。

运行：

```bat
cd /d "c:\Users\hyji11\Desktop\个人小项目\desktop-pet"
python desktop_pet.py
```

## 2. 操作方式

| 操作 | 效果 |
| --- | --- |
| 左键单击宠物 | 跳跃 |
| 左键按住拖动 | 拖拽到任意位置，松手后按重力落地（快速甩动会有惯性） |
| 右键点击宠物 | 退出程序 |
| 鼠标悬停在宠物上按 ESC | 退出程序 |

宠物空闲时会自行随机走动、原地小跳、站立时轻微呼吸起伏；走到屏幕左右边缘会随机选择折返或贴墙向上攀爬，爬到一定高度后蹬墙落下。

只有宠物的不透明像素才响应鼠标，轮廓外的空白区域点击会穿透到桌面。

## 3. 常用参数

全部集中在 `desktop_pet.py` 顶部「配置区」：

| 参数 | 含义 | 默认 |
| --- | --- | --- |
| `PET_HEIGHT` | 宠物高度(px)，宽度按比例自动缩放 | `120` |
| `PET_SCALE` | 按原图倍数缩放，填了数字则 `PET_HEIGHT` 失效 | `None` |
| `JUMP_VELOCITY` | 跳跃初速度，负数向上，绝对值越大跳越高 | `-13.0` |
| `WALK_SPEED` | 走动速度 | `1.6` |
| `CLIMB_SPEED` | 攀爬速度 | `1.4` |
| `GRAVITY` | 重力加速度 | `0.60` |
| `GROUND_OFFSET` | 地面上移量，调大可让宠物站得更高 | `0` |
| `CLIMB_CHANCE` | 撞墙时选择攀爬而非折返的概率 | `0.45` |
| `IDLE_JUMP_CHANCE` | 闲置结束时随机小跳的概率 | `0.18` |
| `BREATH_AMPLITUDE` | 站立呼吸起伏幅度，`0` 关闭 | `2.0` |
| `EDGE_ALPHA_THRESHOLD` | 边缘半透明像素阈值，边缘发白/发紫就调小 | `128` |
| `DEBUG_HITBOX` | 画出窗口边框，调试用 | `False` |

## 4. 扩展多帧动画

配置区的 `ANIMATIONS` 已经预留好接口。把帧图放进同一文件夹，填上文件名即可自动逐帧播放：

```python
ANIMATIONS = {
    "idle":  {"frames": ["pet.png"],                         "fps": 6, "loop": True},
    "walk":  {"frames": ["pet_walk1.png", "pet_walk2.png"],  "fps": 8, "loop": True},
    "jump":  {"frames": ["pet_jump1.png", "pet_jump2.png"],  "fps": 8, "loop": False},
    "fall":  {"frames": ["pet_fall.png"],                    "fps": 6, "loop": True},
    "climb": {"frames": ["pet_climb1.png","pet_climb2.png"], "fps": 7, "loop": True},
    "drag":  {"frames": ["pet_drag.png"],                    "fps": 6, "loop": True},
}
```

规则：

- 文件不存在的帧自动跳过，某个动作一帧都没有时回退到 `idle`，所以现在只有 `pet.png` 也能正常跑，加多少帧算多少帧。
- `loop: False` 表示播到最后一帧停住（`jump` 建议这样）。
- 朝左的图由程序自动水平翻转，不用另画一套。若你想自己画左向帧，把 `FLIP_WHEN_LEFT` 设为 `False`。
- 窗口尺寸取所有帧的最大值，各帧尺寸不一致也不会被裁切（绘制时底部对齐、水平居中）。

## 5. PyInstaller 打包单文件 exe

```bat
python -m pip install pyinstaller

cd /d "c:\Users\hyji11\Desktop\个人小项目\desktop-pet"

pyinstaller --onefile --noconsole --name DesktopPet desktop_pet.py
```

产物：`dist\DesktopPet.exe`。**把 `pet.png` 复制到 `dist\` 里和 exe 放一起**，双击即可运行。

### 参数含义

| 参数 | 含义 |
| --- | --- |
| `--onefile` | 打成独立单个 exe，所有依赖压缩进一个文件，运行时自解压到临时目录 |
| `--noconsole` | 不带控制台窗口（等价 `--windowed` / `-w`），否则会弹一个黑色 cmd 窗口 |
| `--name DesktopPet` | 指定输出名为 `DesktopPet.exe`，不指定则用脚本名 |

可选增强：

```bat
:: 带自定义图标
pyinstaller --onefile --noconsole --name DesktopPet --icon=pet.ico desktop_pet.py

:: 把 pet.png 也塞进 exe（这样单个 exe 就能跑，不用带图片）
pyinstaller --onefile --noconsole --name DesktopPet --add-data "pet.png;." desktop_pet.py
```

`--add-data "源;目标"` 中 Windows 用分号分隔。注意：代码里素材优先从 **exe 所在目录** 读取，这是故意的设计，方便你打包后直接换图不必重新打包；用 `--add-data` 内嵌时，需要把 `resource_dir()` 改为优先返回 `sys._MEIPASS`。

打包后清理中间产物：`rmdir /s /q build` 和 `del DesktopPet.spec`。

## 6. 注意事项

**仅 Windows 可用。** 透明置顶依赖 Win32 分层窗口（`WS_EX_LAYERED` + `LWA_COLORKEY`）和 `SetWindowPos`，macOS / Linux 下无法运行。

**透明窗口的限制：**

- 使用颜色键抠透明，透明色是洋红 `(255, 0, 255)`。素材里**不能出现这个颜色**，否则那部分会变成洞。真要用洋红，改配置区的 `TRANSPARENT_COLOR` 换一个偏门颜色。
- 颜色键透明是非 0/1 的：像素要么全透明要么全不透明，**不支持半透明**。所以程序会把边缘的半透明像素二值化（`EDGE_ALPHA_THRESHOLD`），代价是抗锯齿边缘会稍硬。若看到宠物周围有一圈紫边或白边，把这个值调小（如 `64`）；若边缘出现锯齿缺口，调大（如 `180`）。
- 独占全屏的游戏/视频会盖住宠物，这是 Windows 的层级机制决定的。程序每 2 秒会重新抢一次置顶，切回窗口模式后宠物自动回到最上层。
- 窗口带 `WS_EX_NOACTIVATE`，点击宠物不会打断你正在打字的窗口。代价是它永远拿不到输入焦点，所以鼠标和 ESC 都改成了 Win32 轮询（`GetAsyncKeyState`），这也是 ESC 需要先把鼠标移到宠物身上才生效的原因。
- 默认不在任务栏和 Alt+Tab 里显示（`HIDE_FROM_TASKBAR`）。想从任务栏关掉它就把这项设为 `False`，或直接右键宠物退出、任务管理器结束 `DesktopPet.exe`。
- 已开启 Per-Monitor DPI 感知。系统缩放 125%/150% 下位置和清晰度都正常；多显示器目前只在主屏活动。

**素材存放位置：**

- 源码运行：`pet.png` 和 `desktop_pet.py` 同一文件夹。
- 打包后运行：`pet.png` 和 `DesktopPet.exe` 同一文件夹（即 `dist\`）。
- 找不到素材时会弹消息框提示预期路径，不会静默崩溃。

## 7. 关于素材去背景

当前 `pet.png` 是程序生成的占位小猫图（102×120），用来验证功能。换成你自己的图后，如果背景没抠干净（白底、灰底、边缘残留），把图发我，我给你具体的去背景步骤。透明背景 PNG 的效果直接决定观感，这一步值得做细。
