import pika
import json
import numpy as np
import time
from sklearn.datasets import load_diabetes
from datetime import datetime

X, y = load_diabetes(return_X_y=True)

while True:
	try:
		random_row = np.random.randint(0, X.shape[0]-1)
		ts = round(datetime.timestamp(datetime.now()))
		features_dict = {ts:list(X[random_row])}
		y_true_dict = {ts:y[random_row]}

		connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
		channel = connection.channel()

		channel.queue_declare(queue='Features')
		channel.queue_declare(queue='y_true')

		channel.basic_publish(exchange='',
								routing_key='Features',
								body=json.dumps(features_dict))
		print(f'Сообщение (ID - {ts}) с вектором признаков, отправлено в очередь')

		channel.basic_publish(exchange='',
								routing_key='y_true',
								body=json.dumps(y_true_dict))

		print(f'Сообщение (ID - {ts}) с правильным ответом, отправлено в очередь')
		connection.close()
		time.sleep(5)
	except:
		print('Не удалось подключиться к очереди')