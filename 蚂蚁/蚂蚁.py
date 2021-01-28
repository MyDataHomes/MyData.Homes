import json
import jieba
import collections
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from snownlp import SnowNLP

class Mail:
	def __init__(self):
		with open("qqmail.json", "r") as f:
			self.data = json.load(f)

	#词云
	def wc(self):
		content = ""
		for d in self.data:
			content += d["content"]
		cut = jieba.cut(content)
		result = " ".join(cut)
		w = WordCloud(background_color="white",
			font_path=r'YuGothB.ttc',
			width=500,
			height=350,
			max_font_size=60,
			min_font_size=1,
			mode="RGBA")
		w.generate(result)
		plt.figure("蚂蚁词云")
		plt.imshow(w)
		plt.axis("off")
		plt.show()

	# 邮件情感
	def top_sen(self):
		sens = []
		for d in self.data:
			s = SnowNLP(d["content"])
			sens.append(s.sentiments)
		sens.sort()
		x = [i for i in range(len(sens))]
		plt.figure("蚂蚁邮件情感")
		plt.plot(x, sens)
		plt.show()

	# 统计
	def cal(self):
		email = {}
		for d in self.data:
			e = d["email_addr"].split("@")
			e = e[1].split(".")
			if e[0] in email.keys():
				email[e[0]] += 1
			else:
				email[e[0]] = 1
		email_var = {}
		for d in email:
			if email[d] > 1:
				email_var[d] = email[d]
		x = []
		y = []
		for e in email_var:
			x.append(e)
			y.append(email_var[e])
		plt.figure("邮件发送统计")
		plt.bar(x, y, 0.5)
		plt.show()


if __name__=='main':
	m = Mail()
	print("正在绘制词云")
	m.wc()
	print("正在绘制邮件情感")
	m.top_sen()
	print("正在绘制邮件统计")
	m.cal()