#!usr/bin/python
#coding=utf-8

import urllib2
import sys, time, re
import sys
import chardet 
import jieba
jieba.load_userdict("userdict.txt")
import jieba.analyse
import jieba.posseg as pseg
import os
jieba.initialize()
import operator
reload(sys);
sys.setdefaultencoding('utf8');
import divideSentence


#判断 文本(字符串)的变法类型
def obtainTextType(ff):
    # import chardet 
    enc = chardet.detect(ff) 
    return enc['encoding']  #返回文件类型

#文件编码类型判断
def obtainFileType(filepath):
    # import chardet 
    tt = open(filepath, 'rb') 
    ff = tt.readline()        #这里试着换成read(5)也可以，但是换成readlines()后报错 
    tt.close() 
    return obtainTextType(ff)  #返回文件类型

#读取文件, 返回去掉空格和空白的字符串 
def ReadFile(url):      #url文件的路径
    # print obtainFileType(url)
    if obtainFileType(url) == 'GB2312':
        #.decode("gbk").encode('utf-8') 以gbk编码格式读取字符串（因为他就是gbk编码的）并转换为utf-8格式输出
        content = open(url, "rb").read().decode("gbk").encode('utf-8')
        # print obtainTextType(content)

    elif obtainFileType(url) == 'ascii':
        content = open(url, "rb").read().encode('utf-8')
        # print obtainTextType(content)

    else:
        # print obtainFileType(url)
        content = open(url, "rb").read()
        # print obtainTextType(content)

    strRe = re.sub('\s', '', content)   #用正则干掉所有的空白
    return strRe


#分词,对中文文章进行分词
def divide_text_words(content):
    #分词， 未登录词用veterbi分词
    words = list(jieba.cut(content, cut_all=False))
    #print "分词的总数：", len(words)
    #wordset = sorted(set(words))
    #print "不重复的单词数：", len(wordset)

    return words
    
    '''
    #将数据写入文件
    list = words
    fl = open('list.txt', 'wb')
    for i in range(len(list)):
        fl.write(list[i].encode('utf-8')+'--')
    fl.close()
    '''

# 获取停用词表,返回一个中文的停用词列表
def stopWords():
    #读取文件中的停用词,返回停用词列表
    cn_stop_words_file = open("extra_dict/cn_stop_words.txt", "rb").readlines()
    cn_stop_word_list = []      # 停用词,词表.
    for word in cn_stop_words_file:
        word = re.sub('\s', '', word)   #用正则干掉所有的空白
        #print word
        cn_stop_word_list.append(word.decode('utf-8'))

    return cn_stop_word_list

#去掉停用词,参数是要处理的词列表 和 停用词列表,  返回值是处理之后的列表
def delStopWords(words, stopWords):
    reWords = []
    for word in words:
        if word in stopWords:
            continue
        else:
            reWords.append(word) 

    return reWords


#获取关键词列表,并返回关键词列表
def keywords(content):
    # #TF-IDF
    # jieba.analyse.set_idf_path("extra_dict/idf.txt.big");
    # tf_idf_tags = jieba.analyse.extract_tags(content, topK = 10)
    # # print "TF-IDF 未去除停用词, 获取10个关键词"
    # print(",".join(tf_idf_tags))

    #去掉停用词 TF-IDF 语言,研究,汉语,中文信息处理,汉字
    jieba.analyse.set_idf_path("extra_dict/idf.txt.big");
    jieba.analyse.set_stop_words("extra_dict/cn_stop_words.txt")
    tf_idf_stop_words_tags = jieba.analyse.extract_tags(content, topK = 10)
    # print type(tf_idf_stop_words_tags)
    # print "TF-IDF 去除停用词"
    # print(",".join(tf_idf_stop_words_tags))

    #TextRank 分词
    # print "TextRank, 获取10个关键词"
    #TextRank_words = []
    TextRank_words = jieba.analyse.textrank(content)
    # print type(TextRank_words)
    # key_words_listprint(",".join(TextRank_words))

    keywords_list = TextRank_words + tf_idf_stop_words_tags
    keywords = list(set(keywords_list))
    return keywords



