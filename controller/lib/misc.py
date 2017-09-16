#coding:utf-8

import math

def bytesConvert(bytes):
	lst = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
	i = int(math.floor(math.log(bytes, 1024)))

	if i >= len(lst):
		i = len(lst) - 1
	return ('%.2f {}'.format(lst[i])) % (bytes/math.pow(1024, i))