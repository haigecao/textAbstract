#!usr/bin/python
#coding=utf-8
import divideSentence
import obtainKeywords
import sys, time, re
import operator  	#这里用到了 sort



#############################################
'''
这有几种方式, 
第一种: 判断是否有关键词, 把所有包含关键词的句子提取出来(可设置关键词的最少包含个数), 然后进行 关键词 和 高频词 加权算法.
第二种: 判断是否包含关键词和高频词汇. 此时, 就要使用高频词汇表中不除去关键词的列表. 然后进行计算
第三种: 判断高频词汇是否在句子中, 然后从挑选出来的句子进行计算.

阈值的设置
(1) 整句都是一个簇
(2) 最多5个词是一个阈值
(3) 最多7个词是一个阈值,


计算方式:三种.
(1) 高频词汇 和 关键词 全职相等 都是 1
(2) 关键词 1.5 高于 高频词汇的 1
(3) 关键词 和 高频词汇 交集 权值是2.5 关键词 2 高频词汇 1

'''
##################################          函数        #################################

# 提取含有标记词的句子.
# 参数 1 标记词, 2 句子 
def having_signSentence(wordlist, sentences_list):
	signSentence = []	#保存有标记词的句子.
	for sentence in sentences_list:		#遍历文章句子列表
	 	for signWord in wordlist:		#遍历标记词列表
	 		if signWord in sentence:	#若句子存在, 标记词存在
	 			# print signWord
	 			if sentence not in signSentence:		#判断是否已经存入了该句
	 				signSentence.append(sentence)		#将句子存入含有标记词的列表
	 			break 									#存入就可以退出内层循环

	return signSentence 	#返回提取的句子

##########################################################################################
'''
		###########      第0种       ################
'''
# 第0种 ----只统计标记词的个数,
# 参数 1:关键词 2:高频词汇 3:文章句子列表 4:摘录句子的数量, 5:模式 如果是True,筛选句子只用关键词, False就用关键词和高频词汇 
def zero_Text_Abstract(keywords, high_frequency_vocabulary, sentences_list, sentenceNum, only_key_Model):
	# 1 合并关键词表
	if only_key_Model == True:
		wordlist = keywords 
	else:
		wordlist = list(set(keywords + high_frequency_vocabulary))
		
	# 2 获取有关键词的句子
	signSentence = having_signSentence(wordlist, sentences_list)

	# 3 计算句子权值并排序
	weightMap = {}		#保存权值的字典
	countNum = 0		#记录顺序的标记
	for sentence in signSentence:		# 提取包含了标记词的句子	
		countNum = countNum + 1
		numWord = 0						# 记录一个句子中标记词的个数
		for word in wordlist:			# 遍历标记词表
			if word in sentence:		# 不记录重复的标记词, 就是每个标记词, 有多少次记录多少次, 即使在句子中出现多次
				numWord = numWord + sentence.count(word) 	# 存在就加  sentence.count(word) 计算word在 sentence中存在的次数
				 	
		weight = (numWord * numWord) * 1.0 / len(sentence)	# 计算权值, 就是词语个数
		weightMap[countNum] = weight 	# 保存权值, 加如序号的原因,是如果句子权值相同,选择排在前面的

	sorted_high_weight_sentence = sorted(weightMap.iteritems(), key=operator.itemgetter(1), reverse=True)  	#给权值排序

	# 4 选择权值排在前面的句子, 作为摘要
	singalBreak = sentenceNum		#选择7句作为文章摘要
	print '一共多少个句子', len(signSentence)


	for high_weight_sign in sorted_high_weight_sentence:	#选择权值高的句子编号
		singalBreak = singalBreak - 1
		print '第%d句子' % high_weight_sign[0], signSentence[high_weight_sign[0] - 1]				#输出句子
		if singalBreak == 0:
			break

	print
	print


##########################################################################################


