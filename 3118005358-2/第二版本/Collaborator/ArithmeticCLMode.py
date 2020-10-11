from utils.paser import *
from views.UserIntrface import *

"""
1. -n:  输入并获取生成的题目数量
2. -r:  输入并获取参与运算的最大值
3. -e:  选择题目文件
4. -a:  选择答案文件
5. -g:  启动图形化界面
6. -c:  输出检查的结果
7. -f:  命令行界面运行时，"f" 后跟生成试题的份数
"""

order = 0
if __name__ == '__main__':

        add_path='./docs'

        print("+----------------------------------------------------------+\n"
              "|                 欢迎使用四则运算算式生成器               |\n"
              "+----------------------------------------------------------+\n"
              )

        #识别并获取命令行参数
        arg = arg_parse()

        #当 arg.g 赋值 则进入图形化界面
        if arg.g:
            InitWindows()
        #否则使用命令行操作
        else:
            try:
                #生成题目及答案或者检查答案，两者不能同时进行
                if (arg.e or arg.a) and (arg.n or arg.r):
                    print('参数输入错误')
                    exit(0)
                elif arg.a and arg.e:
                    #输入参数正确，执行检查代码部分
                    inspect("./docs/"+arg.a[0], "./docs/"+arg.e[0])
                    print("")
                elif arg.n and arg.r and arg.f:
                    #输入参数正确，执行生成题目和答案文件Grade?.txt
                    for i in range(0,int(arg.f[0])):
                        Generator(arg.n[0], arg.r[0],order).multi_processor()
                        order += 1
                    what_is_in_it = os.listdir(add_path)
                    print("+——————————————————————————————+")

                    for i in range(0,len(what_is_in_it)):
                        if i==(len(what_is_in_it))/3:#3
                            i=2*i
                            for j in range(i,len(what_is_in_it)):
                                print("| " + what_is_in_it[j])
                        elif i<=(len(what_is_in_it))/3:
                            print("| "+what_is_in_it[int(arg.f[0])+i]+" , "+what_is_in_it[i]+"")
                    print("+——————————————————————————————+")

                elif arg.c:
                   try:
                       #打印改卷结果
                       with open("./docs/"+arg.c[0],'r',encoding='UTF-8') as grade:
                            result=grade.read()
                            print(result)
                            grade.close()
                   except Exception as e:
                       print("请输入正确的文件名")

                else:
                    print("帮助信息: 参数输入错误")
            except Exception as e:
                print(e)
