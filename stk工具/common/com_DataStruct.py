#要像被其他代码调用，一种是，目录管理，被上层的代码调用，
#或者放在将模块放在与你的项目代码相同的目录中。
#将模块放在 Python 的标准库路径中。#
#将模块所在的目录添加到 sys.path 中。


#做成共享模块：
#
#不同方法使用不同地方代码
#
class DataStruct( ):
	"""docstring for ClassName"""
	def __init__(self):
		self.data = {
						'stocks':[],#个股信号
						'blocks':[],#板块信号
						'index' :[],#指数信号
					}
	def push(self,data):
			pass
	def pop(self):
			pass
	def append(self,data,keys=[]):#自定义，为了更方便添加，这里单独添加一条就用字典添加就好了，以后在修改如果不方便，但是这里
		#后期可以判断data类型和长度在优化，分类处理保存方式，这里目前是data=[信号异动信息,note链接]
		#想要的是同时给所有字典同时都添加txt
		if(len(keys)==0):#如果空的含义变了，通过多个self.data，来变化也行，以后再说吧，
			for key in self.data.keys():
				self.data[key].append(data)
		else:
			for key in keys:
				self.data[key].append(data)