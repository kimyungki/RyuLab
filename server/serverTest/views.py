from django.shortcuts import render

from django.http import HttpResponse

import json
import tensorflow as tf
import csv
import pandas as pd
import time
import datetime
import numpy as np

# Create your views here.
# subprocess.call(['C:\\Users\\lexsh\\Desktop\\stockProject\\stockpython\\dist\\nowstock.exe'])

def index(request):
    return render(request, 'serverTest/index.html')


#과거 캔들 차트 그리기
def output(request):
    line_counter = 0
    header = []
    customer_list = []
    i=0
    file = open("A000660_candle.csv", "r")
    for line in file:
         customer_list.append(line.strip('\n'))

    del customer_list[0]

    return HttpResponse(json.dumps(customer_list), content_type="application/json")


def predict(k):
	past=pd.read_csv('C:/Users/lexsh/Desktop/pastStock/A000660_pastStock.csv')  # 과거데이터 읽음
	del past["date"]
	del past["time"]
	past=past.values.tolist()  #이중리스트
	now =pd.read_csv('A000660_now.csv')  #실시간데이터

	del now["time"]
	now = now.values.tolist()
	past.append(now[k])
	past=past[-30:]
	return past

def test(request):
	k = 0
	while True:
		test = predict(k)
		print(test)
		tf.reset_default_graph()
		test = np.asarray(test, dtype=np.float64)
		min = np.min(test, 0)
		max = np.max(test, 0)
		def MinMaxScaler(data):
		    numerator = data - min
		    denominator = max - min
		    # noise term prevents the zero division
		    return numerator / (denominator + 1e-7)
		def MaxMinScaler(data):
		    return data * ( max - min) + min
		# test = test[::-1]#역순
		testX =MinMaxScaler(test)
		# train Parameters
		seq_length = 30                                 # sequence = 7(앞에 7개값 있을 것.)
		data_dim = 2                                    # input data는 한번에 들어감
		hidden_dim = 10                                 # 10개 hidden 있을 것.
		output_dim = 1                                  # output = 1
		learning_rate = 0.01
		iterations = 500
		# input place holders
		X = tf.placeholder(tf.float32, [None, seq_length, data_dim]) # None = batch_size
		Y = tf.placeholder(tf.float32, [None, 1])
		# build a LSTM network
		cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
		outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
		Y_pred = tf.contrib.layers.fully_connected(outputs[:, -1], output_dim, activation_fn=None)  # output은 마지막 하나만 쓰겠다
		# cost/loss
		loss = tf.reduce_sum(tf.square(Y_pred - Y))  # sum of the squares
		# optimizer
		optimizer = tf.train.AdamOptimizer(learning_rate)
		train = optimizer.minimize(loss)
		# RMSE
		targets = tf.placeholder(tf.float32, [None, 1])
		predictions = tf.placeholder(tf.float32, [None, 1])
		rmse = tf.sqrt(tf.reduce_mean(tf.square(targets - predictions)))
		saver = tf.train.Saver()
		sess = tf.Session()
		saver.restore(sess, 'A000660-model')                         # 지정한 cehckpoint 변수값 복구
		test_predict = sess.run(Y_pred, feed_dict={X: [testX]})

		f = open("test1.csv","a", encoding="cp949", newline='')
		field_name_list = ['stock']
		writer = csv.DictWriter(f, fieldnames=field_name_list)
		writer.writerow(
			{'stock':MaxMinScaler(test_predict)[0][1]})
		f.close()


	k = k+1
		

	t = ['a','b']
	return HttpResponse(json.dumps(t), content_type="application/json")

def predict3(request):
    line_counter = 0
    test1_counter = 0
    test2_counter = 0
    i = 0
    header = []
    customer_list = []
    now = []
    pre = []
    file = open("A000660_now.csv", "r")
    for line in file:
        now.append(line.strip('\n'))
        test1_counter = test1_counter + 1

    file2 = open("test1.csv", "r")
    for line in file2:
        pre.append(line.strip('\n'))
        test2_counter = test2_counter + 1

    customer_list.append(now)
    customer_list.append(pre)
    print("들어옴(sk하이닉스)")
    return HttpResponse(json.dumps(customer_list), content_type="application/json")