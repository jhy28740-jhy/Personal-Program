"""
manim 第一个 demo(无需 LaTeX 版本)
运行命令(在本文件所在目录):
    python -m manim -pql demo1_勾股定理.py PythagoreanTheorem

参数说明:
    -p  渲染完自动播放
    -q  画质: l(低) m(中) h(高) k(4K)
    -ql = 低画质预览(快,适合调试)

说明:本版本用 Text(Pango 引擎)显示文字,不依赖 LaTeX。
     几何图形、坐标轴、函数曲线都不需要 LaTeX。
     若想显示漂亮的数学公式(MathTex),需另装 LaTeX。
"""
from manim import *


class PythagoreanTheorem(Scene):
    def construct(self):
        # 标题(用 Text,不用 MathTex,避免依赖 LaTeX)
        title = Text("勾股定理", font="Microsoft YaHei", color=YELLOW).to_edge(UP)
        formula = Text("a² + b² = c²", font="Microsoft YaHei").next_to(title, DOWN)
        self.play(Write(title))
        self.play(Write(formula))
        self.wait(0.5)

        # 画一个直角三角形(3-4-5)
        a, b = 3, 4
        p_right = ORIGIN + LEFT * 1.5 + DOWN * 1.5      # 直角顶点
        p_base = p_right + RIGHT * a                     # 底边端点
        p_top = p_right + UP * b                         # 高端点
        triangle = Polygon(p_right, p_base, p_top, color=WHITE, fill_opacity=0.3)

        self.play(Create(triangle))
        self.wait(0.3)

        # 直角标记
        right_angle = RightAngle(
            Line(p_right, p_base), Line(p_right, p_top), length=0.4, color=RED
        )
        self.play(Create(right_angle))

        # 标注三边
        label_a = Text("a=3", font="Microsoft YaHei").scale(0.6).next_to(
            Line(p_right, p_base), DOWN)
        label_b = Text("b=4", font="Microsoft YaHei").scale(0.6).next_to(
            Line(p_right, p_top), LEFT)
        label_c = Text("c=5", font="Microsoft YaHei").scale(0.6).next_to(
            Line(p_base, p_top).get_center(), UR, buff=0.1)
        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait(1)

        # 强调公式
        self.play(Indicate(formula, color=GREEN))
        self.wait(2)


class FunctionTransform(Scene):
    """函数图像变换:sin 变 cos(不依赖 LaTeX)"""
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={"color": BLUE},
        )
        sin_graph = axes.plot(lambda x: np.sin(x), color=YELLOW)
        cos_graph = axes.plot(lambda x: np.cos(x), color=GREEN)

        sin_label = Text("sin(x)", color=YELLOW).scale(0.7).to_corner(UL)
        cos_label = Text("cos(x)", color=GREEN).scale(0.7).to_corner(UL)

        self.play(Create(axes))
        self.play(Create(sin_graph), Write(sin_label))
        self.wait(1)
        self.play(
            Transform(sin_graph, cos_graph),
            Transform(sin_label, cos_label),
        )
        self.wait(2)
