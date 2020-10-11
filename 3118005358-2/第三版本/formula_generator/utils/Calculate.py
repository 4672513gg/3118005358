# 计算类
from utils.Fraction import *
from utils.constant import *

"""
::param 
::return
"""


class Calculate(object):

    def __init__(self, expression):
        self.expression = expression

    # 分数加法 a1/b1 + a2/b2 = (a1b2 + a2b1)/b1b2
    @staticmethod
    def fraction_add(fra1, fra2):
        molecular = fra1.molecular * fra2.denominator + fra2.molecular * fra1.denominator
        denominator = fra1.denominator * fra2.denominator

        return Fraction(molecular, denominator)

    # 分数减法 a1/b1 - a2/b2 = (a1b2 - a2b1)/b1b2
    @staticmethod
    def fraction_minus(fra1, fra2):
        molecular = fra1.molecular * fra2.denominator - fra2.molecular * fra1.denominator
        denominator = fra1.denominator * fra2.denominator

        return Fraction(molecular, denominator)

    # 分数乘法 a1/b1 * a2/b2 = a1a2/b1b2
    @staticmethod
    def fraction_multiply(fra1, fra2):
        molecular = fra1.molecular * fra2.molecular
        denominator = fra1.denominator * fra2.denominator

        return Fraction(molecular, denominator)

    # 分数除法 a1/b1 ÷ a2/b2 = a1b2/a2b1
    @staticmethod
    def fraction_divide(fra1, fra2):
        molecular = fra1.molecular * fra2.denominator
        denominator = fra1.denominator * fra2.molecular

        return Fraction(molecular, denominator)

    # 基本运算选择器
    def operate(self, num1, num2, operater):
        if not isinstance(num1, Fraction):
            num1 = Fraction(num1)
        if not isinstance(num2, Fraction):
            num2 = Fraction(num2)

        # 计算结果
        if operater == '+':
            return self.fraction_add(num1, num2)
        if operater == '-':
            return self.fraction_minus(num1, num2)
        if operater == '×':
            return self.fraction_multiply(num1, num2)
        if operater == '÷':
            return self.fraction_divide(num1, num2)

    # 转成逆波兰
    def generate_postfix_expression(self):
        # 运算符栈
        operator_stack = []
        # 后缀栈
        postfix_stack = []

        for element in self.expression:
            # 如果是操作数则添加
            if element not in operators:
                postfix_stack.append(element)
            # 如果是运算符则按优先级
            elif element in operator.values():
                # 运算符栈为空，或者栈顶为(，则压栈
                if not operator_stack or operator_stack[-1] == '(':
                    operator_stack.append(element)
                # 若当前运算符优先级大于运算符栈顶，则压栈
                elif priority[element] >= priority[operator_stack[-1]]:
                    operator_stack.append(element)
                # 否则弹栈并压入后缀队列直到优先级大于栈顶或空栈
                else:
                    while operator_stack and priority[element] < priority[operator_stack[-1]]:
                        postfix_stack.append(operator_stack.pop())
                    operator_stack.append(element)

            # 如果遇到括号
            else:
                # 若为左括号直接压入运算符栈
                if element == '(':
                    operator_stack.append(element)
                # 否则弹栈并压入后缀队列直到遇到左括号
                else:
                    while operator_stack[-1] != '(':
                        postfix_stack.append(operator_stack.pop())
                    operator_stack.pop()

        while operator_stack:
            postfix_stack.append(operator_stack.pop())

        return postfix_stack

    # 计算表达式(运算过程出现负数，或者除数为0，返回False，否则返回Fraction类)
    def cal_expression(self):
        # 生成后缀表达式
        expressions_result = self.generate_postfix_expression()
        # 存储阶段性结果
        stage_results = []

        # 使用list作为栈来计算
        calculate_stack = []

        # 后缀遍历
        for element in expressions_result:
            # 若是数字则入栈, 操作符则将栈顶两个元素出栈
            if element not in operators:
                calculate_stack.append(element)
            else:
                # 操作数
                num1 = calculate_stack.pop()
                # 操作数
                num2 = calculate_stack.pop()

                # 除数不能为0
                if num1 == "0" and element == '÷':
                    return [False, []]

                # 结果
                result = self.operate(num2, num1, element)

                if result.denominator == 0 or '-' in result.to_string():
                    return [False, []]

                stage_results.append(result.to_string())

                # 结果入栈
                calculate_stack.append(result)

        # 返回结果
        return [calculate_stack[0], stage_results]