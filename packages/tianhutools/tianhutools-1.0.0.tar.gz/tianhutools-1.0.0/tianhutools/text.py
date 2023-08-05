from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
class Text:
    def suoduan(self,text : str , ratio = 0.2) -> str:
        """
        对中文文本进行简单压缩

        Args:
            text (str): 待压缩的文本
            ratio (float): 压缩比例，保留原文本的 ratio 比例的句子

        Returns:
            str: 压缩后的文本摘要
        """
        # 中文文本分句
        sent_list = [s for s in text.split('\n') if len(s.strip()) > 0]
        for i in range(len(sent_list)):
            sent_list[i] = sent_list[i].strip()

        # 创建 PlaintextParser 对象，并指定使用 Tokenizer('chinese') 进行中文分词处理
        parser = PlaintextParser.from_string('\n'.join(sent_list), Tokenizer('chinese'))

        # 创建 LsaSummarizer 对象
        summarizer = LsaSummarizer()

        # 设置摘要长度
        n = int(len(sent_list) * ratio)

        # 生成摘要
        summary = []
        for sentence in summarizer(parser.document, n):
            summary.append(sentence._text)

        return ''.join(summary)