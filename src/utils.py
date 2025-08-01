from typing import List
import Levenshtein

#================= 字符串相关 =================

def is_subsequence(subsequence: str, word: str) -> bool:
    """
    检查 subsequence 是否是 word 的子序列
    
    Args:
        subsequence: 子序列
        word: 原单词
        
    Returns:
        bool: 是否为子序列
    """
    if not subsequence:
        return True
    
    i = 0  # subsequence 的索引
    for char in word:
        if i < len(subsequence) and char == subsequence[i]:
            i += 1
            if i == len(subsequence):
                return True
    return False

def min_edit_distance(word1: str, word2: str) -> int:
    """
    计算两个单词之间的最小编辑距离
    """
    return Levenshtein.distance(word1, word2)

def sort_by_min_edit_distance(word_list: List[str], word: str) -> List[str]:
    """
    根据最小编辑距离排序

    Args:
        word_list: 单词列表
        word: 目标单词

    Returns:
        List[str]: 排序后的单词列表
    """
    return sorted(word_list, key=lambda x: Levenshtein.distance(x, word))