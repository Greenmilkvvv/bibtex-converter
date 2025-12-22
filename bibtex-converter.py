# %%
import re


# %%
def cnki_str_to_bibtex(cnki_str, cite_key=None):
    """
    将知网引用字符串一键转换为BibTeX
    
    参数:
    cnki_str: str - 知网格式的引用字符串，例如：
        "张三，李四，王五. 文章标题[J]. 期刊名, 2023, 46(5): 100-115."
    cite_key: str - 指定的引用标签，如不指定则自动生成
    
    返回:
    str - BibTeX格式字符串
    """
    
    # 预处理：去除多余空格和换行
    text = re.sub(r'\s+', ' ', cnki_str.strip())
    
    # 1. 提取作者
    # 模式：作者部分以"."或"。"结束
    author_match = re.match(r'^([^。]+?)[。\.]\s*', text)
    if author_match:
        authors_raw = author_match.group(1).strip()
        # 处理多种分隔符：，、;和空格
        authors_list = re.split(r'[，、;,]\s*', authors_raw)
        authors = " and ".join([f"{{{author.strip()}}}" for author in authors_list if author.strip()])
        # 剩余文本
        remaining = text[author_match.end():]
    else:
        authors = "{Unknown}"
        remaining = text
    
    # 2. 提取标题 (直到[J]或[J].)
    title_match = re.search(r'^(.*?)\[J\](?:\.|,\s*|$)', remaining)
    if title_match:
        title = title_match.group(1).strip()
        remaining = remaining[title_match.end():]
    else:
        # 如果没有[J]，则取到第一个逗号或句号
        title_match = re.search(r'^([^,。]+)', remaining)
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        remaining = remaining[title_match.end():] if title_match else remaining
    
    # 3. 提取期刊名
    # 模式：期刊名后跟逗号和年份
    journal_match = re.search(r'^([^,]+?)\s*,\s*(\d{4})', remaining)
    if journal_match:
        journal = journal_match.group(1).strip()
        year = journal_match.group(2)
        remaining = remaining[journal_match.end():]
    else:
        journal = "Unknown Journal"
        # 尝试从文本中提取年份
        year_match = re.search(r'\b(\d{4})\b', remaining)
        year = year_match.group(1) if year_match else "2024"
    
    # 4. 提取卷号、期号和页码
    volume = None
    issue = None
    pages = None
    
    # 模式：卷(期): 页码
    vol_issue_match = re.search(r'(\d+)\s*\((\d+)\)\s*:\s*(\d+(?:-\d+)?)', remaining)
    if vol_issue_match:
        volume = vol_issue_match.group(1)
        issue = vol_issue_match.group(2)
        pages = vol_issue_match.group(3)
    else:
        # 尝试其他格式
        pages_match = re.search(r'[:：]\s*(\d+(?:-\d+)?)', remaining)
        if pages_match:
            pages = pages_match.group(1)
    
    # 5. 生成或使用指定的cite_key
    if cite_key is None:
        # 自动生成cite_key: 第一作者姓氏 + 年份 + 标题前两个字的拼音首字母
        first_author = authors_list[0] if len(authors_list) > 0 else "unknown"
        if ' ' in first_author:
            last_name = first_author.split()[-1]
        else:
            last_name = first_author
        
        # 简单提取标题前两个汉字的首字母
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', title)
        if len(chinese_chars) >= 2:
            initials = chinese_chars[0] + chinese_chars[1]
        else:
            initials = title[:2] if len(title) >= 2 else "xx"
        
        cite_key = f"{last_name}{year}{initials}".lower()
        # 移除特殊字符
        cite_key = re.sub(r'[^\w]', '', cite_key)
    
    # 6. 构建BibTeX
    bibtex_lines = [
        f"@article{{{cite_key},",
        f"  author    = {authors},",
        f"  title     = {{{title}}},",
        f"  journal   = {{{journal}}},",
        f"  year      = {{{year}}},"
    ]
    
    if volume:
        bibtex_lines.append(f"  volume    = {{{volume}}},")
    if issue:
        bibtex_lines.append(f"  number    = {{{issue}}},")
    if pages:
        bibtex_lines.append(f"  pages     = {{{pages}}},")
    
    bibtex_lines.append("  language  = {chinese}")
    bibtex_lines.append("}")
    
    return "\n".join(bibtex_lines)


# %%
# 使用示例
if __name__ == "__main__":
    # 测试用例1：标准格式
    cnki_ref1 = "张三，李四，王五. 深度学习在自然语言处理中的应用研究[J]. 计算机学报, 2023, 46(5): 100-115."
    
    # 测试用例2：不同分隔符
    cnki_ref2 = "王小明; 李华. 人工智能发展趋势分析[J]. 科技导报, 2022, 40(10): 25-30."
    
    # 测试用例3：简单格式
    cnki_ref3 = "赵六. 大数据技术综述. 信息技术, 2021: 45-50."
    
    test_cases = [
        (cnki_ref1, None),
        (cnki_ref2, "wang2022ai"),
        (cnki_ref3, None)
    ]
    
    for cnki_str, key in test_cases:
        print("="*60)
        print("输入:", cnki_str[:50] + "..." if len(cnki_str) > 50 else cnki_str)
        print("输出:")
        print(cnki_str_to_bibtex(cnki_str, key))
        print()