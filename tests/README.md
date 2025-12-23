# テスト仕様書

## 概要
このディレクトリには、`src/function_app.py`の単体テストが含まれています。

## テストフレームワーク
- Python標準の`unittest`を使用
- GitHub ActionsでCI/CD実行
- カバレッジ目標: **80%以上**

## テスト実行方法

### ローカル環境での実行
```bash
# 全テストを実行
python -m unittest discover -s tests -p "test_*.py" -v

# カバレッジ付きで実行
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report --include="src/*" -m
coverage html --include="src/*"
```

### GitHub Actions
- push/PRイベントで自動実行
- カバレッジレポートをアーティファクトとして保存
- 80%以上のカバレッジを要求

## テストケース一覧

### TestMultiply クラス (13テスト)

#### 正常系
- `test_multiply_ok`: 正の整数同士の乗算 (3 × 4 = 12)
- `test_multiply_zero_by_number`: ゼロ × 正数 (0 × 5 = 0)
- `test_multiply_number_by_zero`: 正数 × ゼロ (5 × 0 = 0)
- `test_multiply_negative_positive`: 負数 × 正数 (-3 × 4 = -12)
- `test_multiply_positive_negative`: 正数 × 負数 (3 × -4 = -12)
- `test_multiply_negative_negative`: 負数 × 負数 (-3 × -4 = 12)
- `test_multiply_large_numbers`: 大きな数値 (1000 × 2000 = 2000000)

#### 異常系（パラメータ欠損）
- `test_multiply_missing_a`: パラメータAが欠損
- `test_multiply_missing_b`: パラメータBが欠損
- `test_multiply_both_missing`: 両パラメータが欠損

#### 異常系（無効な入力）
- `test_multiply_invalid_a`: パラメータAが非整数 ("y")
- `test_multiply_invalid_b`: パラメータBが非整数 ("x")
- `test_multiply_empty_string_a`: パラメータAが空文字列
- `test_multiply_float_string`: パラメータAが浮動小数点文字列 ("3.5")

### TestDivide クラス (18テスト)

#### 正常系
- `test_divide_ok_trunc_toward_zero_pos`: 正数の除算・ゼロへの切り捨て (7 ÷ 2 = 3)
- `test_divide_ok_trunc_toward_zero_neg`: 負数の除算・ゼロへの切り捨て (-7 ÷ 2 = -3)
- `test_divide_negative_by_negative`: 負数 ÷ 負数 (-8 ÷ -2 = 4)
- `test_divide_positive_by_negative`: 正数 ÷ 負数 (7 ÷ -2 = -3)
- `test_divide_exact_division`: 完全除算 (10 ÷ 5 = 2)
- `test_divide_zero_by_number`: ゼロ ÷ 正数 (0 ÷ 5 = 0)
- `test_divide_negative_trunc_toward_zero`: 負数のゼロへの切り捨て (-10 ÷ 3 = -3)
- `test_divide_large_numbers`: 大きな数値 (1000000 ÷ 3 = 333333)

#### 異常系（パラメータ欠損）
- `test_divide_missing_a`: パラメータAが欠損
- `test_divide_missing_b`: パラメータBが欠損
- `test_divide_both_missing`: 両パラメータが欠損

#### 異常系（無効な入力）
- `test_divide_invalid_a`: パラメータAが非整数 ("abc")
- `test_divide_invalid_b`: パラメータBが非整数 ("xyz")
- `test_divide_empty_string_b`: パラメータBが空文字列
- `test_divide_float_string`: パラメータAが浮動小数点文字列 ("7.5")

#### 異常系（ゼロ除算）
- `test_divide_by_zero`: 正数 ÷ ゼロ (7 ÷ 0)
- `test_divide_zero_by_zero`: ゼロ ÷ ゼロ (0 ÷ 0)

## カバレッジ詳細

全31テストケースで以下をカバー:
- ✅ multiply エンドポイント: パラメータ検証、四則演算（正数・負数・ゼロ）
- ✅ divide エンドポイント: パラメータ検証、ゼロ除算、ゼロへの切り捨て
- ✅ _get_required_int_query: 欠損・型変換エラー（エンドポイント経由）
- ✅ _error: エラーレスポンス形式（エンドポイント経由）
- ✅ _trunc_div: 符号の組み合わせ、切り捨て方向（エンドポイント経由）

## エラーメッセージ形式
全エラーは以下の形式で返されます:
- HTTP ステータス: 200
- Content-Type: text/plain; charset=utf-8
- Body: `ERROR: <理由>`

例:
- `ERROR: Missing query parameter A`
- `ERROR: Query parameter B must be an integer`
- `ERROR: Division by zero`
