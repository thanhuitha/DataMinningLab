import numpy as np
import pandas as pd
import sys
import math

name ,option , f_input, f_output, f_log = sys.argv
df = pd.read_csv(f_input,delimiter=',')

if option == 'summary':
	with open(f_log,'w') as f:
		num_entri = df.shape[0]
		num_col = df.shape[1]
		f.write(str(num_entri)+'\n')
		f.write(str(num_col)+'\n')
		col = df.columns
		s = ''
		for index,c in enumerate(col):
			if '?' in list(df[c].unique()):
				df = df[df[c] != '?']
			try:
				val = df[c].astype(int)
				s += 'Thuoc tinh thu '+str(index+1)+' : '+c+' '+'numeric'
			except Exception :
				s += 'Thuoc tinh thu '+str(index+1)+' : '+c+' '+'nominal'
			s +='\n'
		f.write(s)
if option =='replace':
	with open(f_log,'w') as f:
		col = df.columns
		for index,c in enumerate(col):
			if '?' in list(df[c].unique()):
				df[c] = df[c].replace('?',np.nan)
				num_miss = df[c].isnull().sum()
				new_value = ''

				tt = ''
				try:
					df[c] = df[c].astype(float)
					new_value = df[c].mean()
					new_value = round(new_value,3)
					df = df.replace(np.nan,new_value)
				except Exception:
					new_value = df[c].value_counts().idxmax()
					df = df.replace(np.nan,new_value)
				f.write(str(c)+' '+str(num_miss)+' '+str(new_value)+'\n')
	df.to_csv(f_output,header=df.columns,index=None,sep=',',mode='a')



if option =='discretize':
	print('1.Chia gio theo chieu rong\n2.Chia gio theo chieu sau')
	print('Chon 1 hoac 2 ?')
	style = int(input())
	print('Chon so gio :')
	num_bag = int(input())
	# chia gio theo chieu sau
	if style == 2:
		col = df.columns
		with open(f_log,'w') as f:
			for index,c in enumerate(col):
				if '?' in list(df[c].unique()):
					df[c] = df[c].replace('?',np.nan)
				try:
					df[c] = df[c].astype(float)
					val_c = np.array(df[c].unique())
					val_c = np.sort(val_c)
					if np.isnan(val_c[-1]):
						val_c =np.delete(val_c, -1)

					f.write('Thuoc tinh : '+c)
					val_c = list(val_c)

					h_bin = len(val_c)//num_bag
					result = []
					binn = []

					if num_bag >= len(val_c):
						for x in val_c:
							result.append([x])
					else:
						for i,value in enumerate(val_c):
							if len(result) + 1 == num_bag:
								result.append(val_c[i-1:])
								break
							else:
								if len(binn) < h_bin:
									binn.append(value)
								else:
									result.append(binn)
									binn = [value]
					for i in result:
						f.write('<'+'['+str(i[0])+' '+str(i[-1])+']>:')
						f.write('<'+str(len(i))+'>')
					f.write("\n")
					for ii,vll in enumerate(result):
						df[c] = df[c].replace(vll,'['+str(result[ii][0])+' '+str(result[ii][-1])+']')
				except Exception:
					tmp = 0
	#Chia gio theo chia rong
	if style == 1:
		col = df.columns
		with open(f_log,'w') as f:
			for index,c in enumerate(col):
				if '?' in list(df[c].unique()):
					df[c] = df[c].replace('?',np.nan)
				try:
					df[c] = df[c].astype(float)
					val_c = np.array(df[c].unique())
					val_c = np.sort(val_c)
					if np.isnan(val_c[-1]):
						val_c =np.delete(val_c, -1)

					val_c = list(val_c)
					f.write('Thuoc tinh : '+c)
					r_bin = (val_c[-1] - val_c[0])//num_bag
					min_bin,max_bin = val_c[0],val_c[0] + r_bin
					count = 0
					for i,value in enumerate(val_c):
						if value == val_c[-1]:
							count +=1
							df[c] = df[c].replace(value,'['+str(min_bin)+' '+str(max_bin)+']')
							f.write('<'+'['+str(min_bin)+' '+str(value)+']>:'+str(count))
							break
						if value >= min_bin and value < max_bin:
							count +=1
							df[c] = df[c].replace(value,'['+str(min_bin)+' '+str(max_bin)+')')
						else:
							f.write('<'+'['+str(min_bin)+' '+str(max_bin)+')>:'+str(count))
							min_bin = max_bin
							max_bin = min_bin + r_bin
							count = 1
							df[c] = df[c].replace(value,'['+str(min_bin)+' '+str(max_bin)+']')
					f.write('\n')
				except Exception:
					tmp = 0

	df.to_csv(f_output,header=df.columns,index=None,sep=',',mode='a')

if option == 'normalize':
	print('1.Min-Max \n2.Z-score')
	print('1 or 2 ?')
	choose = int(input())
	if choose == 1:
		col = df.columns
		with open(f_log,'w') as f:
			for index,c in enumerate(col):
				if '?' in list(df[c].unique()):
					df[c] = df[c].replace('?',np.nan)
				try:
					df[c] = df[c].astype(float)
					val_c = np.array(df[c].unique())
					val_c = np.sort(val_c)
					if np.isnan(val_c[-1]) :
						val_c =np.delete(val_c, -1)

					val_c = list(val_c)
					if val_c[0] != val_c[-1]:
						for ii,vll in enumerate(val_c):
							new_vll = (vll-val_c[0])/(val_c[-1]-val_c[0])
							df[c] = df[c].replace(vll,round(new_vll,3))
					f.write('Thuoc tinh: '+c + ' [0 1]')
					f.write('\n')
				except Exception:
					tmp = 0
	if choose == 2:
		col = df.columns
		with open(f_log,'w') as f:
			for index,c in enumerate(col):
				if '?' in list(df[c].unique()):
					df[c] = df[c].replace('?',np.nan)
				try:
					df[c] = df[c].astype(float)

					mean = df[c].mean()
					var_std = df[c].std()

					val_c = np.array(df[c].unique())
					val_c = np.sort(val_c)
					if np.isnan(val_c[-1]) :
						val_c =np.delete(val_c, -1)

					val_c = list(val_c)
					if val_c[0] != val_c[-1]:
						for ii,vll in enumerate(val_c):
							new_vll = (vll-mean)/var_std
							df[c] = df[c].replace(vll,round(new_vll,3))
					f.write('Thuoc tinh: '+c+ '['+str(df[c].max())+' '+str(df[c].min())+']')
					f.write('\n')
				except Exception:
					tmp = 0

	df.to_csv(f_output,header=df.columns,index=None,sep=',',mode='a')
