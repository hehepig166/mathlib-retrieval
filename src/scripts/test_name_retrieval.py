import sys
import os
# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from name_retrieval import NameRetrieval


def test_name_retrieval():
    """测试名字检索系统的各种功能"""
    
    # 创建测试数据
    test_words = [
        "alice", "bob", "charlie", "david", "emma", "frank", "grace", "henry",
        "alex", "alexander", "alexandra", "alexis", "alexa", "alexander",
        "anna", "anne", "annie", "annabelle", "annabella",
        "michael", "michelle", "mike", "mikey", "michaela",
        "john", "johnny", "johnson", "johnathan", "johnathon",
        "sarah", "sara", "sarah", "sarah", "sarah",
        "james", "jamie", "jameson", "jamison", "james",
        "emily", "emma", "emma", "emma", "emma",
        "william", "will", "willy", "william", "william",
        "olivia", "olive", "olivia", "olivia", "olivia"
    ]
    
    # 初始化检索系统
    nr = NameRetrieval(test_words)
    
    print("=== 名字检索系统测试 ===\n")
    
    # 1. 测试存在性检查
    print("1. 存在性检查:")
    test_words_check = ["alice", "bob", "xyz", "alex"]
    for word in test_words_check:
        exists = nr.exists(word)
        print(f"   '{word}' 存在: {exists}")
    print()
    
    # 2. 测试前缀搜索
    print("2. 前缀搜索:")
    prefixes = ["al", "mi", "jo", "em"]
    for prefix in prefixes:
        results = nr.prefix_search(prefix)
        print(f"   前缀 '{prefix}': {results}")
    print()
    
    # 3. 测试子串搜索
    print("3. 子串搜索:")
    substrings = ["al", "mi", "jo", "em"]
    for substring in substrings:
        results = nr.substring_search(substring)
        print(f"   包含子串 '{substring}': {results}")
    print()
    
    # 4. 测试子序列搜索
    print("4. 子序列搜索:")
    subsequences = ["al", "mi", "jo", "em"]
    for subsequence in subsequences:
        results = nr.subsequence_search(subsequence)
        print(f"   包含子序列 '{subsequence}': {results}")
    print()
    
    # 5. 测试自定义过滤
    print("5. 自定义过滤:")
    
    # 过滤长度为4的单词
    length_4_filter = lambda word: len(word) == 4
    results = nr.filter_search(length_4_filter)
    print(f"   长度为4的单词: {results}")
    
    # 过滤以'a'开头的单词
    starts_with_a_filter = lambda word: word.startswith('a')
    results = nr.filter_search(starts_with_a_filter)
    print(f"   以'a'开头的单词: {results}")
    
    # 过滤包含'e'的单词
    contains_e_filter = lambda word: 'e' in word
    results = nr.filter_search(contains_e_filter)
    print(f"   包含'e'的单词: {results}")
    print()
    
    # 6. 显示统计信息
    print("6. 统计信息:")
    print(f"   总单词数: {nr.get_word_count()}")
    print(f"   所有单词: {nr.get_all_words()[:10]}... (显示前10个)")


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 边界情况测试 ===\n")
    
    # 空列表测试
    empty_nr = NameRetrieval([])
    print("空列表测试:")
    print(f"   单词数: {empty_nr.get_word_count()}")
    print(f"   搜索'abc': {empty_nr.exists('abc')}")
    print(f"   前缀搜索'a': {empty_nr.prefix_search('a')}")
    print()
    
    # 单个单词测试
    single_nr = NameRetrieval(["hello"])
    print("单个单词测试:")
    print(f"   单词数: {single_nr.get_word_count()}")
    print(f"   搜索'hello': {single_nr.exists('hello')}")
    print(f"   搜索'world': {single_nr.exists('world')}")
    print(f"   前缀搜索'he': {single_nr.prefix_search('he')}")
    print(f"   子串搜索'll': {single_nr.substring_search('ll')}")
    print()
    
    # 重复单词测试
    duplicate_nr = NameRetrieval(["hello", "hello", "world", "world"])
    print("重复单词测试:")
    print(f"   单词数: {duplicate_nr.get_word_count()}")
    print(f"   所有单词: {duplicate_nr.get_all_words()}")


if __name__ == "__main__":
    test_name_retrieval()
    test_edge_cases() 