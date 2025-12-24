# %%
from bibtex_converter import *

def get_my_cnki_ref(my_ref: str): 
    targets = [cnki_str_to_bibtex(ref) for ref in my_ref.strip().split('\n')]
    for target in targets:
        print(target)
        print('\n')

# %%
my_ref = """
倪中新,郭婧,王琳玉.上证50ETF期权隐含波动率微笑形态的风险信息容量研究[J].财经研究,2020,46(04):155-169.DOI:10.16538/j.cnki.jfe.2020.04.011.
曾伟,陈平.波动率微笑、相对偏差和交易策略——基于非线性生灭过程的股价波动一般扩散模型[J].经济学(季刊),2008,(04):1415-1436.DOI:10.13821/j.cnki.ceq.2008.04.018.
杨霭.基于随机波动模型的50ETF期权定价和波动率微笑研究[D].西南财经大学,2016.
"""
get_my_cnki_ref(my_ref)


# %%