'''
		###########      第一类      ################
'''
# 实现第一种 先寻找含有关键词的句子.  阈值的大小就是整个句子, 且所有词汇权重相同都是1
# 参数 1:关键词 2:高频词汇 3:文章句子列表 4:摘录句子的数量
def fisrt_Text_Abstract(keywords, high_frequency_vocabulary, sentences_list, sentenceNum):
	# 1 合并关键词表
	wordlist = list(set(keywords + high_frequency_vocabulary))
	
	# 2 获取有关键词的句子
	signSentence = having_signSentence(wordlist, sentences_list)

	# 3 计算句子权值并排序
	weightMap = {}		#保存权值的字典
	countNum = 0		#记录顺序的标记
	for sentence in signSentence:		# 提取包含了标记词的句子	
		countNum = countNum + 1
		numWord = 0						# 记录一个句子中标记词的个数
		for word in wordlist:
			if word in sentence:		# 不记录重复的标记词, 就是每个标记词,只记录一次,即使在句子中出现多次
				numWord = numWord + sentence.count(word) 	# 存在就加  sentence.count(word) 计算word在 sentence中存在的次数

		# print numWord
		weight = (numWord * numWord) * 1.0 / len(sentence)	# 计算权值, 计算方式: (标记词个数的平方) / (句子长度)
		weightMap[countNum] = weight 	# 保存权值, 加如序号的原因,是如果句子权值相同,选择排在前面的

	sorted_high_weight_sentence = sorted(weightMap.iteritems(), key=operator.itemgetter(1), reverse=True)  	#给权值排序

	# 4 选择全职排在前面的句子, 作为摘要
	singalBreak = sentenceNum		#选择7句作为文章摘要
	print '一共多少个句子', len(signSentence)

	for high_weight_sign in sorted_high_weight_sentence:	#选择权值高的句子编号
		singalBreak = singalBreak - 1
		print '第%d句子' % high_weight_sign[0], signSentence[high_weight_sign[0] - 1]				#输出句子
		if singalBreak == 0:
			break

	print
	print

##########################################################################################


'''
		###########      第2类       ################
'''

#		(1)--以关键词作为 提取句子的基础, 
# 		(2)--权值是关键词为1, 高频词汇为 1 或 0.5
########################################################################
#函数参数: 1 关键醋, 2 高频词汇, 3 文章句子列表, 4: 摘录句子的数量
########################################################################
def second_Text_Abstract(keywords, high_frequency_vocabulary, sentences_list, sentenceNum):
	# 1 获取关键词表
	wordlist = keywords
								
	# 2 获取有关键词的句子
	signSentence = having_signSentence(wordlist, sentences_list)

	# 3 计算句子权值并排序
	weightMap = {}		#保存权值的字典
	countNum = 0		#记录顺序的标记
	for sentence in signSentence:		# 提取包含了关键词的句子	
		countNum = countNum + 1
		numWord = 0						# 记录一个句子中关键词的权值
		for word in keywords:			# 遍历关键词表
			if word in sentence:		# 不记录重复的关键词, 就是每个关键词,只记录一次,即使在句子中出现多次
				numWord = numWord + sentence.count(word) 	# 存在就加  sentence.count(word) 计算word在 sentence中存在的次数

		for word in high_frequency_vocabulary:		#遍历高频词汇表
			if word in sentence:			# 不记录重复的高频词汇, 就是每个高频词汇, 只记录所包含的次, 如果在句子中出现多次
				numWord = numWord + 0.5 * sentence.count(word)	# 存在就加 0.5 * n

		# print numWord
		weight = (numWord * numWord) * 1.0 / len(sentence)	# 计算权值, 计算方式: (标记词个数的平方) / (句子长度)
		weightMap[countNum] = weight 	# 保存权值, 加如序号的原因,是如果句子权值相同,选择排在前面的

	sorted_high_weight_sentence = sorted(weightMap.iteritems(), key=operator.itemgetter(1), reverse=True)  	#给权值排序

	# 4 选择全职排在前面的句子, 作为摘要
	singalBreak = sentenceNum		#选择7句作为文章摘要
	print '一共多少个句子', len(signSentence)

	for high_weight_sign in sorted_high_weight_sentence:	#选择权值高的句子编号
		singalBreak = singalBreak - 1
		print '第%d句子' % high_weight_sign[0], signSentence[high_weight_sign[0] - 1]				#输出句子
		if singalBreak == 0:
			break

	print
	print
##########################################################################################

