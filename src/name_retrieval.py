from typing import List, Callable, Optional
from utils import is_subsequence


class NameRetrieval:
    """
    名字检索系统 - 基于简单列表实现
    提供多种搜索功能：存在性检查、前缀搜索、子串搜索、子序列搜索和自定义过滤
    """
    
    def __init__(self, word_list: List[str]):
        """
        初始化检索系统
        
        Args:
            word_list: 要索引的单词列表
        """
        self.words = word_list.copy()  # 创建副本避免外部修改影响内部数据
    
    def exists(self, word: str) -> bool:
        """
        检查某个单词是否存在
        
        Args:
            word: 要检查的单词
            
        Returns:
            bool: 单词是否存在
        """
        return word in self.words
    
    def prefix_search(self, prefix: str) -> List[str]:
        """
        搜索前缀为特定词的列表
        
        Args:
            prefix: 要搜索的前缀
            
        Returns:
            List[str]: 匹配前缀的单词列表
        """
        results = []
        for word in self.words:
            if word.startswith(prefix):
                results.append(word)
        return results
    
    def substring_search(self, substring: str) -> List[str]:
        """
        搜索存在子串为特定词的列表
        
        Args:
            substring: 要搜索的子串
            
        Returns:
            List[str]: 包含指定子串的单词列表
        """
        results = []
        for word in self.words:
            if substring in word:
                results.append(word)
        return results
    
    def subsequence_search(self, subsequence: str) -> List[str]:
        """
        搜索存在子序列为特定词的列表
        子序列是指在不改变字符相对顺序的情况下，删除某些字符后得到的序列
        
        Args:
            subsequence: 要搜索的子序列
            
        Returns:
            List[str]: 包含指定子序列的单词列表
        """
        results = []
        for word in self.words:
            if is_subsequence(subsequence, word):
                results.append(word)
        return results
    
    def filter_search(self, filter_func: Callable[[str], bool]) -> List[str]:
        """
        通过特定 filter 函数剩下的列表
        
        Args:
            filter_func: 过滤函数，接受一个字符串参数，返回布尔值
            
        Returns:
            List[str]: 通过过滤函数的单词列表
        """
        results = []
        for word in self.words:
            if filter_func(word):
                results.append(word)
        return results
    
    def get_all_words(self) -> List[str]:
        """
        获取所有单词列表
        
        Returns:
            List[str]: 所有单词的列表
        """
        return self.words.copy()
    
    def get_word_count(self) -> int:
        """
        获取单词总数
        
        Returns:
            int: 单词总数
        """
        return len(self.words) 