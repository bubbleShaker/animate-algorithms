# サマリ: バブルソート MVP (Issue #2)

## やったこと

mermaid + Manim のパイプラインを、バブルソートを題材に最後まで通した。

- `docs/bubble-sort.md` — 制御フロー / データフローの mermaid 図
- `scenes/bubble_sort.py` — Manim アニメーション
  - 黄 = 比較中、赤 = 交換中、青 = 未確定、緑 = 確定済み
  - 早期終了（1 パスで交換ゼロなら完了）も実装
- `manim -ql` で `BubbleSortScene.mp4` のレンダリングを確認済み

## 設計メモ

再利用を見据え、シーンを部品に分割した。

| 関数 | 役割 |
|------|------|
| `_build_bars` | 値リスト → バー(Rectangle)の VGroup |
| `_highlight_pair` | 比較中ペアを色付け |
| `_swap_bars` | バーを位置ごと入れ替え、内部順序も同期 |
| `_reset_pair` | 比較後に色を戻す（確定済みは除外）|

次のアルゴリズム（二分探索・BFS 等）に進むとき、`_build_bars` や比較ハイライトは
共通モジュールへ切り出す候補。

## 実行環境（重要）

Windows のグローバル Python (3.14) では Manim の依存（moderngl/pycairo）が
ビルドできず **WSL で動かす**。詳細は `knowledge/manim-setup-windows-wsl.md`。

```bash
wsl -e bash -lc 'cd /mnt/c/Users/moai0/git/animate-algorithms && \
  ~/.local/bin/manim -ql scenes/bubble_sort.py BubbleSortScene'
```

## 次の一歩

- ロードマップ（`research/algorithm-catalog.md`）に従い **二分探索** へ
- 共通 Manim 部品の切り出しを検討