# 在阈值固定的情况下, 获取一个最大的簇, 保证包含的关键词个数最多
# 参数: 一个链表, 保存了关键词的位置, 用 0 / 1 表示, 就是关键词所在句子这的位置.
# 返回值: 包含关键词, 最大的个数.
def having_max_keywords_in_threshold(singal_list, threshold):
	length = len(singal_list)		# 标记词的个数
	if length == 1:					# 如果只有一个关键词,那就只能是一个了
		return 1

	maxCount = 0					# 记录包含最多标记词的个数.
	count_keyword_distance = []		# 保存关键词之间的距离

	if (singal_list[length - 1] - singal_list[0]) <= threshold:		#包含所有.
		maxCount = length
	else:
		for i in range(length - 1):		# 这里只遍历了总长度减一,因为最后一个无法做差了.
			count_keyword_distance.append(singal_list[i + 1] - singal_list[i])

		# 关键词之间的距离个数, 等于关键词个数 - 1 
		len_distance = 0	# 记录词语之间的距离, 与阈值做比较
		count = 0 			# 记录每次遍历的包含个数.

		for i in range(length - 1):			
			if count_keyword_distance[i] < threshold:
				count = 2		# 因为这是差值节点, 一个差值, 就包含2个节点.
				len_distance = count_keyword_distance[i]  	# 保持距离

				for j in range(i + 1, length - 1):
					if len_distance + count_keyword_distance[j] < threshold:
						count = count + 1
						if count > maxCount:
							maxCount = count
						len_distance = len_distance + count_keyword_distance[j]
					else:
						break

	# print count_keyword_distance
	# print maxCount

	return maxCount		#返回最大的个数.


# 参数: 1--signSentence_dict = {} 	保存有标记词的句子.
#      2--sentence_for_map 			文章分词之后--句子列表
def having_mark_sentence_in_Clause(signSentence_dict, wordlist, sentence_for_map):
	#获取包含了关键词的链表, 组成的字典. key 是在文章中出现的顺序, value 是分词以后的句子.
	for (num, sentence_list) in sentence_for_map.items(): 
		for word in wordlist:
			if word in sentence_list:
				signSentence_dict[num] = sentence_list
				break

	return signSentence_dict
########################################################################

########################################################################
# 函数排序后的句子, 输出结果, 
# 参数: 	1 sorted_high_weight_sentence 	按照权值排序后的包含标记词的句子.
#		2 signSentence_dict 			保存有标记词的句子
#		3 sentenceNum 					选择输出句子的数量, 作为文章摘要
#		4 lengthSenctenceMax			句子的最大长度词数

def show_result_sentence(sorted_high_weight_sentence, signSentence_dict, sentenceNum, lengthSenctenceMax):
	singalBreak = sentenceNum									#选择多少句, 数量, 作为文章摘要
	print '一共多少个句子', len(signSentence_dict)

	for high_weight_sign in sorted_high_weight_sentence:		#选择权值高的句子编号
		
		if len(signSentence_dict[high_weight_sign[0]]) >= lengthSenctenceMax:	#如果句子大于最大长度的词数, 就放弃
			continue

		singalBreak = singalBreak - 1
		print '第%d句子' % high_weight_sign[0], 					
		for word in signSentence_dict[high_weight_sign[0]]: 	#输出句子
			print word,
		print 
		if singalBreak == 0:
			break


'''
		###########      第3类       ################
'''

########################################################################
#		(1)--以关键词作为 提取句子的基础, 
# 		(2)--权值是关键词为1, 高频词汇为 1 或 0.5
#		(3)--阈值是5, 只有标记词距离在5个之内, 才会假如算入权值, 
########################################################################
'''
		这是第三类 第一种: 只计算关键词 并且,只计算最大的簇, 只计算了一个簇中的关键词,
	用这个簇的关键词的平方,厨艺句子的长度.(这里没有除以簇的长度,而是句子的长度.)
'''
#函数参数: 1 关键醋, 2 高频词汇, 3 文章分词之后--句子列表, 4: 摘录句子的数量, 5: 阈值的大小 ,默认为 5 threshold
########################################################################
def Third_Text_Abstract_A(keywords, high_frequency_vocabulary, sentence_for_map, sentenceNum, threshold = 7, lengthSenctenceMax = 40):
	# 1 获取关键词表
	wordlist = keywords
	# 2 获取有关键词的句子
	count = 0				# 作为标号, 进行分句的key,
	signSentence_dict = {}	# 保存有标记词的句子.
	
	#获取含有标记词的句子 字典. key 保存出现的顺序, value 保存句子.
	signSentence_dict = having_mark_sentence_in_Clause(signSentence_dict, wordlist, sentence_for_map)

	#阈值为7, 为一簇, 计算方式有很多种,这里选择最简单的方式, 计算一段话中, 最大的一簇, 所包含的关键词的个数.
	weightMap = {}		# 保存权值的字典
	weightMap_only_Count = {}
	for (num, sentence_list) in signSentence_dict.items(): 
		singal_list = []		# 保留有关键词的位置, 是就1, 不是关键词就是0, 形成了一个关键词标记的链表
		singal_num = 0
		for word in sentence_list:			# 遍历句子, 用句子内的分词去匹配标记词, 看是否存在
			singal_num = singal_num + 1   	# 遍历单词, 加1. 举例: 1 和 7是, 7 - 1 = 6 < 阈值.即可. 防止出现 7 - 0 = 7 情况, 这事实上已经8个了.
			if word in keywords:
				singal_list.append(singal_num)

		# print "singal_list  ", singal_list		
		# print singal_list
		countMaxNum = having_max_keywords_in_threshold(singal_list, threshold)		# 获取最大簇中包含的关键词的个数
		weightMap[num] = countMaxNum * countMaxNum * 1.0 / len(sentence_list)

