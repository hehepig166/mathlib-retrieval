import sys
import os
# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from name_retrieval import NameRetrieval
from utils import sort_by_min_edit_distance

def extract_names_and_type_from_file(file_path):
    def process_line(line):
        line = line.strip()
        # 删除最后的 ':' 符号
        if line.endswith(':'):
            line = line[:-1]
        return line.strip()

    res = []
    with open(file_path, 'r', encoding='utf-8') as file:
        flag = 0
        """
        flag = 0 : 等待提取名字
        flag = 1 : 已经有名字，正在提取类型
        """
        name = ""
        type_str = ""
        for line in file:
            line = process_line(line)
            if flag == 0 and line != '':
                name = line
                flag = 1
            elif flag == 1:
                if line.strip() == '':
                    continue
                elif line.startswith('===='):
                    flag = 0
                    res.append({
                        "name": name,   
                        "type": type_str
                    })
                    name = ""
                    type_str = ""
                else:
                    type_str += line
    return res

def filter_by_depth(info_list, depth):
    """
    过滤出深度小于等于 depth 的名字，深度定义为名字中 '.' 的个数 + 1
    例如：
    "a.b.c" 的深度为 3
    "a.b" 的深度为 2
    "a" 的深度为 1
    """
    def get_depth(word):
        return word.count('.') + 1
    return [info for info in info_list if get_depth(info["name"]) <= depth]

def print_info(info, hint: str = ""):
    print(f"{info['name']} :\n{info['type']}")


def interactive_search(info_list):
    word_list = [info["name"] for info in info_list]
    name_to_info = {info["name"]: info for info in info_list}
    retrieval = NameRetrieval(word_list)
    max_results = 5
    while True:
        hint = """
        h                   : help 显示帮助
        setmr <max_results> : set_max_results 设置最大返回结果数
        w <word>            : word 搜索单词
        p <prefix>          : prefix 搜索前缀
        sstr <substring>    : substring 搜索子串，存在子串为特定词的列表
        sseq <subsequence>  : subsequence 搜索子序列，存在子序列为特定词的列表
        q                   : quit 退出"""
        query = input("\nEnter a query: ")
        parts = query.split()
        if len(parts) == 0:
            continue
        elif len(parts) == 1:
            op = parts[0]
            arg = ""
        else:
            op, arg = parts[0], " ".join(parts[1:])
        if op == "set_max_results" or op == "setmr":
            if not arg:
                print("Please provide a max_results")
                continue
            max_results = int(arg)
            print(f"set max_results to {max_results}")
            continue
        elif op == "word" or op == "w":
            results = retrieval.exists(arg)
        elif op == "prefix" or op == "p":
            results = retrieval.prefix_search(arg)
        elif op == "substring" or op == "sstr":
            results = retrieval.substring_search(arg)
        elif op == "subsequence" or op == "sseq":
            results = retrieval.subsequence_search(arg)
        elif op == "help" or op == "h":
            print(hint)
            continue
        elif op == "quit" or op == "q":
            break
        else:
            print("Invalid command")
            continue
        
        # 处理结果，根据max_results限制显示数量
        if isinstance(results, list):
            results = sort_by_min_edit_distance(results, arg)
            if len(results) > max_results:
                print(f"{len(results)} results (showing first {max_results}):")
            else:
                print(f"{len(results)} results:")
            for i, result in enumerate(results[:max_results]):
                info = name_to_info[result]
                print(f"\n------------------------------------[{i+1:^3}]--------")
                print_info(info)
        else:
            print(f"results: {results}")

if __name__ == "__main__":
    max_depth = 2
    fname = "./mathlib_examples.txt"
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    print(f"reading {fname}...")
    res = extract_names_and_type_from_file(fname)
    print(f"{len(res)} theorems extracted")
    res = filter_by_depth(res, max_depth)
    print(f"{len(res)} theorems filtered by max_depth {max_depth}")
    interactive_search(res)
    