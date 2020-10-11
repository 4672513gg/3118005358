# 命令行参数定义
from argparse import ArgumentParser


def arg_parse():
    parser = ArgumentParser()
    parser.add_argument('-n', nargs=1, type=int, help='输入并获取生成的题目数量')
    parser.add_argument('-r', nargs=1, type=int, help='输入并获取参与运算的最大值')
    parser.add_argument('-e', nargs=1, type=str, help='选择题目文件')
    parser.add_argument('-a', nargs=1, type=str, help='选择答案文件')
    parser.add_argument('-g', help= '启动图形化界面')
    parser.add_argument('-c', nargs=1, type=str, help='输出检查的结果')
    parser.add_argument('-f', nargs=1, type=str, help='命令行界面运行时，"f" 后跟生成试题的份数')
    args = parser.parse_args()
    return args
