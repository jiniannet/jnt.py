# -*- coding: utf-8 -*-
from jntemplate import Template,engine,BaseLoader,FileLoader,engine
from timeit import timeit
import time
#from jntemplate import Lexer

# engine.configure(None)
# lexer = Lexer("${user.name}23412BAESFD$225B${name}${none}")
# arr = lexer.parse()
# for c in arr:
#     print(c.string())

# dic = {"aaa":1}
# #dic.fromkeys
# t ="2"

# print(type(1))
# print(type(1.1))
# print(type(1.11112545225))
# print(type(""))
# print(type([]))
# print(type({}))
# print(type(True))


# class Parent(object):
#     "父类"
#     parentAttr = 100

#     def __init__(self):
#         super(Parent,self).__init__()
#         print ("调用父类构造函数")

#     def parentMethod(self):
#         print ('调用父类方法')

#     def setAttr(self, attr):
#         Parent.parentAttr = attr

#     def getAttr(self):
#         print ("父类属性 :", Parent.parentAttr)

#     def bbb(self):
#         print ("父类bbb")


# class Child(Parent):
#     "定义子类"

 
#     def childMethod(self):
#         print ('调用子类方法 child method')
#         # 在子类中调用父类方法
#         print (Parent.getAttr(self))

#     def bbb(self):
#         print ("Child类bbb")

# class DD(Child):
#     "定义子类"


#     def bbb(self):
#         print ("dd类bbb")
# c = DD()
# c.childMethod()

#engine.configure(None)
# t = Template("hello ${name}")
# t.set("name","jnt4py")
# print(t.render())
#print(hasattr(t,"stringbb"))
#s = getattr(t,"string")
#print(s)
#print(getattr(t,"string"))

#print(dir(getattr(t,"context")) )
#print(t.string())

# class dd:
#     def test(self,a,b):
#         return a+b

# def test1():
#     r = dd()
#     arr=["test code:","success"]
#     eval("r.test(arr[0],arr[1])")

# def test2():
#     r = dd()
#     arr=["test code:","success"]
#     r.test(arr[0],arr[1])

# print(timeit('test1()', 'from __main__ import test1', number=10000))
# print(timeit('test2()', 'from __main__ import test2', number=10000))

# arr = [1,2,3,4,5,6,7]
# print(arr[2:-3])
# print(arr[2:len(arr)-3])


# g = lambda x,y: x +y
# text = "${g(2,8)}vvvvv"
# template = Template(text)
# template.set("g",g)
# print( template.render())


engine.configure()
# text = "$str.upper()"
# template = engine.create_template(text)
# template.set("str","hello jnt4py")
# render = template.render()

template =  engine.create("$data[2]") 
template.set("data", [7, 0, 2, 0, 6])
render = template.render()
print( render)

 

# list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
# print(list[1:3])
# print(list[1:])

#print(type(time.time()))

# dic = {"aaa":1,"bbb":2}
# for n in dic:
#     print(dic[n])