#统计分词,统计词频. 参数:  words 需要统计的分词之后的列表,  
#                       high_frequency_level:高频词汇的等级,数值越小,统计的量越大.
def having_high_frequency_vocabulary(words, high_frequency_level):
# 统计分词结果后，每个个分词的次数
    
    wordsDict = {}
    DictsMaxWordlen = 0
    singal = ''
    for w in words:
        if wordsDict.get(w) == None:
            wordsDict[w] = 1
        else:
            wordsDict[w] += 1
            
        if DictsMaxWordlen <= wordsDict[w]:
            DictsMaxWordlen = wordsDict[w]
            # global singal 
            singal = w
            #print w

    #print "分词最多重复的次数：%d" % DictsMaxWordlen , "分词是: %s" % singal
    #按字典值排序（默认为升序），返回值是字典{key, tuple}
    sorted_wordsDict = sorted(wordsDict.iteritems(), key=operator.itemgetter(1))
    # print sorted_wordsDict[2][0]

#按照统计次数相同的词,进行分组.

    classNumWord = {}       #保存分组之后的字典, 例如: {1:['1', '2'], 2:['文化', '历史'], }
    for w in sorted_wordsDict:
        if classNumWord.has_key(w[1]) == True:
            if w[0] not in classNumWord[w[1]]:  
                classNumWord[w[1]].append(w[0])
        else:
            classNumWord[w[1]] = []
            classNumWord[w[1]].append(w[0])

    #将字典排序，按照升序, 通过键排序，
    sort_classNumWord = sorted(classNumWord.iteritems(), key=lambda asd:asd[0], reverse = False)
    wordsList = []  #存取单词的列表
    
    #根据自己的想法,设置前多少级的词频,进入统计
    for num in range(int(len(sort_classNumWord) * high_frequency_level), len(sort_classNumWord)):
        #print sort_classNumWord[num][0]
        wordsList = wordsList + sort_classNumWord[num][1]       

    # print "数字大小", int(len(sort_classNumWord) * high_frequency_level)
    # print len(wordsList)
    return wordsList
    # print type(sort_classNumWord)
    # print type(sort_classNumWord[20])
    # print 'sort_classNumWord[20][1]', sort_classNumWord[20][1]
    # print type(sort_classNumWord[20][1])

    # print sort_classNumWord[20][1][0]
    # print sort_classNumWord[20][1][1]

    # wordslength = 0             #分词的总数
    # worldsNum = 0               #分词有多少个不同的词或词组
    # wordsFequencelist = {}      #分词出现的频次等级，从1到N次,并存储所对应等级的词语个数

    # for w in sort_classNumWord:
    #     worldsNum += w[0]
    #     wordslength += len(w[1]) * w[0]
    #     wordsFequencelist[w[0]] = []
    #     wordsFequencelist[w[0]].append(len(w[1]))

    # sort_wordsFequencelist = sorted(wordsFequencelist.iteritems(), key=lambda asd:asd[0], reverse = False)

    # print '\t\t频率是单词出现的次数, 次数是出现对应次数的所有不同单词的总和'
    # lenWords = 0
    # for wordsFequence in sort_wordsFequencelist:
    # 	lenWords += 1
    # 	print '频率:{0:<4} 词数:{1:>6}'.format(wordsFequence[0], wordsFequence[1]), " ",
    # 	if lenWords % 4 == 0:
    # 		print

    # print 
    # print "一共有".decode('utf-8'), worldsNum, '个不同的词或词组'.decode('utf-8')
    # print "一共有".decode('utf-8'), wordslength, '个词或词组'.decode('utf-8')


#获取高频词汇的函数, 只去除列表中停用词.
def having_del_stop_high_frequency_word(strReContent):
    stop_words_list = stopWords()                       #获取停用词
        
    #获取高频词汇,设置阈值, 取出高频词汇, 消除 关键词和停用词 共同构成的词表, 剩下的高频词汇.
    words = divide_text_words(strReContent)                                                # 对文章进行分词
    high_frequency_vocabulary = having_high_frequency_vocabulary(words, 0.333)          # 计算词频, 取后等级, 全体等级数量的后2/3的所有词.
    high_frequency_words = delStopWords(high_frequency_vocabulary, stop_words_list)     # 获取删除停用词之后的词汇列表

    return high_frequency_words



