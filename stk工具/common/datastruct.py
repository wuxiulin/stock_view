#要像被其他代码调用，一种是，目录管理，被上层的代码调用，
#或者放在将模块放在与你的项目代码相同的目录中。
#将模块放在 Python 的标准库路径中。#
#将模块所在的目录添加到 sys.path 中。


#做成共享模块：
#
#不同方法使用不同地方代码
#引入这个模块目的是所有地方使用同一的数据结构方便管理和统一
class DataStruct( ):
	"""docstring for ClassName"""
	def __init__(self):
		self.data = {
						'stocks':[],#个股信号a=["内容提示"，"链接"]
						'blocks':[],#板块信号
						'index' :[],#指数信号
					}
	def push(self,data):
			pass
	def pop(self):
			pass
	def append(self,data,keys=[]):#默认keys为空之后，同时添加三个级别的信号，非空，只添加对应级别信号。
		#后期可以判断data类型和长度在优化，分类处理保存方式，这里目前是data=[信号异动信息,note链接]
		#想要的是同时给所有字典同时都添加txt
		if(len(keys)==0):#如果空的含义变了，通过多个self.data，来变化也行，以后再说吧，
			for key in self.data.keys():
				self.data[key].append(data)
		else:
			for key in keys:
				self.data[key].append(data)
	def update(self,data):#传进来的是DataStruct的数据，进行合并
		self.data["stocks"]=self.data["stocks"]+data.data["stocks"]
		self.data["index"]=self.data["index"]+data.data["index"]
		self.data["blocks"]=self.data["blocks"]+data.data["blocks"]
