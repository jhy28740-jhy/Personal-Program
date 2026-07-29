"""
镜子王国的秘密 - 函数奇偶性趣味教学
运行命令：
    python -m manim -qh demo4_镜子王国.py MirrorKingdom

创意设计：
    - 场景化：镜子王国的两位居民
    - 角色化：小球代表函数值，会跳舞
    - 故事线：先展示现象（神奇的对称），再揭秘原理
    - 悬念感：为什么有的镜子左右对称，有的要倒立？
"""
from manim import *


class MirrorKingdom(Scene):
    def construct(self):
        # ========== 开场：镜子王国 ==========
        # 标题动画
        title = Text("镜子王国的秘密", font="Microsoft YaHei", color=GOLD, weight=BOLD)\
            .scale(1.5)
        subtitle = Text("探索函数的对称之美", font="Microsoft YaHei", color=BLUE_C)\
            .scale(0.8).next_to(title, DOWN, buff=0.3)

        self.play(
            Write(title, run_time=1.5),
            FadeIn(subtitle, shift=UP*0.3)
        )
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ========== 第一幕：普通镜子（偶函数） ==========
        scene_title_1 = Text("第一面镜子：完美复制", font="Microsoft YaHei", color=GREEN)\
            .scale(0.9).to_edge(UP)
        self.play(FadeIn(scene_title_1))

        # 画镜子（y轴）
        mirror = Line(UP*3, DOWN*3, color=BLUE_B, stroke_width=8)
        mirror_glow = mirror.copy().set_stroke(BLUE_C, width=15, opacity=0.3)
        mirror_label = Text("魔法镜", font="Microsoft YaHei", color=BLUE_B)\
            .scale(0.5).next_to(mirror, UP, buff=0.2)

        self.play(
            Create(mirror_glow),
            Create(mirror),
            Write(mirror_label),
            run_time=1.5
        )
        self.wait(0.5)

        # 左边出现一个小球（代表函数值）
        ball_left = Dot(LEFT*2 + UP*1, radius=0.15, color=RED)
        ball_left_label = Text("我", font="Microsoft YaHei", color=RED)\
            .scale(0.4).next_to(ball_left, DOWN, buff=0.15)

        self.play(
            GrowFromCenter(ball_left),
            Write(ball_left_label)
        )
        self.wait(0.3)

        # 镜子里出现对称的球
        ball_right = ball_left.copy().move_to(RIGHT*2 + UP*1)
        ball_right_label = ball_left_label.copy().next_to(ball_right, DOWN, buff=0.15)

        flash = Circle(radius=0.3, color=YELLOW, stroke_width=3)\
            .move_to(ball_right.get_center())

        self.play(
            Flash(ball_right.get_center(), color=YELLOW, flash_radius=0.5),
            FadeIn(flash.scale(0.01)),
            flash.animate.scale(100).set_opacity(0),
            GrowFromCenter(ball_right),
            Write(ball_right_label),
            run_time=0.8
        )
        self.remove(flash)
        self.wait(0.5)

        # 小球跳舞（上下移动）
        dance_text = Text("试试跳舞！", font="Microsoft YaHei", color=YELLOW)\
            .scale(0.6).to_edge(DOWN)
        self.play(Write(dance_text))

        for _ in range(2):
            self.play(
                ball_left.animate.shift(UP*0.5),
                ball_left_label.animate.shift(UP*0.5),
                ball_right.animate.shift(UP*0.5),
                ball_right_label.animate.shift(UP*0.5),
                run_time=0.4
            )
            self.play(
                ball_left.animate.shift(DOWN*1),
                ball_left_label.animate.shift(DOWN*1),
                ball_right.animate.shift(DOWN*1),
                ball_right_label.animate.shift(DOWN*1),
                run_time=0.4
            )
            self.play(
                ball_left.animate.shift(UP*0.5),
                ball_left_label.animate.shift(UP*0.5),
                ball_right.animate.shift(UP*0.5),
                ball_right_label.animate.shift(UP*0.5),
                run_time=0.4
            )

        self.play(FadeOut(dance_text))
        self.wait(0.3)

        # 揭秘：这就是偶函数
        secret_box = Rectangle(width=6, height=1.5, color=GREEN, fill_opacity=0.2)\
            .to_edge(DOWN, buff=0.5)
        secret_title = Text("揭秘：偶函数", font="Microsoft YaHei", color=GREEN, weight=BOLD)\
            .scale(0.7).next_to(secret_box, UP, buff=0.1).shift(DOWN*0.6)
        secret_text = Text("f(-x) = f(x)  镜子左右完美对称", font="Microsoft YaHei", color=WHITE)\
            .scale(0.5).next_to(secret_title, DOWN, buff=0.2)

        self.play(
            Create(secret_box),
            Write(secret_title),
            Write(secret_text),
            run_time=1.5
        )
        self.wait(1.5)

        # 显示真实函数图像
        axes_small = Axes(
            x_range=[-2, 2, 1], y_range=[0, 2, 1],
            x_length=3, y_length=1.5,
            axis_config={"include_numbers": False, "color": GREY}
        ).shift(RIGHT*3.5 + DOWN*2)
        graph_even = axes_small.plot(lambda x: 0.5*x**2, color=GREEN)
        graph_label = Text("y=x²", font="Microsoft YaHei", color=GREEN)\
            .scale(0.4).next_to(axes_small, UP, buff=0.1)

        self.play(
            Create(axes_small),
            Create(graph_even),
            Write(graph_label),
            run_time=1
        )
        self.wait(2)

        # 清场
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # ========== 第二幕：魔法镜子（奇函数） ==========
        scene_title_2 = Text("第二面镜子：倒立魔法", font="Microsoft YaHei", color=ORANGE)\
            .scale(0.9).to_edge(UP)
        self.play(FadeIn(scene_title_2))

        # 原点（旋转中心）
        origin = Dot(ORIGIN, radius=0.12, color=PURPLE)
        origin_label = Text("魔法点", font="Microsoft YaHei", color=PURPLE)\
            .scale(0.4).next_to(origin, DOWN, buff=0.15)
        origin_glow = Circle(radius=0.3, color=PURPLE, stroke_width=2)\
            .move_to(origin.get_center())

        self.play(
            Create(origin_glow),
            GrowFromCenter(origin),
            Write(origin_label)
        )
        self.play(
            origin_glow.animate.scale(1.5).set_opacity(0.3),
            run_time=0.8
        )

        # 画坐标轴（但不强调镜子）
        axes_line_x = Line(LEFT*3, RIGHT*3, color=GREY, stroke_width=2)
        axes_line_y = Line(DOWN*3, UP*3, color=GREY, stroke_width=2)
        self.play(Create(axes_line_x), Create(axes_line_y))

        # 右上方出现小球
        ball_ru = Dot(RIGHT*1.5 + UP*1.2, radius=0.15, color=RED)
        ball_ru_label = Text("我", font="Microsoft YaHei", color=RED)\
            .scale(0.4).next_to(ball_ru, UR, buff=0.1)

        self.play(GrowFromCenter(ball_ru), Write(ball_ru_label))
        self.wait(0.3)

        # 魔法镜子的规则：旋转180度
        magic_text = Text("这面镜子会旋转魔法！", font="Microsoft YaHei", color=YELLOW)\
            .scale(0.6).to_edge(DOWN)
        self.play(Write(magic_text))
        self.wait(0.5)

        # 复制球并旋转到对称位置
        ball_ld = ball_ru.copy()
        ball_ld_label = ball_ru_label.copy()
        ball_ld_group = VGroup(ball_ld, ball_ld_label)

        # 旋转动画
        rotation_arc = Arc(
            radius=2, start_angle=PI/4, angle=PI,
            color=YELLOW, stroke_width=3
        ).shift(ORIGIN)

        self.play(
            Create(rotation_arc),
            Rotate(ball_ld_group, angle=PI, about_point=ORIGIN),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)
        self.play(FadeOut(rotation_arc), FadeOut(magic_text))

        # 揭秘：奇函数
        secret_box_2 = Rectangle(width=6, height=1.5, color=ORANGE, fill_opacity=0.2)\
            .to_edge(DOWN, buff=0.5)
        secret_title_2 = Text("揭秘：奇函数", font="Microsoft YaHei", color=ORANGE, weight=BOLD)\
            .scale(0.7).next_to(secret_box_2, UP, buff=0.1).shift(DOWN*0.6)
        secret_text_2 = Text("f(-x) = -f(x)  绕原点旋转180°", font="Microsoft YaHei", color=WHITE)\
            .scale(0.5).next_to(secret_title_2, DOWN, buff=0.2)

        self.play(
            Create(secret_box_2),
            Write(secret_title_2),
            Write(secret_text_2),
            run_time=1.5
        )
        self.wait(1.5)

        # 显示真实函数
        axes_small_2 = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=3, y_length=1.8,
            axis_config={"include_numbers": False, "color": GREY}
        ).shift(LEFT*3.5 + DOWN*1.8)
        graph_odd = axes_small_2.plot(lambda x: 0.3*x**3, color=ORANGE, x_range=[-1.8, 1.8])
        graph_label_2 = Text("y=x³", font="Microsoft YaHei", color=ORANGE)\
            .scale(0.4).next_to(axes_small_2, UP, buff=0.1)

        self.play(
            Create(axes_small_2),
            Create(graph_odd),
            Write(graph_label_2),
            run_time=1
        )
        self.wait(2)

        # 清场
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # ========== 结尾：总结 ==========
        end_title = Text("镜子王国的两大法则", font="Microsoft YaHei", color=GOLD, weight=BOLD)\
            .scale(1.2)
        self.play(Write(end_title))
        self.wait(0.5)
        self.play(end_title.animate.to_edge(UP))

        # 左右对比 - 偶函数
        even_title = Text("偶函数", font="Microsoft YaHei", color=GREEN, weight=BOLD).scale(0.8)
        even_subtitle = Text("左右镜像", font="Microsoft YaHei", color=WHITE).scale(0.5)
        even_formula = Text("f(-x) = f(x)", font="Microsoft YaHei", color=WHITE).scale(0.5)

        # 偶函数图像
        even_axes = Axes(
            x_range=[-2, 2, 1], y_range=[0, 2, 1],
            x_length=3.5, y_length=2,
            axis_config={"include_numbers": False, "color": GREY, "stroke_width": 1}
        )
        even_graph = even_axes.plot(lambda x: 0.5*x**2, color=GREEN, stroke_width=3)
        even_graph_group = VGroup(even_axes, even_graph)

        even_example = Text("例: x², |x|, cos(x)", font="Microsoft YaHei", color=GREEN).scale(0.45)

        even_box = Rectangle(width=5, height=5, color=GREEN, stroke_width=3, fill_opacity=0.05)

        even_content = VGroup(even_title, even_subtitle, even_formula, even_graph_group, even_example)\
            .arrange(DOWN, buff=0.3)
        even_all = VGroup(even_box, even_content).move_to(LEFT*3.2)

        # 右侧 - 奇函数
        odd_title = Text("奇函数", font="Microsoft YaHei", color=ORANGE, weight=BOLD).scale(0.8)
        odd_subtitle = Text("旋转180°", font="Microsoft YaHei", color=WHITE).scale(0.5)
        odd_formula = Text("f(-x) = -f(x)", font="Microsoft YaHei", color=WHITE).scale(0.5)

        # 奇函数图像
        odd_axes = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=3.5, y_length=2,
            axis_config={"include_numbers": False, "color": GREY, "stroke_width": 1}
        )
        odd_graph = odd_axes.plot(lambda x: 0.5*x**3, color=ORANGE, stroke_width=3, x_range=[-1.8, 1.8])
        odd_graph_group = VGroup(odd_axes, odd_graph)

        odd_example = Text("例: x³, x, sin(x)", font="Microsoft YaHei", color=ORANGE).scale(0.45)

        odd_box = Rectangle(width=5, height=5, color=ORANGE, stroke_width=3, fill_opacity=0.05)

        odd_content = VGroup(odd_title, odd_subtitle, odd_formula, odd_graph_group, odd_example)\
            .arrange(DOWN, buff=0.3)
        odd_all = VGroup(odd_box, odd_content).move_to(RIGHT*3.2)

        self.play(
            FadeIn(even_all, shift=RIGHT*0.5),
            FadeIn(odd_all, shift=LEFT*0.5),
            run_time=1.5
        )

        # 依次创建图像
        self.play(
            Create(even_graph),
            Create(odd_graph),
            run_time=2
        )
        self.wait(2)

        # 结束语
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        thanks = Text("感谢观看！", font="Microsoft YaHei", color=YELLOW, weight=BOLD)\
            .scale(1.8)
        subtext = Text("数学，原来可以这么有趣", font="Microsoft YaHei", color=BLUE_C)\
            .scale(0.7).next_to(thanks, DOWN, buff=0.5)

        self.play(Write(thanks, run_time=1.5))
        self.play(FadeIn(subtext, shift=UP*0.3))
        self.wait(3)