#获取高频词汇的函数, 去除关键词和停用词的高频词汇, 参数是strReContent 文本.
def having_del_keywords_and_stop_high_frequency_word(strReContent):
    key_words_list = keywords(strReContent)             #获取关键词通过tf-idf和textRank
    stop_words_list = stopWords()                       #获取停用词
        
    #获取高频词汇,设置阈值,取出高频词汇,消除 关键词和停用词 共同构成的词表, 剩下的高频词汇.
    words = divide_text_words(strReContent)                                            # 对文章进行分词
    high_frequency_vocabulary = having_high_frequency_vocabulary(words, 0.333)      # 计算词频, 取后等级, 全体等级数量的后2/3的所有词.
    stop_words_list = list(set(stop_words_list + key_words_list))                   # 将关键词 和 停用词叠加, 合成停用词表
    high_frequency_delstopWords_list = delStopWords(high_frequency_vocabulary, stop_words_list)   #获取删除停用词之后的词汇列表

    return high_frequency_delstopWords_list


#获取关键词,通过tf-idf和textRank合成,在去除停用词
def having_keywords(strReContent):
    key_words_list = keywords(strReContent)             #获取关键词通过tf-idf和textRank
    stop_words_list = stopWords()                       #获取停用词
    keywords_del_stop_list = delStopWords(key_words_list, stop_words_list)   #获取删除停用词之后的词汇列表
    return keywords_del_stop_list




# ------------------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':

    #这里读取的文件是utf-8 和 gbk 文件, 暂不支持asscii码.
 
    #获取关键词,通过tf-idf和textRank合成,在去除停用词
    strReContent = ReadFile('DIPS-LY06-15339.txt')                   #获取去掉空白的中文文档字符串   
    # print obtainTextType(strReContent)

    key_words_list = keywords(strReContent)             #获取关键词通过tf-idf和textRank
    stop_words_list = stopWords()                       #获取停用词
    keywords_del_stop_list = delStopWords(key_words_list, stop_words_list)   #获取删除停用词之后的词汇列表
    print 
    print 'keywords_del_stop_list'
    for word in keywords_del_stop_list:
        print word
    print   
    
    # 获取高频词汇,设置阈值,取出高频词汇,消除 关键词和停用词 共同构成的词表, 剩下的高频词汇.
    words = divide_text_words(strReContent)                                         #对文章进行分词
    high_frequency_vocabulary = having_high_frequency_vocabulary(words, 0.333)      #计算词频,取后等级,2/3的所有词.
    stop_words_list = stop_words_list + key_words_list                              #将关键词和停用词叠加,合成停用词表
    # for i in range(0, len(stop_words_list)):
    #     stop_words_list[i] = stop_words_list[i].encode('utf8')

    # for i in range(0, len(high_frequency_vocabulary)):
    #     high_frequency_vocabulary[i] = high_frequency_vocabulary[i].encode('utf8')

    # print 'high_frequency_vocabulary'
    # for word in high_frequency_vocabulary:
    #     print word
    # print
    high_frequency_delstopWords_list = delStopWords(high_frequency_vocabulary, stop_words_list)   #获取删除停用词之后的词汇列表

    # print type(stop_words_list[1])
    # print type(high_frequency_vocabulary[1])
    # print 

    # high_frequency_delstopWords_list = []
    # for word in high_frequency_vocabulary:
    #     print '111111', word, type(word)
    #     # word = (word).decode('utf8')
    #     if word in stop_words_list:
    #         print 'continue'
    #         continue
    #     else:
    #         high_frequency_delstopWords_list.append(word) 


    #     # print divideSentence.obtainTextType(stop_words_list[1])


    print 
    print 'high_frequency_delstopWords_list'
    for word in high_frequency_delstopWords_list:
        print word


    print 
    print