## 只算了权值,不计算长度.
	# 	weightMap_only_Count[num] = countMaxNum
	# sorted_high_weight_sentence_only_keywords = sorted(weightMap_only_Count.iteritems(), key=operator.itemgetter(1), reverse=True)  	# 按照权值排序	
	# print sorted_high_weight_sentence_only_keywords

	sorted_high_weight_sentence = sorted(weightMap.iteritems(), key=operator.itemgetter(1), reverse=True)  	# 按照权值排序	
	# print sorted_high_weight_sentence
	show_result_sentence(sorted_high_weight_sentence, signSentence_dict, sentenceNum, lengthSenctenceMax)
	# singalBreak = sentenceNum		#选择7句作为文章摘要
	# print '一共多少个句子', len(signSentence_dict)

	# for high_weight_sign in sorted_high_weight_sentence:	#选择权值高的句子编号
	# 	if len(signSentence_dict[high_weight_sign[0]]) >= 40:	#如果句子大于15个词, 就放弃
	# 		continue

	# 	singalBreak = singalBreak - 1
	# 	print '第%d句子' % high_weight_sign[0], 					
	# 	for word in signSentence_dict[high_weight_sign[0]]: 	#输出句子
	# 		print word,
	# 	print 
	# 	if singalBreak == 0:
	# 		break


	# print weightMap


########################################################################
# 获取被标记过后的标记词链表, 返回, 除去了最长标记词的链表
def having_lableword_count_list(singal_list, threshold):
	length = len(singal_list)		# 标记词的个数
	count_keyword_distance = []		# 保存关键词之间的距离

	for i in range(length - 1):		# 这里只遍历了总长度减一,因为最后一个无法做差了.
		count_keyword_distance.append(singal_list[i + 1] - singal_list[i])

	# print count_keyword_distance
	# 关键词之间的距离个数, 等于关键词个数 - 1 
	len_distance = 0	# 记录词语之间的距离, 与阈值做比较
	count = 0 			# 记录每次遍历的包含个数.
	singla_del = 0		# 用了删除已经标记了的词.
	maxCount = 0		# 记录列表中 簇中包含的最大分词个数

	for i in range(length - 1):			# 这里只遍历了总长度减一,因为最后一个无法做差了.
		if count_keyword_distance[i] < threshold:
			count = 2		# 因为这是差值节点, 一个差值, 就包含2个节点.
			if maxCount < count:
				maxCount = count
				# print 'maxCount', maxCount
				singla_del = i 	# 保存删除词的其实位置, 因为被标记后的词, 就已经被取出了, 不能从新计入下一次循环
			len_distance = count_keyword_distance[i]  	# 保存距离

			for j in range(i + 1, length - 1):
				if len_distance + count_keyword_distance[j] < threshold:	# 继续叠加词语之间的距离, 若依旧小于阈值,就在 加1
					count = count + 1

					if count > maxCount:		# 若此时标记词个数 大于 最大标记词个数, 就进行赋值.
						maxCount = count
						# print 'maxCount', maxCount
						singla_del = i 			# 保存删除词的其实位置, 因为被标记后的词, 就已经被取出了, 不能从新计入下一次循环
					len_distance = len_distance + count_keyword_distance[j]
				else:
					break

	# print 'singla_del: 删除的起始位置:', singla_del, 'maxCount:删除长度', maxCount

	#  如果 maxCount == 0 , 证明所有标记词, 都只能各自在自己的簇中, 不存在于一个簇中. 返回标记词的个数.
	if maxCount == 0:
		return length  	# 返回标记词列表长度,

	# 将链表中的标记词, 标记为普通词汇, 但是要将词之间的关系更新. 剩下的标记词之间的距离要更新.
	if singla_del == 0:			# 从第一词开始更新标记词表	
		# print '-------singla_del == 0---------'
		for start in range(0, maxCount):
			# print 'start', start
			del singal_list[0]
			
	elif (singla_del + maxCount) >= length:		# 这种情况是, 从最后一个词进行更新标记词表
		# print '--------(singla_del + maxCount) >= length--------'
		for start in range(0, maxCount)[: : -1]:		# [::-1] 数组倒序遍历
			del singal_list[len(singal_list) - 1]

	else:										# 这种情况是在中间.
		# print "------这种情况是在中间.-------"
		for start in range(0, maxCount)[::-1]:		# [::-1] 数组倒序遍历
			del singal_list[singla_del]

	# print 'singal_list 函数返回:', singal_list
	return singal_list


