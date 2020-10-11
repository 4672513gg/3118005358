# 把所有数当成分数
class Fraction(object):


    def __init__(self, molecular, denominator=1):
        # 分子
        self.molecular = molecular
        # 分母
        self.denominator = denominator

        z = 0
        if isinstance(self.molecular, str):
            # 如果为带分数则分离整数部分
            if '\'' in self.molecular:
                # 整数部分
                temp = self.molecular.split('\'')
                z = int(temp[0])
                self.molecular = temp[1]
            if '/' in self.molecular:
                self.molecular = self.molecular.split('/')
                self.denominator = int(self.molecular[1])
                self.molecular = int(self.molecular[0])
            else:
                self.molecular = int(self.molecular)
            if z:
                self.molecular += z * self.denominator

    # 计算公约数
    def gcd(self):
        a = self.molecular
        b = self.denominator
        while a:
            temp = b % a
            b = a
            a = temp

        return b

    # 约分
    def fraction_reduction(self):
        gcd = self.gcd()
        self.denominator /= gcd
        self.molecular /= gcd

    # 将分子分母变为字符串形式
    def to_string(self):
        if self.denominator == 1 or self.molecular % self.denominator == 0:
            operand = str(int(self.molecular / self.denominator))
        elif self.molecular > self.denominator:
            z = int(self.molecular / self.denominator)
            self.fraction_reduction()
            operand = str(z) + "\'" + str(int(self.molecular - z * self.denominator)) + "/" + str(int(self.denominator))
        else:
            self.fraction_reduction()
            operand = str(int(self.molecular)) + "/" + str(int(self.denominator))

        return operand
