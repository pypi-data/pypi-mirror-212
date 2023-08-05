import re
import jieba
import math
class Text:
    

    def preprocess_text(self,text):
        # 去除 HTML 标签
        text = re.sub('<[^<]+?>', '', text)
        
        # 分词处理
        words = jieba.cut(text)
        words = [w for w in words if w.strip()]
        
        # 停用词过滤
        stopwords = ['的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这']
        words = [w for w in words if w not in stopwords]
        
        return words

    def generate_word_frequency(self,words):
        # 计算词频
        word_frequency = {}
        for word in words:
            word_frequency[word] = word_frequency.get(word, 0) + 1
            
        return word_frequency

    def calculate_tf_idf(self,word_frequency, total_words):
        # 计算 tf-idf 值
        tf_idf = {}
        for word, frequency in word_frequency.items():
            tf = frequency / total_words
            idf = math.log(total_words / frequency)
            tf_idf[word] = tf * idf
            
        return tf_idf

    def suoduan(self,text, max_length=500):
        """
        将文本进行缩短
        Args:
            text:欲缩短文本
            max_length  : 缩短后最长字数，默认500
        Return:
            返回缩短后的文本
        """
        # 文本预处理
        words = self.preprocess_text(text)
        total_words = len(words)
        
        # 计算词频和 tf-idf 值
        word_frequency = self.generate_word_frequency(words)
        tf_idf = self.calculate_tf_idf(word_frequency, total_words)
        
        # 按 tf-idf 值降序排序
        sorted_words = sorted(tf_idf.items(), key=lambda x:x[1], reverse=True)
        
        # 生成精简文章
        shortened_text = []
        word_count = 0
        for i in range(total_words):
            if word_count >= max_length:
                break
            word = words[i]
            if word in [w[0] for w in sorted_words[:max_length]]:
                shortened_text.append(word)
                word_count += 1
        
        return ''.join(shortened_text)