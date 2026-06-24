"""バブルソートの Manim アニメーション。

実行（WSL 推奨。Windows の Python 3.14 では依存ビルド不可）:
    manim -pql scenes/bubble_sort.py BubbleSortScene

Manim 用語メモ:
- Scene.construct() … 1 本のアニメーションの本体。ここに描く手順を書く。
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
    YELLOW,
    Create,
    Rectangle,
    Scene,
    Text,
    VGroup,
)

# 並べ替える対象。小さめにして 1 比較ずつ追えるようにする。
VALUES = [5, 2, 9, 1, 6, 3]

BAR_WIDTH = 0.8
BAR_GAP = 0.25
UNIT_HEIGHT = 0.5  # 値 1 あたりのバーの高さ


class BubbleSortScene(Scene):
    def construct(self) -> None:
        title = Text("Bubble Sort", font_size=40).to_edge(UP)
        self.add(title)

        values = list(VALUES)
        bars = self._build_bars(values)
        self.play(Create(bars))
        self.wait(0.5)

        n = len(values)
        for i in range(n - 1):
            swapped = False
            # 末尾 i 個は確定済みなので比較しない
            for j in range(n - 1 - i):
                self._highlight_pair(bars, j, j + 1, YELLOW)

                if values[j] > values[j + 1]:
                    # 値とバーの両方を入れ替える
                    values[j], values[j + 1] = values[j + 1], values[j]
                    self._swap_bars(bars, j, j + 1)
                    swapped = True

                self._reset_pair(bars, j, j + 1)

            # この回で右端に上がった最大値を「確定」色にする
            bars[n - 1 - i].set_color(GREEN)

            if not swapped:  # 1 パスで交換ゼロ＝既に整列済み（早期終了）
                break

        # 残り（先頭側）も全部確定色にして終了
        for bar in bars:
            bar.set_color(GREEN)
        self.wait(1)

    # --- 以下、再利用を見据えた部品 -------------------------------------

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