########################################################################
#函数作用: 返回 簇中, 包含标记词个数的数组,
'''
	# 在阈值固定的情况下, 梯度获取包含标记词的簇, 
	# 保证包含标记词最多的簇优先选出, 然后被选择的标记词就标记为普通词, 
	# 重复继续选择, 直到所有的标记词都被选中.
'''
# 参数: 一个链表, 保存了关键词的位置, 用 0 / 1 表示, 就是关键词所在句子这的位置.
# 返回值: 包含标记词的个数的数组, 数组的每一个值, 包含了一个簇内关键词的个数
########################################################################

def having_all_keywords_in_threshold(singal_list, threshold):
	thresholdCount = []				# 记录簇中包含标记词的个数的列表, 列表的每个值代表, 在同一个簇中,关键词的个数
	length = len(singal_list)		# 标记词的个数

	if length == 1:					# 如果只有一个关键词,那就只能是一个了
		thresholdCount.append(1)	
		# print '如果只有一个关键词,那就只能是一个了'
		return thresholdCount		# 返回列表


	if (singal_list[length - 1] - singal_list[0]) <= threshold:		# 包含所有. 因为 词表的长度 小于 阈值 
		thresholdCount.append(length)	# 将所有词数 全部放入
		# print '将所有词数 全部放入', thresholdCount
		return thresholdCount		# 返回列表

	else:

		while True:
			length = len(singal_list)
			# print "length: ", length
			singal_list = having_lableword_count_list(singal_list, threshold)
			# print 'singal_list', singal_list

			if singal_list == length:		# 如果返回的是数值, 并且值和列表长度一样, 就证明所有标记词, 都只能各自在自己的簇中, 不存在于一个簇中
				# print '===========length================='
				for i in range(length):
					thresholdCount.append(1)
				# print 'return thresholdCount=============================================', thresholdCount
				return thresholdCount
					
			else:
				thresholdCount.append(length - len(singal_list))
				# print '=========thresholdCount:=========', thresholdCount

	# print count_keyword_distance
	# print maxCount

	# return maxCount		#返回最大的个数.



########################################################################

'''
						这是第三类 
	第二种: 

	记录关键词 和 高频词 共同计入权值, 并且将句子中的所有关键词都加入计算. 
	句子还是用关键词去标记, 并取出.
		(a)是一个阈值中,就平方; 
		(b)不是一个阈值内的, 分别计算; 
		(c)原则,保证同一个词不能进入2个簇中
	并且加入了规则 --->> 只有1个关键词的舍去的规则.
	#如果句子大于40个词, 就放弃
'''
#函数参数: 	1 关键醋, 2 高频词汇, 3 文章分词之后--句子列表, 
#			4: 摘录句子的数量, 5: 阈值的大小 ,默认为 5 threshold, 
#			6: 句子的阈值, 句子分词之后的长度,超过这个限度,就舍去
########################################################################

