# Manim を Windows + WSL で動かす（つまずき解説）

## 何が問題だったか

Windows のグローバル Python (3.14.6) で `pip install manim` すると失敗した。

- `moderngl` / `glcontext` … 3.14 用のビルド済み wheel が無く、ソースビルドに
  C コンパイラが要る → Windows に gcc が無くて失敗
- （仮に通っても）動画書き出しに `ffmpeg` が要るが Windows に無い

## なぜ WSL なのか

WSL (Ubuntu) は次がそろっていて、Manim の前提を満たしやすい。

- Python 3.12（moderngl などの wheel がある安定版）
- `gcc` 13、`ffmpeg` 6.1 が標準で使える
- ただし **cairo / pango の開発ライブラリは別途必要**（pycairo のビルドに使う）

> 用語: **cairo** は 2D 描画ライブラリ、**pango** は文字組版ライブラリ。
> Manim は内部でこれらを使って図形と文字を描くので、開発用ヘッダ（`-dev`）が要る。

## 手順（再現用）

```bash
# 1. system 依存（sudo パスワードが要る）
wsl -e bash -lc "sudo apt-get update && \
  sudo apt-get install -y libcairo2-dev libpango1.0-dev pkg-config build-essential"

# 2. Manim 本体（pipx で CLI を隔離インストール）
wsl -e bash -lc 'pipx install manim'

# 3. 実行（pipx の bin は ~/.local/bin。PATH に無ければフルパスで）
wsl -e bash -lc 'cd /mnt/c/Users/moai0/git/animate-algorithms && \
  ~/.local/bin/manim -ql scenes/bubble_sort.py BubbleSortScene'
```

> 用語: **pipx** は「CLI ツールを専用の仮想環境に隔離して入れる」道具。
> 通常の `pip install` と違い、依存が他プロジェクトと混ざらない。

## ポイント

- プロジェクトは Windows 側 `C:\...` に置いたまま、WSL から `/mnt/c/...` で触れる
- 出力 `media/` は `.gitignore` 済み（動画はコミットしない）
- 画質オプション: `-ql`(低/速) `-qm` `-qh`(高) / `-p` で再生 / `--disable_caching`
