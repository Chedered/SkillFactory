import pika
import json
import numpy as np
import math

try:
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host='rabbitmq'))
	channel = connection.channel()


	channel.queue_declare(queue='y_true')
	channel.queue_declare(queue='y_pred')

	def rmse(ts):
		try:
			with open(f'./logs/pred_logs/{ts}.txt', 'r') as pred_log:
				for line in pred_log:
					y_pred = float(line)

			with open(f'./logs/true_logs/{ts}.txt', 'r') as true_log:
				for line in true_log:
					y_true = float(line)

			MSE = np.square(np.subtract(y_true, y_pred)).mean() 

			RMSE = math.sqrt(MSE)

			answer_string = f'Для ID - {ts} получено значение RMSE - {RMSE}'
			with open('./logs/rmse_log.txt', 'a') as log:
				log.write(answer_string +'\n')
		
		except:
			pass

			
	def callback_pred(ch, method, properties, body):
		ts = list(json.loads(body).keys())[0]
		value = list(json.loads(body).values())[0]

		with open(f'./logs/pred_logs/{ts}.txt', 'w') as log:
			log.write(str(value))

		rmse(ts)
		
	def callback_true(ch, method, properties, body):
		ts = list(json.loads(body).keys())[0]
		value = list(json.loads(body).values())[0]

		with open(f'./logs/true_logs/{ts}.txt', 'w') as log:
			log.write(str(value))

		rmse(ts)

	channel.basic_consume(
		queue='y_pred', on_message_callback=callback_pred, auto_ack=True)

	channel.basic_consume(
		queue='y_true', on_message_callback=callback_true, auto_ack=True)

	print('...Ожидание сообщений, для выхода нажмите CTRL+C')
	channel.start_consuming()
	
except:
    print('Не удалось подключиться к очереди')