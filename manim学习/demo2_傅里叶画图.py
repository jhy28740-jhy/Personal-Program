"""
manim 炫酷版：傅里叶级数画心形
运行命令：
    python -m manim -ql demo2_傅里叶画图.py FourierHeart

高清版用 -qh（渲染慢但画质好）

原理：
    任何闭合曲线都能用复数傅里叶级数表示
    c(t) = Σ c_n * e^(i*n*ω*t)
    几何意义 = 多个圆嵌套旋转，最外层点的轨迹就是目标曲线
"""
from manim import *
import numpy as np


class FourierHeart(Scene):
    def construct(self):
        # 标题
        title = Text("傅里叶级数：用圆画心形", font="Microsoft YaHei", color=PINK)\
            .scale(0.8).to_edge(UP)
        self.add(title)

        # 心形的参数方程（极坐标形式）
        def heart_func(t):
            # 心形曲线：r = 1 - sin(θ)
            # 转成笛卡尔坐标
            x = 16 * np.sin(t)**3
            y = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)
            return np.array([x, y, 0]) * 0.15  # 缩放到合适大小

        # 采样点
        t_values = np.linspace(0, TAU, 200)
        points = [heart_func(t) for t in t_values]

        # 计算傅里叶系数（离散傅里叶变换）
        n_circles = 15  # 圆的数量，越多越精确
        coefficients = self.compute_fourier_coefficients(points, n_circles)

        # 创建旋转圆系统
        circles = VGroup()
        vectors = VGroup()

        center = ORIGIN + DOWN * 0.5
        current_pos = center.copy()

        for n in range(-n_circles, n_circles + 1):
            if n == 0:
                continue
            radius = np.abs(coefficients[n + n_circles])
            if radius < 0.01:  # 跳过太小的圆
                continue

            circle = Circle(radius=radius, color=BLUE_D, stroke_width=1, stroke_opacity=0.5)
            circle.move_to(current_pos)

            angle = np.angle(coefficients[n + n_circles])
            vector = Arrow(
                current_pos,
                current_pos + radius * np.array([np.cos(angle), np.sin(angle), 0]),
                buff=0, stroke_width=2, color=YELLOW, max_tip_length_to_length_ratio=0.1
            )

            circles.add(circle)
            vectors.add(vector)
            current_pos = vector.get_end()

        # 绘制路径
        path = TracedPath(
            lambda: vectors[-1].get_end() if len(vectors) > 0 else ORIGIN,
            stroke_color=RED,
            stroke_width=3,
            dissipating_time=None  # 路径不消失
        )

        self.add(circles, vectors, path)

        # 动画：旋转一圈（周期）
        def update_system(mob, alpha):
            t = alpha * TAU
            current_pos = center.copy()
            circle_idx = 0
            vector_idx = 0

            for n in range(-n_circles, n_circles + 1):
                if n == 0:
                    continue
                radius = np.abs(coefficients[n + n_circles])
                if radius < 0.01:
                    continue

                angle = np.angle(coefficients[n + n_circles]) + n * t

                if circle_idx < len(circles):
                    circles[circle_idx].move_to(current_pos)
                if vector_idx < len(vectors):
                    new_end = current_pos + radius * np.array([np.cos(angle), np.sin(angle), 0])
                    vectors[vector_idx].put_start_and_end_on(current_pos, new_end)
                    current_pos = new_end

                circle_idx += 1
                vector_idx += 1

        system = VGroup(circles, vectors)
        self.play(
            UpdateFromAlphaFunc(system, update_system),
            rate_func=linear,
            run_time=8
        )
        self.wait(1)

    def compute_fourier_coefficients(self, points, n_terms):
        """计算离散傅里叶系数"""
        N = len(points)
        coefficients = []

        for n in range(-n_terms, n_terms + 1):
            coef = 0
            for k, point in enumerate(points):
                # 转成复数
                z = complex(point[0], point[1])
                coef += z * np.exp(-1j * n * TAU * k / N)
            coef /= N
            coefficients.append(coef)

        return coefficients


class FourierStar(Scene):
    """额外赠送：五角星版本（运行更快）"""
    def construct(self):
        title = Text("傅里叶级数：用圆画五角星", font="Microsoft YaHei", color=GOLD)\
            .scale(0.8).to_edge(UP)
        self.add(title)

        # 五角星路径
        star = Star(n=5, color=YELLOW, fill_opacity=0).scale(1.5).shift(DOWN*0.5)
        points = [star.point_from_proportion(t) for t in np.linspace(0, 1, 100)]

        # 简化版：只用几个关键圆
        n_circles = 10
        coefficients = self.compute_fourier_coefficients(points, n_circles)

        circles = VGroup()
        vectors = VGroup()
        center = ORIGIN + DOWN * 0.5

        for n in range(-n_circles, n_circles + 1):
            if n == 0:
                continue
            radius = np.abs(coefficients[n + n_circles])
            if radius < 0.05:
                continue

            circle = Circle(radius=radius, color=BLUE, stroke_width=1.5, stroke_opacity=0.3)
            angle = np.angle(coefficients[n + n_circles])
            vector = Line(
                ORIGIN, radius * RIGHT, color=YELLOW, stroke_width=2.5
            ).rotate(angle, about_point=ORIGIN)

            circles.add(circle)
            vectors.add(vector)

        path = TracedPath(
            lambda: vectors[-1].get_end() if len(vectors) > 0 else ORIGIN,
            stroke_color=RED, stroke_width=4
        )

        system = VGroup(circles, vectors).move_to(center)
        self.add(circles, vectors, path)

        def updater(mob, alpha):
            t = alpha * TAU
            pos = center.copy()
            for i, n in enumerate([k for k in range(-n_circles, n_circles+1) if k != 0]):
                if i >= len(circles):
                    break
                radius = np.abs(coefficients[n + n_circles])
                if radius < 0.05:
                    continue
                angle = np.angle(coefficients[n + n_circles]) + n * t
                circles[i].move_to(pos)
                new_pos = pos + radius * np.array([np.cos(angle), np.sin(angle), 0])
                vectors[i].put_start_and_end_on(pos, new_pos)
                pos = new_pos

        self.play(
            UpdateFromAlphaFunc(VGroup(circles, vectors), updater),
            rate_func=linear,
            run_time=6
        )
        self.wait(1)

    def compute_fourier_coefficients(self, points, n_terms):
        N = len(points)
        coefficients = []
        for n in range(-n_terms, n_terms + 1):
            coef = sum(
                complex(p[0], p[1]) * np.exp(-1j * n * TAU * k / N)
                for k, p in enumerate(points)
            ) / N
            coefficients.append(coef)
        return coefficients