def Third_Text_Abstract_B(keywords, high_frequency_vocabulary, sentence_for_map, sentenceNum, threshold = 7, lengthSenctenceMax = 40):
	# 1 获取关键词表
	wordlist = keywords
	# 2 获取有关键词的句子
	count = 0				# 作为标号, 进行分句的key,
	signSentence_dict = {}	# 保存有标记词的句子.

	#获取含有标记词的句子 字典. key 保存出现的顺序, value 保存句子.
	signSentence_dict = having_mark_sentence_in_Clause(signSentence_dict, wordlist, sentence_for_map)

	#阈值为7, 为一簇, 计算方式有很多种,这里选择最简单的方式, 计算一段话中, 最大的一簇, 所包含的关键词的个数.
	weightMap = {}		# 保存权值的字典
	weightMap_only_Count = {}
	for (num, sentence_list) in signSentence_dict.items(): 
		singal_list = []		# 保留关键词的位置的列表, 例如:关键词在第10个位置, 那么就把10, 存入列表
		singal_num = 0
		for word in sentence_list:			# 遍历句子, 用句子内的分词去匹配标记词, 看是否存在
			singal_num = singal_num + 1   	# 遍历单词, 加1. 举例: 1 和 7是, 7 - 1 = 6 < 阈值.即可. 防止出现 7 - 0 = 7 情况, 这事实上已经8个了.
			if word in wordlist:
				singal_list.append(singal_num)

		if len(singal_list) == 1:			# 并且加入了句子, 只有1个关键词的舍去的规则.
			continue
		# print "singal_list  ",num , '===', singal_list		
		'''
				# 获取一句话中, 簇中关键词个数的列表,  
			#举例:[3, 2, 1, 1] 意义就是: 包含一个簇内有3个标记词, 一个簇内2个, 剩下两个簇分别包含1个.
		'''
		countMaxNum_list = having_all_keywords_in_threshold(singal_list, threshold)		
		# print 'countMaxNum_list', countMaxNum_list
		weight = 0.0
		for countNum in range(0, len(countMaxNum_list)):		# 遍历 并计算 梯度的 权值
			# print countMaxNum_list[countNum],
			weight = weight + countMaxNum_list[countNum] * countMaxNum_list[countNum] * 1.0 / threshold
		# print 
		weightMap[num] = weight * weight * 1.0 / len(sentence_list)


	sorted_high_weight_sentence = sorted(weightMap.iteritems(), key=operator.itemgetter(1), reverse=True)  	# 按照权值排序	

	show_result_sentence(sorted_high_weight_sentence, signSentence_dict, sentenceNum, lengthSenctenceMax)	# 输入筛选出来代表摘要的句子.




########################################################################

