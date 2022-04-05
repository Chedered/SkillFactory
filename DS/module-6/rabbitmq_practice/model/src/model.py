import pika
import json
import pickle
import numpy as np

with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='Features')
    channel.queue_declare(queue='y_pred')

    def callback(ch, method, properties, body):
        ts = list(json.loads(body).keys())[0]
        print(f'Получен вектор признаков (ID - {ts})')
        features = list(json.loads(body).values())[0]
        pred = regressor.predict(np.array(features).reshape(1, -1))
        y_pred_dict = {ts:pred[0]}

        channel.basic_publish(exchange='',
                              routing_key='y_pred',
                              body=json.dumps(y_pred_dict))
        print(f'Предсказание (ID - {ts}) отправлено в очередь y_pred')


    channel.basic_consume(
        queue='Features', on_message_callback=callback, auto_ack=True)

    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()

except:
    print('Не удалось подключиться к очереди')