#要像被其他代码调用，一种是，目录管理，被上层的代码调用，
#或者放在将模块放在与你的项目代码相同的目录中。
#将模块放在 Python 的标准库路径中。#
#将模块所在的目录添加到 sys.path 中。


#做成共享模块：
#
#不同方法使用不同地方代码
#引入这个模块目的是所有地方使用同一的数据结构方便管理和统一




class DataStruct( ):  
#此数据结构，配合noteplt来使用的 "异动信号" 来使用的，主要是为他服务的，
#尽量不要给其他东西使用处理
#只是为了方便某些操作才单独拿出来，作为公共模块的
	def __init__(self):
		self.data = {  #notes在第二个板块中方便
						'stocks':[],#个股信号a=["内容提示"，"链接"]
						'blocks':[],#板块信号
						'index' :[],#指数信号
					}
		self.timepoint={
					'time':[],#重要时间点

						}
	def push(self,data):
			pass
	def pop(self):
			pass
	def append(self,data,keys=[]):#默认keys为空之后，同时添加三个级别的信号，非空，只添加对应级别信号。
 
		if(len(data)!=2):
			print("输入数据格式有问题，应该是[信号异动信息,note链接]")
		if(len(data[1])==0):
			#打开提示页面，没有笔记
			data[1]="file:///C:/Users/DELL/Desktop/stk%E5%B7%A5%E5%85%B7/modules/noteplt/help-center/%E6%97%A0%E7%AC%94%E8%AE%B0%E7%BD%91%E9%A1%B5.html"
			 
		#这里不太好检查data的格式是[信号异动信息,note链接]
		if(len(keys)==0):#如果空的含义变了，通过多个self.data，来变化也行，以后再说吧，不是所有地方都需要这样操作，所以新建结构就是了
			for key in self.data.keys():
				self.data[key].append(data)
		else:
			for key in keys:
				self.data[key].append(data)
	def update(self,data):#传进来的是DataStruct的数据，进行合并， 
		self.data["stocks"]=self.data["stocks"]+data.data["stocks"]
		self.data["index"]=self.data["index"]+data.data["index"]
		self.data["blocks"]=self.data["blocks"]+data.data["blocks"]









class TimePoint( ):  
#此数据结构，配合noteplt来使用的 "异动信号" 来使用的，主要是为他服务的，
#尽量不要给其他东西使用处理
#只是为了方便某些操作才单独拿出来，作为公共模块的
	def __init__(self):
		self.data = {  #notes在第二个板块中方便
						'time':[],#个股信号a=["内容提示"，"链接"]
					}
 
	def push(self,data):
			pass
	def pop(self):
			pass
	def append(self,data,keys=[]):#默认keys为空之后，同时添加三个级别的信号，非空，只添加对应级别信号。
			 
		if(len(data)!=2):
			print("输入数据格式有问题，应该是[信号异动信息,note链接]")
		if(len(data[1])==0):
			#打开提示页面，没有笔记
			data[1]="file:///C:/Users/DELL/Desktop/stk%E5%B7%A5%E5%85%B7/modules/noteplt/help-center/%E6%97%A0%E7%AC%94%E8%AE%B0%E7%BD%91%E9%A1%B5.html"
			 
		#这里不太好检查data的格式是[信号异动信息,note链接]
		if(len(keys)==0):#如果空的含义变了，这里代码没有改，因为这里只time这个，所以注意目前没这个需求才从DataStruct分裂的，只是代码没有改而已。其实应该改
			for key in self.data.keys():
				self.data[key].append(data)
		else:
			for key in keys:
				self.data[key].append(data)
				
	def update(self,data ):#传进来的是DataStruct的数据，进行合并， 
		self.data["stocks"]=self.data["stocks"] + data.data["stocks"]
		self.data["index"]=self.data["index"] + data.data["index"]
		self.data["blocks"]=self.data["blocks"] + data.data["blocks"]



class CommonStruct( ):  
#此数据结构，配合noteplt来使用的 "异动信号" 来使用的，主要是为他服务的，
#尽量不要给其他东西使用处理
#只是为了方便某些操作才单独拿出来，作为公共模块的
	def __init__(self):
		self.data = {  #notes在第二个板块中方便
						'dynamic_monitor':[],#个股信号a=["内容提示"，"链接"]
					}
 
	def push(self,data):
			pass
	def pop(self):
			pass
	def append(self,data,keys=[]):#默认keys为空之后，同时添加三个级别的信号，非空，只添加对应级别信号。
			 
		if(len(data)!=2):
			print("输入数据格式有问题，应该是[信号异动信息,note链接]")
		if(len(data[1])==0):
			#打开提示页面，没有笔记
			data[1]="file:///C:/Users/DELL/Desktop/stk%E5%B7%A5%E5%85%B7/modules/noteplt/help-center/%E6%97%A0%E7%AC%94%E8%AE%B0%E7%BD%91%E9%A1%B5.html"
			 
		#这里不太好检查data的格式是[信号异动信息,note链接]
		if(len(keys)==0):#如果空的含义变了，这里代码没有改，因为这里只time这个，所以注意目前没这个需求才从DataStruct分裂的，只是代码没有改而已。其实应该改
			return #不做任何修改变化
		else:
			for key in keys:
				self.data[key].append(data)
				
	def update(self,data ):#传进来的是DataStruct的数据，进行合并， 
		self.data["stocks"]=self.data["stocks"] + data.data["stocks"]
		self.data["index"]=self.data["index"] + data.data["index"]
		self.data["blocks"]=self.data["blocks"] + data.data["blocks"]


if __name__ == '__main__':
	b=DataStruct()
	a=TimePoint()
