"""バブルソートの Manim アニメーション。

実行（WSL 推奨。Windows の Python 3.14 では依存ビルド不可）:
    manim -pql scenes/bubble_sort.py BubbleSortScene

描画系の共通部品は SortSceneBase に集約してある。本ファイルは
バブルソート固有のループ手順だけを持つ。
"""

from manim import GREEN, YELLOW

from sort_scene_base import SortSceneBase

# 並べ替える対象。小さめにして 1 比較ずつ追えるようにする。
VALUES = [5, 2, 9, 1, 6, 3]


class BubbleSortScene(SortSceneBase):
    def construct(self) -> None:
        values = list(VALUES)
        bars = self._setup("Bubble Sort", values)

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
        self._finish(bars)
