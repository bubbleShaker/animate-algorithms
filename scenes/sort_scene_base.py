"""ソート系アニメーションの共通基底クラス。

bubble_sort / shaker_sort など「バーを並べて比較・交換していく」系の
シーンで共通する部品をここに集約する（Template Method パターン）。
子クラスは construct() でソートのループ本体だけを実装すればよい。

Manim 用語メモ:
- Scene.construct() … 1 本のアニメーションの本体。子クラスで実装する。
- Mobject (Mathematical Object) … 画面に置ける図形・文字。Rectangle や Text など。
- VGroup … 複数 Mobject を 1 つにまとめて一括操作するための入れ物。
- self.play(...) … 中の Animation を実際に再生する（1 回が 1 カット）。
- mobject.animate.xxx … 「xxx した状態への変化」をアニメーションとして生成する糖衣構文。
"""

from manim import (
    BLUE,
    DOWN,
    GREEN,
    RED,
    UP,
    WHITE,
    Create,
    Rectangle,
    Scene,
    Text,
    VGroup,
)

BAR_WIDTH = 0.8
BAR_GAP = 0.25
UNIT_HEIGHT = 0.5  # 値 1 あたりのバーの高さ


class SortSceneBase(Scene):
    """バー可視化ソートの共通部品を持つ基底クラス。

    子クラスは `title`（表示名）と `values`（並べ替える値）を用意し、
    construct() でソート手順を書く。描画系の部品は本クラスが提供する。
    """

    # --- 子クラスから使う「お膳立て」 ---------------------------------

    def _setup(self, title_text: str, values: list[int]) -> VGroup:
        """タイトルを置き、バーを生成・描画して VGroup を返す共通の導入部。"""
        title = Text(title_text, font_size=40).to_edge(UP)
        self.add(title)
        bars = self._build_bars(values)
        self.play(Create(bars))
        self.wait(0.5)
        return bars

    def _finish(self, bars: VGroup) -> None:
        """全バーを確定色(GREEN)にして終わる共通の締め。"""
        for bar in bars:
            bar.set_color(GREEN)
        self.wait(1)

    # --- 描画部品 -----------------------------------------------------

    def _build_bars(self, values: list[int]) -> VGroup:
        """値リストからバー（Rectangle）の VGroup を作って中央に並べる。"""
        bars = VGroup()
        for v in values:
            bar = Rectangle(
                width=BAR_WIDTH,
                height=v * UNIT_HEIGHT,
                fill_color=BLUE,
                fill_opacity=1.0,
                stroke_color=WHITE,
            )
            bars.add(bar)
        # 横一列に等間隔で並べ、下端を揃える
        bars.arrange(buff=BAR_GAP, aligned_edge=DOWN)
        bars.to_edge(DOWN, buff=1.0)
        return bars

    def _highlight_pair(self, bars: VGroup, a: int, b: int, color) -> None:
        self.play(
            bars[a].animate.set_color(color),
            bars[b].animate.set_color(color),
            run_time=0.3,
        )

    def _reset_pair(self, bars: VGroup, a: int, b: int) -> None:
        # 確定済み（GREEN）のバーは戻さない
        for idx in (a, b):
            if bars[idx].get_color() != GREEN:
                bars[idx].set_color(BLUE)

    def _swap_bars(self, bars: VGroup, a: int, b: int) -> None:
        """バー a と b を、見た目の位置ごと入れ替える。

        高さが異なるバー同士なので、中心ごと動かすと下端（ベースライン）が
        ズレてしまう。バーは底辺を揃えて並べてあるため、入れ替えるのは
        横位置 (x) だけにして、各バーの下端は固定したままにする。
        """
        x_a = bars[a].get_x()
        x_b = bars[b].get_x()
        self.play(
            bars[a].animate.set_color(RED).set_x(x_b),
            bars[b].animate.set_color(RED).set_x(x_a),
            run_time=0.5,
        )
        # VGroup 内のインデックスと描画順を実データと一致させる
        bars.submobjects[a], bars.submobjects[b] = (
            bars.submobjects[b],
            bars.submobjects[a],
        )
