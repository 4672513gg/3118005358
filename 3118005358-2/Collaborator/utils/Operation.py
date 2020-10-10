# OS操作, 传入表达式/答案/正确率保存到文件

import os
from utils.Calculate import *
from re import split

flag=0
# 文件保存位置

if not os.path.exists('./docs'):
    os.mkdir('./docs')

# 检查
def inspect(answer_file, expression_file):
    # 正确错误列表序号
    correct_seq = []
    wrong_seq = []

    try:
        # 读取文件
        with open(expression_file, 'r', encoding='utf-8') as fa:
            expression_content = fa.readlines()
        # 读取文件
        with open(answer_file, 'r', encoding='utf-8') as fb:
            answer_content = fb.readlines()

        # 由答案文件获取序号 再在运算式中找到相对应的题目计算答案 再比较
        # 获取列表
        for item_b in answer_content:

            # 每行答案的序号
            answer_sqe = int(item_b.split('. ')[0])

            answer =item_b.split('.')[1]
            # 找到对应的习题的行数
            expression = expression_content[answer_sqe - 1]

            # 分割字符
            pattern = expression.strip().replace(' ', '').replace('　', '').split('.')[1]
            pattern = list(filter(None, split(r'([()×÷+-])', pattern)))

            # 提取表达式并计算 如若正确存进
            if Calculate(pattern).cal_expression()[0].to_string() == answer.strip():
                correct_seq.append(answer_sqe)

        # 生成错误列表
        for item_a in expression_content:
            a_sqe = int(item_a.split('. ')[0])
            if a_sqe not in correct_seq:
                wrong_seq.append(a_sqe)

        # 保存结果
        save_inspect(correct_seq, wrong_seq)

    except IOError:
        print('Failed to open file')
        return


# 保存题目 传入序列号以及题目
def save_exercise(expressions_list, order):
    exercise_file = './docs/Exercises{}.txt'.format(order)
    try:
        with open(exercise_file, 'a+', encoding='utf-8') as f:
            for line in expressions_list:
                f.write('{}\n'.format(line))
    except IOError:
        print('Exercise.txt create failed. Please check again')


# 保存答案 传入序列号以及答案
def save_answer(answers_list, order):
    global flag
    flag=order
    answer_file = './docs/Answer{}.txt'.format(order)
    try:
        with open(answer_file, 'a+', encoding='utf-8') as f:
            for line in answers_list:
                f.write('{}\n'.format(line))
    except IOError:
        print('Answer.txt create failed. Please check again')


# 保存比较结果 传入正确列表以及错误列表
def save_inspect(correct_list, wrong_list):
    global i
    inspect_file = './docs/Grade{}.txt'.format(i)
    try:
        with open(inspect_file, 'w+', encoding='utf-8') as f:
            f.write(f'Correct: {len(correct_list)} {correct_list}\n'
                    f'Wrong: {len(wrong_list)} {wrong_list}\n'
                    f'Accuracy: {round(len(correct_list) / (len(wrong_list) + len(correct_list)), 4) * 100}%\n')
    except IOError:
        print('Grade.txt create failed. Please check again')

