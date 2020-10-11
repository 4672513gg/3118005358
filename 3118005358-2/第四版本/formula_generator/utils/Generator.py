# 调用, 生成表达式集
from utils.Operation import *
import collections
import multiprocessing
import time
from utils.Arithmetic import *

class Generator(object):

    def __init__(self, num, domain, order=0):
        self.order = order
        # 表达式个数
        self.expression_num = num
        # 表达式集
        self.expressions = []
        # 答案集
        self.answers = []
        # 值域
        self.domain = domain

        # 单次写入的缓冲区
        self.buffer_expression = []
        self.buffer_answer = []
        self.buffer_domain = 1000 if num >= 10000 else 100
        self.no_repeat_dict = {}

    # 检查重复
    def judge_repeat(self, answer, test_sign):
        for expression_sign in self.no_repeat_dict[answer]:
            # 记录相同的个数
            same_num = 0

            for i in range(3):
                if collections.Counter(expression_sign[i]) == collections.Counter(test_sign[i]):
                    same_num += 1
            # 如果中间结果、操作数、运算符均相等，则为重复
            if same_num == 3:
                return False
        return True

    # 表达式-生产
    def expression_generator(self, queue):

        while self.expression_num > 0:

            [expression, operand_list, operator_list] = Arithmetic(self.domain).create_arithmetic()
            [answer, stage_results] = Calculate(expression).cal_expression()

            # 计算错误
            if answer:
                # 如果该答案不存在字典中，则新建该键值对，否则判断重复，若重复则不添加表达式
                stringify_answer = answer.to_string()
                if answer.to_string() in self.no_repeat_dict:
                    if self.judge_repeat(answer.to_string(), [stage_results, operand_list, operator_list]):
                        self.no_repeat_dict[answer.to_string()].append([stage_results, operand_list, operator_list])
                        self.expression_num -= 1
                        res = [expression, answer, self.expression_num]
                        queue.put(res)
                else:
                    self.no_repeat_dict[answer.to_string()] = [[stage_results, operand_list, operator_list]]
                    self.expression_num -= 1
                    res = [expression, answer, self.expression_num]
                    queue.put(res)

    # 表达式-消费
    def io_operation(self, queue):

        index = 0
        while True:

            index += 1
            res = queue.get()
            if res is not None:

                answer = f"{index}. {res[1].to_string()}"
                expression_remain_num = res[2]

                expression_str = str(index) + ". "

                for item in res[0]:
                    if item in operator.values():
                        expression_str += " " + item + " "
                    else:
                        expression_str += item

                # 存入缓冲区
                self.buffer_expression.append(expression_str)
                self.buffer_answer.append(answer)
                # 缓冲区满100个时 写文件
                if index % self.buffer_domain == 0 and expression_remain_num > self.buffer_domain:
                    # 交由I/O操作函数
                    save_exercise(self.buffer_expression, self.order)
                    save_answer(self.buffer_answer, self.order)
                    # 清空buffer
                    self.buffer_expression.clear()
                    self.buffer_answer.clear()
            else:
                # 交由I/O操作函数
                save_exercise(self.buffer_expression, self.order)
                save_answer(self.buffer_answer, self.order)


                # 清空buffer
                self.buffer_expression.clear()
                self.buffer_answer.clear()
                # exit()
                break

    # 调用接口 生成多条题目
    def multi_processor(self):
        start_time = time.time()

        queue = multiprocessing.Queue()
        producer = multiprocessing.Process(target=self.expression_generator, args=(queue,))
        consumer = multiprocessing.Process(target=self.io_operation, args=(queue,))

        producer.start()

        consumer.start()

        producer.join()
        queue.put(None)

        ene_time = time.time()
        print(f"\nBuffer size:{self.buffer_domain}, time cost: {ene_time - start_time}\n")