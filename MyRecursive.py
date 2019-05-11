# -*- coding: utf-8 -*-
"""
Created on Fri May 10 17:15:05 2019

微信公众号: Python高效编程
"""
import doctest
currency = {1, 2, 5, 10}
value = 12




# 给定总和，确定排列方式
def equal(currency:set, value:int, *,dup:bool=False)->list:
    '''
    >>> currency = {1, 2, 5, 10}
    >>> value = 12
    >>> len(equal(currency, value))
    377
    >>> len(equal(currency, value, dup=True))
    11
    '''
    # 初始值
    num = 0
    sub_list = []   
    total_list = []
    # 不考虑次序
    if dup:
        unique_set = set()
    # 闭包
    def _equal(num:int, sub_list:list):
        # 停止条件 1
        # 当前总和等于给定值
        if num == value:
            return sub_list       
        
        for elem in currency:
            # 当前总和
            total_num = num + elem
            # 子列表增加元素
            sub_list.append(elem)
            # 停止条件 2
            # 当前总和大于给定值
            if num > value:
                return []
            # 副本
            result = _equal(total_num, sub_list.copy())
            # 去重模式
            # 若排序长度相同，则为重复值
            if dup:
                length = len(result)
                if length not in unique_set:
                    unique_set.add(length)
                else:
                    result = []
                    
            # 如果返回值不为空
            # 将结果保存至列表中
            if result:
                total_list.append(result)
            # 子列表删除这个元素
            sub_list.pop()
          
        return []

   
    _equal(num=num, sub_list=sub_list)
    return total_list



if __name__ == '__main__':
    doctest.testmod()

