```sh
python .\src\scripts\test_mathlib_nameretrieval.py .\data\all\found_theorems_without_prefix_229064.txt
```

```
reading .\data\all\found_theorems_without_prefix_229064.txt...
229064 theorems extracted
162867 theorems filtered by max_depth 2

Enter a query: h

        h                   : help 显示帮助
        setmr <max_results> : set_max_results 设置最大返回结果数
        w <word>            : word 搜索单词
        p <prefix>          : prefix 搜索前缀
        sstr <substring>    : substring 搜索子串，存在子串为特定词的列表
        sseq <subsequence>  : subsequence 搜索子序列，存在子序列为特定词的列表
        q                   : quit 退出

Enter a query: sseq Finset.sumrange
29 results (showing first 5):

------------------------------------[ 1 ]--------
Finset.sum_range :
∀ {M : Type u_2} [inst : AddCommMonoid M] {n : ℕ} (f : ℕ → M), ∑ i ∈ Finset.range n, f i = ∑ i, f ↑i

------------------------------------[ 2 ]--------
Finset.sum_range_id :
∀ (n : ℕ), ∑ i ∈ Finset.range n, i = n * (n - 1) / 2

------------------------------------[ 3 ]--------
Finset.sum_range_one :
∀ {M : Type u_4} [inst : AddCommMonoid M] (f : ℕ → M), ∑ k ∈ Finset.range 1, f k = f 0

------------------------------------[ 4 ]--------
Finset.sum_range_sub :
∀ {G : Type u_3} [inst : AddCommGroup G] (f : ℕ → G) (n : ℕ), ∑ i ∈ Finset.range n, (f (i + 1) - f i) = f n - f 0

------------------------------------[ 5 ]--------
Finset.sum_range_add :
∀ {M : Type u_4} [inst : AddCommMonoid M] (f : ℕ → M) (n m : ℕ),∑ x ∈ Finset.range (n + m), f x = ∑ x ∈ Finset.range n, f x + ∑ x ∈ Finset.range m, f (n + x)

Enter a query: sseq Nat.primeiff
46 results (showing first 5):

------------------------------------[ 1 ]--------
Nat.prime_iff :
∀ {p : ℕ}, Nat.Prime p ↔ Prime p

------------------------------------[ 2 ]--------
Nat.isCoprime_iff :
∀ {m n : ℕ}, IsCoprime m n ↔ m = 1 ∨ n = 1

------------------------------------[ 3 ]--------
Nat.prime_mul_iff :
∀ {a b : ℕ}, Nat.Prime (a * b) ↔ Nat.Prime a ∧ b = 1 ∨ Nat.Prime b ∧ a = 1

------------------------------------[ 4 ]--------
PNat.isCoprime_iff :
∀ {m n : ℕ+}, IsCoprime ↑m ↑n ↔ m = 1 ∨ n = 1

------------------------------------[ 5 ]--------
Nat.minFac_prime_iff :
∀ {n : ℕ}, Nat.Prime n.minFac ↔ n ≠ 1

Enter a query: q
```