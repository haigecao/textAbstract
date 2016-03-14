#!usr/bin/python
#coding=utf-8
# import sys
# import chardet 
# reload(sys)
# sys.setdefaultencoding('utf8')
# import divideSentence








# import chardet 
# fileText = open('hgwj.txt', "rb").read()
# enc = chardet.detect(fileText)
# # enc = chardet.detect("你好") 
# print enc  #返回文件类型s
    
# string = divideSentence.ReadFile('hgwj.txt')

# def obtainFileType(filepath):
#     import chardet 
#     tt = open(filepath, 'rb') 
#     ff = tt.readline()        #这里试着换成read(5)也可以，但是换成readlines()后报错 
#     enc = chardet.detect(ff) 
#     tt.close() 
#     return enc['encoding']  #返回文件类型

# # def obtainFileType(data):
# #     import chardet 
# #     enc = chardet.detect(data) 

# #     return enc['encoding']  #返回文件类型

# url = "hgwj.txt"
# fileText = open(url, "rb").readline()
# divideSentence.remove_special_characters()

# # print obtainFileType(url) 
# # # content = open(url, "rb").read().encode('utf-8')
# # if obtainFileType(url) == "ascii" or obtainFileType(url) == "GB2312":
# # 	print obtainFileType(url) 
# # 	content = open(url, "rb").read().encode('utf-8')

# # elif obtainFileType(url) == 'utf-8':
# # 	content = fileText
# # 	print 'utf-8'
# # else:
# # 	print "未知编码"
# # 	exit()

# enc = chardet.detect(fileText) 
# print enc['encoding']  #返回文件类型


singal_list = []
singal_list.append(1)
singal_list.append(2)
singal_list.append(3)
singal_list.append(4)
print singal_list



