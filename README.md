# animate-algorithms

典型アルゴリズムを **mermaid でデータフロー可視化** し、**Manim でアニメーション**して、
「動きで理解する」ことで認知負債を軽減するためのプロジェクト。

対象とする「典型アルゴリズム」:

- CodinGame / AtCoder の Algorithm・Heuristic でよく使われるもの
- 次点で CTF・ソフトウェア開発でよく使われるもの

## ディレクトリ構成

| ディレクトリ | 役割 |
|------------|------|
| `research/` | どんなアルゴリズムがあるかの調査・難易度別の整理 |
| `summary/`  | 実装完了時の概要（認知負債の軽減） |
| `knowledge/`| つまずきポイントとその解説 |
| `docs/`     | 各アルゴリズムの mermaid データフロー図 |
| `scenes/`   | Manim アニメーションのシーン (Python) |

## 技術

- [Manim Community](https://www.manim.community/) — 数学アニメーション
- mermaid — 静的データフロー図
- GitHub / git / `gh`

## セットアップ

```bash
python -m pip install -r requirements.txt
# 動画レンダリングに ffmpeg が必要（Manim 0.18+ は pyav 同梱のことが多い）
manim -pql scenes/bubble_sort.py BubbleSortScene
```