'''
						第四类
第一种:

		在簇中获取关键词, 将簇截取出来. 组成中文摘要
规则:		
	(a) 获取关键句子, 通过关键词
	(b) 分词聚类, 一个句子, 最少有2个关键词, 只有一个关键词的句子, 过滤掉.
	(c) 将句子中包含关键词最多的簇, 从句子中抽离出来, 抽取的时候, 加入扩展的规则,这样防止一个句子中出现两个相同的权值,
		如果假如扩展一样还是相同, 就按照最先出现保留. 进行排序. 

		抽取规则: 从标记开始, 到','或者'.' 结束.
		
		排序的规则: 标记词的个数的平方 除以 截取出句子的长度.

	(d) 用截取句子的片段, 按照出现顺序, 组成一个摘要.
'''
########################################################################
#函数参数: 1 关键醋, 2 高频词汇, 3 文章分词之后--句子列表, 4: 摘录簇的数量, 5: 阈值的大小 ,默认为 5 threshold, 6: 句子的阈值, 句子分词之后的长度,超过这个限度,就舍去
########################################################################
def Fourth_Text_Abstract_A(keywords, high_frequency_vocabulary, sentence_for_map, clusterNum, threshold = 7, lengthSenctenceMax = 40):
	# 1 获取关键词表
	wordlist = keywords
	# 2 获取有关键词的句子
	count = 0				# 作为标号, 进行分句的key,
	signSentence_dict = {}	# 保存有标记词的句子.
	output_TextAbstract = {} # 保存输出的摘要

	#获取含有标记词的句子 字典. key 保存出现的顺序, value 保存句子.
	signSentence_dict = having_mark_sentence_in_Clause(signSentence_dict, wordlist, sentence_for_map)

	# 标记词扩充
	wordlist = keywords + high_frequency_vocabulary

	#阈值为7, 为一簇, 计算方式有很多种,这里选择最简单的方式, 计算一段话中, 最大的一簇, 所包含的关键词的个数.
	weightMap = {}		# 保存权值的字典
	weightMap_only_Count = {}
	for (num, sentence_list) in signSentence_dict.items(): 
		singal_list = []		# 保留关键词的位置的列表, 例如:关键词在第10个位置, 那么就把10, 存入列表
		singal_num = 0
		for word in sentence_list:			# 遍历句子, 用句子内的分词去匹配标记词, 看是否存在
			singal_num = singal_num + 1   	# 遍历单词, 加1. 举例: 1 和 7是, 7 - 1 = 6 < 阈值.即可. 防止出现 7 - 0 = 7 情况, 这事实上已经8个了.
			if word in wordlist:
				# print "关键词", word
				singal_list.append(singal_num)

		if len(singal_list) == 1:			# 并且加入了句子, 只有1个关键词的舍去的规则.
			continue
		# print "singal_list  ",num , '===', singal_list		

		length = len(singal_list)		# 标记词的个数
		count_keyword_distance = []		# 保存关键词之间的距离

		for i in range(length - 1):		# 这里只遍历了总长度减一,因为最后一个无法做差了.
			count_keyword_distance.append(singal_list[i + 1] - singal_list[i])

		# print count_keyword_distance
		# 关键词之间的距离个数, 等于关键词个数 - 1 
		len_distance = 0	# 记录词语之间的距离, 与阈值做比较
		count = 0 			# 记录每次遍历的包含个数.
		singla_del = 0		# 用来标记抽取的起始的词.
		maxCount = 0		# 记录列表中 簇中包含的最大分词个数

		for i in range(length - 1):			# 这里只遍历了总长度减一,因为最后一个无法做差了.
			if count_keyword_distance[i] <= threshold:
				count = 2		# 因为这是差值节点, 一个差值, 就包含2个节点.
				
				if maxCount < count:
					maxCount = count
					# print 'maxCount', maxCount
					singla_del = i 	# 保存删除词的其实位置, 因为被标记后的词, 就已经被取出了, 不能从新计入下一次循环
				len_distance = count_keyword_distance[i]  	# 保存距离

				for j in range(i + 1, length - 1):
					if len_distance + count_keyword_distance[j] <= threshold:	# 继续叠加词语之间的距离, 若依旧小于阈值,就在 加1
						count = count + 1

						if maxCount < count:			# 若此时标记词个数 大于 最大标记词个数, 就进行赋值.
							maxCount = count
							# print 'maxCount', maxCount
							singla_del = i 			# 保存删除词的其实位置, 因为被标记后的词, 就已经被取出了, 不能从新计入下一次循环
					
						len_distance = len_distance + count_keyword_distance[j]
					else:
						break


		if maxCount == 0:		# 如果截取长度是0, 就意味着没有2个或者2个以上的标记词在一个簇, 就算有多个标记词在句子中, 也是分散来. 
			continue

		# print 'singla_del: 抽取的起始位置:', singla_del, 'maxCount:截取长度', maxCount
		# print '句子中的起始位置是:', singal_list[singla_del], "结束位置是:", singal_list[singla_del + maxCount - 1]

		start = singal_list[singla_del] - 1 			# 起始位置
		end = singal_list[singla_del + maxCount - 1]	# 结束位置
		
		# punt_list = '[ • （ “ 《 ：'.decode('utf8')
		punt_list = ','.decode('utf8')
		cut_sentence_list = []		# 临时保存切割的句子

		for i in range(start, len(sentence_list)):
			if i >= end and sentence_list[i] in punt_list:		# 遇到标点符号退出.
				# print '。'
				cut_sentence_list.append('。')
				break
			# print sentence_list[i],
			cut_sentence_list.append(sentence_list[i])
			# if i >=  end + threshold + threshold/2 + 1:				# 第一种退出方式, 从最后一个关键词的位置过后, 超过了一倍阈值还没有标点符号结束,就退出
			# 	break

		# print " =========== ::::::", maxCount * maxCount * 1.0 / len(sentence_list)
		weight = 1.0
		weight = maxCount * maxCount * 1.0 / len(sentence_list)

		output_TextAbstract[weight] = cut_sentence_list					# 初始化将要保存的句子

		# print "'=============",  output_TextAbstract[num]


	sorted_high_weight_sentence = sorted(output_TextAbstract.iteritems(), key=lambda asd:asd[0], reverse = True)	

	singalBreak = sentenceNum		#选择7句作为文章摘要
	print '一共多少个句子', len(signSentence_dict)

	for (key, value) in sorted_high_weight_sentence:	#选择权值高的句子编号

		singalBreak = singalBreak - 1				
		for word in value:
			print word,
		print
		if singalBreak == 0:
			break


'''
						第四类  
第二种:

		在簇中获取关键词, 将簇截取出来. 组成中文摘要
规则:		
	(a) 获取关键句子, 通过关键词
	(b) 分词聚类, 一个句子, 最少有2个关键词, 只有一个关键词的句子, 过滤掉.
	(c) 将句子中包含关键词最多的簇, 从句子中抽离出来, 抽取的时候, 加入扩展的规则,这样防止一个句子中出现两个相同的权值,
		如果假如扩展一样还是相同, 就按照最先出现保留. 进行排序. 

		截取规则是: 一个句子内, 只截取出一段.
			但是加一条规则, 如果临近的词距离相加, 如果小于 2个簇的长度, 就将临近的词也假如截取范围. 
				扩展的起始位置是, 从最大簇的起始位置开始, 结束位置: 和簇结束的最后一个位置, 做前后的2个扩展点.
				扩展的阈值被设置为逐级递减 : 暂时设定为--1/2递减! 举例: 7 阈值, 第二次就是 3, 然后是 1....
					例子: [5,2,3,3,1,2,2,2,5,3,1]--->假定簇为7长度.
				获取的开始位置应该是:4, 结束位置应该是:7 ( 这里从0 开始计算)
					(1):从第5位向前扩展, (3, 3 被选中, 因为7/2=3 所以,2个被选中. 就是 2,3,3), 
					(2):从第8位向后扩展(5 被选中, 7/2=3 3被选中, 3/2=1, 1被选中).
					(3):最后选中的是 [2,3,3,1,2,2,2,5,3,1],这串序列.
		
		排序的规则: 标记词的个数 除以 截取出的长度.

	(d) 用截取句子的片段, 按照出现顺序, 组成一个摘要.
'''


