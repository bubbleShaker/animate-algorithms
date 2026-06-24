"""シェーカーソート（カクテルソート / 双方向バブルソート）の Manim アニメーション。

実行（WSL 推奨。Windows の Python 3.14 では依存ビルド不可）:
    manim -pql scenes/shaker_sort.py ShakerSortScene

バブルソートが「左→右」の一方向走査を繰り返すのに対し、シェーカーソートは
「左→右で最大を右端へ」「右→左で最小を左端へ」と往復する。両端から確定領域が
広がっていく。描画系の共通部品は SortSceneBase に集約してある。
"""

from manim import GREEN, YELLOW

from sort_scene_base import SortSceneBase

# 往復が活きるよう、最小値(1)を末尾近く、最大値(9)を先頭近くに置いた並び。
VALUES = [8, 3, 6, 1, 7, 2, 9, 4]


class ShakerSortScene(SortSceneBase):
    def construct(self) -> None:
        values = list(VALUES)
        bars = self._setup("Shaker Sort", values)

        lo, hi = 0, len(values) - 1
        while lo < hi:
            # --- 左→右: 最大値を右端 hi へ押し上げる ---
            swapped = False
            for j in range(lo, hi):
                self._highlight_pair(bars, j, j + 1, YELLOW)
                if values[j] > values[j + 1]:
                    values[j], values[j + 1] = values[j + 1], values[j]
                    self._swap_bars(bars, j, j + 1)
                    swapped = True
                self._reset_pair(bars, j, j + 1)
            bars[hi].set_color(GREEN)  # 右端の最大値を確定
            hi -= 1
            if not swapped:  # 交換ゼロ＝整列済み（早期終了）
                break

            # --- 右→左: 最小値を左端 lo へ押し下げる ---
            swapped = False
            for j in range(hi, lo, -1):
                self._highlight_pair(bars, j - 1, j, YELLOW)
                if values[j - 1] > values[j]:
                    values[j - 1], values[j] = values[j], values[j - 1]
                    self._swap_bars(bars, j - 1, j)
                    swapped = True
                self._reset_pair(bars, j - 1, j)
            bars[lo].set_color(GREEN)  # 左端の最小値を確定
            lo += 1
            if not swapped:
                break

        # 残り（中央付近）も全部確定色にして終了
        self._finish(bars)
