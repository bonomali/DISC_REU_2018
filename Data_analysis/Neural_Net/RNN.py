##Created by Jun Han
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch
import numpy as np
from torch.utils.data import DataLoader
import argparse
import torch.optim as optim


parser = argparse.ArgumentParser(description='PyTorch Implementation of RNN,GRU, and LSTM')
parser.add_argument('--lr', type=float, default=1e-3, metavar='LR',
                    help='learning rate (default: 1e-4)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='disables CUDA training')
parser.add_argument('--batch_size', type=int, default=1, metavar='N',
                    help='input batch size for training (default: 128)')
parser.add_argument('--epochs', type=int, default=100, metavar='N',
                    help='number of epochs to train (default: 100)')
parser.add_argument('--embed_size', type=int, default=1,
                    help='intput in RNN')
parser.add_argument('--hidden_size', type=int, default=128,
                    help='hidden dimension in RNN')

args = parser.parse_args()
print(not args.no_cuda)
print(torch.cuda.is_available())
args.cuda = not args.no_cuda and torch.cuda.is_available()
kwargs = {'num_workers': 10, 'pin_memory': True} if args.cuda else {}


class GRUCell(nn.Module):
	def __init__(self):
		super(GRUCell,self).__init__
		self.Wxu = nn.Parameter(torch.FloatTensor(args.embed_size,args.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.Whu = nn.Parameter(torch.FloatTensor(args.hidden_size,args.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.bu = nn.Parameter(torch.zeros(1,args.hidden_size),requires_grad=True)
		self.Wxr = nn.Parameter(torch.FloatTensor(arg.embed_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.Whr = nn.Parameter(torch.FloatTensor(arg.hidden_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.br = nn.Parameter(torch.zeros(1,arg.hidden_size),requires_grad=True)
		self.Wxc = nn.Parameter(torch.FloatTensor(arg.embed_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.bc= nn.Parameter(torch.zeros(1,arg.hidden_size),requires_grad=True)
		self.Whc = nn.Parameter(torch.FloatTensor(arg.hidden_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)

	def forward(self,input,hidden_state):
		u = F.sigmoid(input*self.Wxu+torch.mm(hidden_state,self.Whu)+bu)
		r = F.sigmoid(input*self.Wxr+torch.mm(hidden_state,self.Whr)+br)
		c_prime = F.tanh(input*self.Wxc+torch.mm(hidden_state*r,self.Whc)+self.bc)
		c = u*c_prime+(1-u)*hidden_state
		return c

class LSTM_Cell(nn.Module):
	def __init__(self):
		super(LSTM_Cell,self).__init__
		self.Wci = nn.Parameter(torch.FloatTensor(arg.embed_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.Wch = nn.Parameter(torch.FloatTensor(arg.hidden_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.bc = nn.Parameter(torch.zeros(1,arg.hidden_size),requires_grad=True)
		self.Wui = nn.Parameter(torch.FloatTensor(arg.embed_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.Wuh = nn.Parameter(torch.FloatTensor(arg.hidden_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.bu = nn.Parameter(torch.zeros(1,arg.hidden_size),requires_grad=True)
		self.Wfi = nn.Parameter(torch.FloatTensor(arg.embed_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.Wfh = nn.Parameter(nn.init.normal(args.hidden_size,args.hidden_size))
		self.bf = nn.Parameter(torch.zeros(1,arg.hidden_size),requires_grad=True)
		self.Woi = nn.Parameter(torch.FloatTensor(arg.embed_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.Woh = nn.Parameter(torch.FloatTensor(arg.hidden_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.bo = nn.Parameter(torch.zeros(1,arg.hidden_size),requires_grad=True)


	def forward(self,input,hidden_state,cell_state):
		c_prime = F.tanh(input*self.Wci+torch.mm(hidden_state,self.Wch)+self.bc)
		update_state = F.sigmoid(input*self.Wui+torch.mm(hidden_state,self.Wuh)+self.bu)
		forget_state = F.sigmoid(input*self.Wfi+torch.mm(hidden_state,self.Wfh)+self.bf)
		output_state = F.sigmoid(input*self.Woi+torch.mm(hidden_state,self.Woh)+self.bo)
		c = update_state*c_prime+forget_state*cell_state
		h = output_state*F.tanh(c)
		return h,c

class RNN_Cell(nn.Module):
	def __init__(self):
		super(RNN_Cell,self).__init__()
		self.Wx = nn.Parameter(torch.FloatTensor(arg.embed_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.Wh = nn.Parameter(torch.FloatTensor(arg.hidden_size,arg.hidden_size).uniform_(-1e-1,1e-1),requires_grad=True)
		self.b = nn.Parameter(torch.zeros(1,arg.hidden_size),requires_grad=True)

	def forward(self,x,hidden_state):
		return F.tanh(x*self.Wx+torch.mm(hidden_state,self.Wh)+self.b)

class RNN_OneLayer(nn.Module):
	def __init__(self,mode,length,distrbution):
		super(RNN_OneLayer,self).__init__()
		self.RNN_cell = RNN_Cell()
		self.mode = mode
		self.length = length
		self.fc_score = nn.Linear(arg.hidden_size,1)
		if distrbution is not None:
			self.fc_dis = nn.Linear(arg.hidden_size,distrbution)

	def forward(self,x):
		h0 = Variable(torch.zeros(1,arg.hidden_size))
		for i in range(0,self.length):
			h0 = self.RNN_cell(x[0][i],h0)
		if self.mode == 'Score':
			h0 = F.sigmoid(self.fc_score(h0))
		elif self.mode == 'Distrbution':
			h0 = F.softmax(self.fc_dis(h0))
			h0 = torch.argmax(h0)
		return h0

class GRU_OneLayer(nn.Module):
	def __init__(self,mode,length,distrbution):
		super(GRU_OneLayer,self).__init__
		self.GRU_cell = GRU_cell(args.embed_size,args.hidden_size)
		self.mode = mode
		self.length = length
		self.fc_score = nn.Linear(args.hidden_size,1)
		if distrbution is not None:
			self.fc_dis = nn.Linear(args.hidden_size,distrbution)

	def forward(x):
		h0 = Varibale(torch.zeros(1,args.hidden_size))
		for i in range(0,length):
			h0 = self.RNN_cell(x[0][i],h0)
		if self.mode == 'Score':
			h0 = F.sigmoid(self.fc_score(h0))
		elif self.mode == 'Distrbution':
			h0 = F.softmax(self.fc_dis(h0))
			h0 = torch.argmax(h0)
		return h0

class LSTM_OneLayer(nn.Module):
	def __init__(self,mode,length,distrbution):
		super(LSTM_OneLayer,self).__init__
		self.LSTM_cell = LSTM_cell(args.embed_size,args.hidden_size)
		self.mode = mode
		self.length = length
		self.fc_score = nn.Linear(args.hidden_size,1)
		if distrbution is not None:
			self.fc_dis = nn.Linear(args.hidden_size,distrbution)

	def forward(x):
		h0 = Varibale(torch.zeros(1,arg.hidden_size))
		c0 = Varibale(torch.zeros(1,arg.hidden_size))
		for i in range(0,length):
			h0,c0 = self.RNN_cell(x[0][i],h0,c0)
		if self.mode == 'Score':
			h0 = F.sigmoid(self.fc_score(h0))
		elif self.mode == 'Distrbution':
			h0 = F.softmax(self.fc_dis(h0))
			h0 = torch.argmax(h0)
		return h0

def GetData():
	##############################

	# read data into data and label arrays

	##############################
	data = torch.FloatTensor(data)
	label = torch.FloatTensor(label)
	dataset = torch.utils.data.TensorDataset(data,label)
	train_loader = DataLoader(dataset=dataset,batch_size=args.batch_size, shuffle=True, **kwargs)
	return train_loader



def train(mode,epoch,model,train_loader):
	optimizer = optim.Adam(model.parameters(), lr=args.lr)
	if mode == 'Score':
		Loss = nn.BCELoss()
	elif mode == 'Distrbution':
		Loss = nn.CrossEntropyLoss()
	for itera in range(1,epoch+1):
		l = 0.0
		for batch_idx, (data,label) in enumerate(train_loader):
			data = Variable(data)
			label = Variable(label)
			optimizer.zero_grad()
			label_pre = model(data)
			c = Loss(label_pre,label)
			l = l+c.item()
			c.backward()
			optimizer.step()
		print("Loss = "+str(l))
	torch.save(model,'model.pth')


def main(model_type,length,mode,distrbution):
	train_loader = GetData()
	if model_type =='RNN':
		model = RNN_OneLayer(mode=mode,length=length,distrbution=distrbution)
	elif model_type =="GRU":
		model = GRU_OneLayer(mode=mode,length=length,distrbution=distrbution)
	elif model_type=="LSTM":
		model = LSTM_OneLayer(mode=mode,length=length,distrbution=distrbution)
	train(mode,args.epochs,model,train_loader)