########################################################################



if __name__ == '__main__':
	t1 = time.time()
	# print t1

	url = 'foo.txt'
	#获取去掉空白的中文文档字符串
	strReContent = obtainKeywords.ReadFile(url)       
	#通过tf-idf和textRank获取关键词,并去除停用词            			
	keywords = obtainKeywords.having_keywords(strReContent)						
	#获取高频词汇,在去除停用词和关键词后的高频词汇
	high_frequency_vocabulary = obtainKeywords.having_del_keywords_and_stop_high_frequency_word(strReContent)	   
	#获取高频词汇的函数, 只去除高频词汇列表中停用词.
	having_del_stop_high_frequency_word = obtainKeywords.having_del_stop_high_frequency_word(strReContent)			
	#先读取文章中的数据,然后进行分句,返回分句之后的列表
	sentences_list = divideSentence.divideSentence(url)			


	for word in high_frequency_vocabulary:
		print word, 
	print

####################	第 0 种方式
	sentenceNum = 7		#摘录句子的个数
	zero_Text_Abstract(keywords, high_frequency_vocabulary, sentences_list, sentenceNum, False)

# ####################  	第一种摘录方式
	sentenceNum = 7		#摘录句子的个数
	fisrt_Text_Abstract(keywords, high_frequency_vocabulary, sentences_list, sentenceNum)
# ####################  	第二种摘录方式
	sentenceNum = 7		#摘录句子的个数
	second_Text_Abstract(keywords, high_frequency_vocabulary, sentences_list, sentenceNum)	
####################		第三种摘录 A方式
	print " " * 20, "第三种摘录 A方式"
	sentence_for_map = divideSentence.divide_sentence_for_Map(strReContent)			# 获取文章分句以后的字典. key-->句子的顺序, value --> 是列表, 保存的时候分词为单位的列表
	sentenceNum = 5				# 摘录句子的个数, 作为摘要
	threshold = 5				# 阈值, 就是判断簇的大小, 7个构成一个簇, 判断一个句子, 簇权值最大.
	lengthSenctenceMax = 40 	# 选择句子的最大长度
	Third_Text_Abstract_A(keywords, high_frequency_vocabulary, sentence_for_map, sentenceNum, threshold, lengthSenctenceMax)
####################		第三种摘录 B方式
	print  " " * 20, "第三种摘录 B方式"
	sentence_for_map = divideSentence.divide_sentence_for_Map(strReContent)			# 获取文章分句以后的字典. key-->句子的顺序, value --> 是列表, 保存的时候分词为单位的列表
	sentenceNum = 5				# 摘录句子的个数, 作为摘要
	threshold = 5				# 阈值, 就是判断簇的大小, 7个构成一个簇, 判断一个句子, 簇权值最大.
	lengthSenctenceMax = 40 	# 选择句子的最大长度
	Third_Text_Abstract_B(keywords, high_frequency_vocabulary, sentence_for_map, sentenceNum, threshold, lengthSenctenceMax)		
####################
	print  " " * 20, "第四种摘录 B方式"
	sentence_for_map = divideSentence.divide_sentence_for_Map(strReContent)			# 获取文章分句以后的字典. key-->句子的顺序, value --> 是列表, 保存的时候分词为单位的列表
	sentenceNum = 5		# 摘录句子的个数, 作为摘要
	threshold = 7		# 阈值, 就是判断簇的大小, 7个构成一个簇, 判断一个句子, 簇权值最大.
	lengthSenctenceMax = 40 	# 选择句子的最大长度
	Fourth_Text_Abstract_A(keywords, high_frequency_vocabulary, sentence_for_map, sentenceNum, threshold, lengthSenctenceMax)	

####################

	print
	t2 = time.time()
	# print t2
	tm_cost = t2 - t1
	print '程序运行时间', tm_cost




























