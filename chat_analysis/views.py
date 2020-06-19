from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect,HttpResponse
from django.core.files.storage import FileSystemStorage
import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



import os
import sys
def index(request):
    return render(request,"index.html")




def clean(words):
    return dict([(word, True) for word in words])




def process(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['data']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
      
        f = open('model', 'rb')
        classifier = pickle.load(f)
        f.close()
        opinion = {}

        f = open('user_data/'+uploaded_file.name, 'r')
        pos, neg = 0, 0
        for line in f:
            print(line)
            try:
                chat = line.split(']')[1].split(':')[1]
                name = line.split(']')[1].split(':')[0]
                if opinion.get(name, None) is None:
                    opinion[name] = [0, 0]
                res = classifier.classify(clean(chat))
                print(name, res, chat)
                if res == 'positive':
                    pos += 1
                    opinion[name][0] += 1
                else:
                    neg += 1
                    opinion[name][1] += 1
            except:
                pass

        neg = abs(neg)
        sizes = [15, 30]
        labels = ['positive', 'negative']
        explodes = (0, 0.1)
        colors = ['#66b3ff', '#ff9999']
        sizes = [pos, neg]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, explode=explodes, autopct='%1.1f%%',  colors=colors, shadow=True, startangle=90)
        plt.title('Chat Sentiment Analysis Overall')







        print(pos,neg)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

       # return render(request, 'graphic.html', {'graphic': graphic})





        names, positive, negative = [], [], []
        for name in opinion:
            names.append(name)
            positive.append(opinion[name][0])
            negative.append(opinion[name][1])
        ind = np.arange(len(names))
        width = 0.3
        max_x = max(max(positive), max(negative)) + 2

        fig = plt.figure()
        ax = fig.add_subplot()

        yvals = positive
        rects1 = ax.bar(ind, yvals, width, color='#66b3ff')
        zvals = negative
        rects2 = ax.bar(ind + width, zvals, width, color='#ff9999')

        ax.set_xlabel('Names')
        ax.set_ylabel('Sentiment')

        ax.set_xticks(ind + width)
        ax.set_yticks(np.arange(0, max_x, 1))
        ax.set_xticklabels(names,rotation=90)
        ax.legend((rects1[0], rects2[0]), ('positive', 'negative'))
        ax.set_title('Chat Sentiment Analysis Individual')
        fig.set_size_inches(12, 10, forward=True)


        for rect in rects1:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 0.5 * h, '%d' % int(h),
                    ha='center', va='bottom')

        for rect in rects2:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 0.5 * h, '%d' % int(h),
                    ha='center', va='bottom')

        buffer2 = BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        image_png2 = buffer2.getvalue()
        buffer2.close()

        graphic2 = base64.b64encode(image_png2)
        graphic2 = graphic2.decode('utf-8')

        return render(request, 'graphic.html', {'full': graphic,'indi':graphic2})

    return render(request, "index.html")





