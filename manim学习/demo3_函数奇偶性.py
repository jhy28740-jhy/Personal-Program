"""
函数奇偶性可视化教学
运行命令：
    python -m manim -qh demo3_函数奇偶性.py FunctionParity

教学内容：
    1. 偶函数定义与对称性（y轴对称）
    2. 奇函数定义与对称性（原点对称）
    3. 具体例子对比
"""
from manim import *


class FunctionParity(Scene):
    def construct(self):
        # ========== 第一部分：标题与定义 ==========
        title = Text("函数的奇偶性", font="Microsoft YaHei", color=YELLOW, weight=BOLD)\
            .scale(1.2).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ========== 第二部分：偶函数 ==========
        subtitle_even = Text("偶函数 (Even Function)", font="Microsoft YaHei", color=GREEN)\
            .scale(0.8).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle_even))
        self.wait(0.3)

        # 定义文字
        definition_even = VGroup(
            Text("定义: f(-x) = f(x)", font="Microsoft YaHei", color=WHITE).scale(0.6),
            Text("对称性: 关于 y 轴对称", font="Microsoft YaHei", color=BLUE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(subtitle_even, DOWN, buff=0.4)

        self.play(Write(definition_even[0]))
        self.wait(0.5)
        self.play(Write(definition_even[1]))
        self.wait(0.8)

        # 坐标系与偶函数图像 f(x) = x²
        axes_even = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 2],
            x_length=6,
            y_length=4,
            axis_config={"color": GREY, "include_numbers": False},
        ).shift(DOWN * 1)

        # y轴标注
        y_axis_label = Text("y轴", font="Microsoft YaHei", color=BLUE).scale(0.4)\
            .next_to(axes_even.y_axis.get_top(), RIGHT, buff=0.1)

        graph_even = axes_even.plot(lambda x: x**2, color=GREEN, x_range=[-2.5, 2.5])
        graph_label = Text("f(x) = x²", font="Microsoft YaHei", color=GREEN).scale(0.5)\
            .next_to(graph_even, UP, buff=0.2).shift(RIGHT * 1)

        self.play(
            FadeOut(definition_even),
            Create(axes_even),
            Write(y_axis_label)
        )
        self.play(Create(graph_even), Write(graph_label))
        self.wait(0.5)

        # 对称性演示：标记对称点
        dot_right = Dot(axes_even.c2p(1.5, 1.5**2), color=RED, radius=0.08)
        dot_left = Dot(axes_even.c2p(-1.5, 1.5**2), color=RED, radius=0.08)

        label_right = Text("f(a)", font="Microsoft YaHei", color=RED).scale(0.4)\
            .next_to(dot_right, UR, buff=0.1)
        label_left = Text("f(-a)", font="Microsoft YaHei", color=RED).scale(0.4)\
            .next_to(dot_left, UL, buff=0.1)

        # 对称线（虚线）
        dashed_line = DashedLine(
            axes_even.c2p(-1.5, 1.5**2),
            axes_even.c2p(1.5, 1.5**2),
            color=YELLOW,
            stroke_width=2
        )

        self.play(FadeIn(dot_right), Write(label_right))
        self.wait(0.3)
        self.play(Create(dashed_line))
        self.play(FadeIn(dot_left), Write(label_left))
        self.wait(1)

        # 强调对称轴
        symmetry_arrow = Arrow(
            axes_even.y_axis.get_top() + UP * 0.3,
            axes_even.y_axis.get_top() + DOWN * 0.3,
            color=BLUE,
            stroke_width=4,
            buff=0
        )
        self.play(GrowArrow(symmetry_arrow), y_axis_label.animate.set_color(YELLOW))
        self.wait(1.5)

        # 清屏
        self.play(
            *[FadeOut(mob) for mob in [
                subtitle_even, axes_even, graph_even, graph_label,
                dot_right, dot_left, label_right, label_left,
                dashed_line, symmetry_arrow, y_axis_label
            ]]
        )

        # ========== 第三部分：奇函数 ==========
        subtitle_odd = Text("奇函数 (Odd Function)", font="Microsoft YaHei", color=ORANGE)\
            .scale(0.8).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle_odd))
        self.wait(0.3)

        # 定义文字
        definition_odd = VGroup(
            Text("定义: f(-x) = -f(x)", font="Microsoft YaHei", color=WHITE).scale(0.6),
            Text("对称性: 关于原点对称", font="Microsoft YaHei", color=PURPLE).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(subtitle_odd, DOWN, buff=0.4)

        self.play(Write(definition_odd[0]))
        self.wait(0.5)
        self.play(Write(definition_odd[1]))
        self.wait(0.8)

        # 坐标系与奇函数图像 f(x) = x³
        axes_odd = Axes(
            x_range=[-2, 2, 1],
            y_range=[-8, 8, 2],
            x_length=6,
            y_length=4,
            axis_config={"color": GREY, "include_numbers": False},
        ).shift(DOWN * 1)

        # 原点标注
        origin_dot = Dot(axes_odd.c2p(0, 0), color=PURPLE, radius=0.08)
        origin_label = Text("原点", font="Microsoft YaHei", color=PURPLE).scale(0.4)\
            .next_to(origin_dot, DR, buff=0.15)

        graph_odd = axes_odd.plot(lambda x: x**3, color=ORANGE, x_range=[-1.8, 1.8])
        graph_label_odd = Text("f(x) = x³", font="Microsoft YaHei", color=ORANGE).scale(0.5)\
            .next_to(graph_odd, RIGHT, buff=0.2).shift(UP * 0.5)

        self.play(
            FadeOut(definition_odd),
            Create(axes_odd),
            FadeIn(origin_dot),
            Write(origin_label)
        )
        self.play(Create(graph_odd), Write(graph_label_odd))
        self.wait(0.5)

        # 对称性演示：标记对称点
        a_val = 1.2
        dot_right_odd = Dot(axes_odd.c2p(a_val, a_val**3), color=RED, radius=0.08)
        dot_left_odd = Dot(axes_odd.c2p(-a_val, -a_val**3), color=RED, radius=0.08)

        label_right_odd = Text("f(a)", font="Microsoft YaHei", color=RED).scale(0.4)\
            .next_to(dot_right_odd, UR, buff=0.1)
        label_left_odd = Text("f(-a) = -f(a)", font="Microsoft YaHei", color=RED).scale(0.4)\
            .next_to(dot_left_odd, DL, buff=0.1)

        # 旋转对称线（通过原点）
        symmetry_line = Line(
            axes_odd.c2p(-a_val, -a_val**3),
            axes_odd.c2p(a_val, a_val**3),
            color=YELLOW,
            stroke_width=2
        )

        self.play(FadeIn(dot_right_odd), Write(label_right_odd))
        self.wait(0.3)
        self.play(Create(symmetry_line))
        self.play(FadeIn(dot_left_odd), Write(label_left_odd))
        self.wait(1)

        # 旋转演示原点对称
        rotation_group = VGroup(dot_right_odd.copy(), label_right_odd.copy())
        self.play(
            Rotate(rotation_group, angle=PI, about_point=axes_odd.c2p(0, 0)),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1.5)

        # 清屏
        self.play(
            *[FadeOut(mob) for mob in [
                subtitle_odd, axes_odd, graph_odd, graph_label_odd,
                dot_right_odd, dot_left_odd, label_right_odd, label_left_odd,
                symmetry_line, origin_dot, origin_label, rotation_group
            ]]
        )

        # ========== 第四部分：对比总结 ==========
        summary_title = Text("总结对比", font="Microsoft YaHei", color=YELLOW)\
            .scale(0.9).next_to(title, DOWN, buff=0.5)
        self.play(Write(summary_title))
        self.wait(0.3)

        # 左右对比图
        axes_compare_left = Axes(
            x_range=[-2, 2, 1], y_range=[0, 4, 1],
            x_length=4, y_length=2.5,
            axis_config={"color": GREY, "include_numbers": False}
        ).shift(LEFT * 3 + DOWN * 1.5)

        axes_compare_right = Axes(
            x_range=[-2, 2, 1], y_range=[-4, 4, 2],
            x_length=4, y_length=2.5,
            axis_config={"color": GREY, "include_numbers": False}
        ).shift(RIGHT * 3 + DOWN * 1.5)

        graph_even_cmp = axes_compare_left.plot(lambda x: x**2, color=GREEN, x_range=[-1.8, 1.8])
        graph_odd_cmp = axes_compare_right.plot(lambda x: x**3, color=ORANGE, x_range=[-1.5, 1.5])

        label_even_cmp = Text("偶函数: y轴对称", font="Microsoft YaHei", color=GREEN)\
            .scale(0.5).next_to(axes_compare_left, UP, buff=0.3)
        label_odd_cmp = Text("奇函数: 原点对称", font="Microsoft YaHei", color=ORANGE)\
            .scale(0.5).next_to(axes_compare_right, UP, buff=0.3)

        self.play(
            Create(axes_compare_left), Create(axes_compare_right),
            Create(graph_even_cmp), Create(graph_odd_cmp),
            Write(label_even_cmp), Write(label_odd_cmp)
        )
        self.wait(3)

        # 结束
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        end_text = Text("感谢观看！", font="Microsoft YaHei", color=YELLOW, weight=BOLD)\
            .scale(1.5)
        self.play(Write(end_text))
        self.wait(2)
