# バブルソート — データフロー可視化

## 概要

隣り合う 2 要素を比較し、順序が逆なら交換する。これを配列の端から繰り返すと、
大きい要素が泡（bubble）のように後ろへ上がっていく。

- 計算量: 平均・最悪 `O(n^2)`、最良 `O(n)`（最適化版・交換が無ければ早期終了）
- 安定ソート / in-place（追加メモリ `O(1)`）

## 制御フロー

```mermaid
flowchart TD
    Start([開始]) --> Init["i = 0"]
    Init --> OuterCond{"i < n-1 ?"}
    OuterCond -- いいえ --> Done([整列完了])
    OuterCond -- はい --> InitJ["j = 0, swapped = false"]
    InitJ --> InnerCond{"j < n-1-i ?"}
    InnerCond -- いいえ --> CheckSwap{"swapped ?"}
    InnerCond -- はい --> Compare{"a[j] > a[j+1] ?"}
    Compare -- はい --> Swap["a[j] ↔ a[j+1]<br/>swapped = true"]
    Compare -- いいえ --> NextJ["j++"]
    Swap --> NextJ
    NextJ --> InnerCond
    CheckSwap -- いいえ（交換なし）--> Done
    CheckSwap -- はい --> NextI["i++"]
    NextI --> OuterCond
```

## データフロー（1 パスで起きること）

```mermaid
graph LR
    subgraph Pass["1 パス: 隣接比較を左から右へ"]
        direction LR
        c0["a[0]:a[1]"] --> c1["a[1]:a[2]"] --> c2["a[2]:a[3]"] --> cN["...:a[n-1]"]
    end
    Pass --> R["この回の最大値が<br/>右端に確定"]
    R --> Next["未確定範囲が 1 縮む"]
```

## 可視化の勘所（Manim でアニメ化する点）

1. **比較中の 2 本のバー**をハイライト（色を変える）
2. **交換**はバーの位置を入れ替えるトランジション
3. **確定済み**の末尾要素は色を固定（もう動かない印）
4. **早期終了**: 1 パスで交換が無ければ「完了」表示

→ 実装は `scenes/bubble_sort.py`（Issue #2）。
