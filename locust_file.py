from locust.stats import RequestStats
from locust import Locust, TaskSet, task, events
import os
import sys
from random import randint,random
import json
import time

from grpc.beta import implementations
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

 
class GrpcLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(GrpcLocust, self).__init__(*args, **kwargs)
 
class ApiUser(GrpcLocust):
     
    min_wait=900    # Min time between requests of each user
    max_wait=1100    # Max time between requests of each user
     
 
    class task_set(TaskSet):

        def on_start(self):
            print "on start"
 
        @task
        def get_prediction(self):
            host, port = '127.0.0.1:9000'.split(':')
            channel = implementations.insecure_channel(host, int(port))
            stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
            with open('/home/ubuntu/tensorflow-serving-gatling-extension/test.jpg', 'rb') as f:
                data = f.read()
                start_time = time.time()
                request = predict_pb2.PredictRequest()
                request.model_spec.name = 'inception'
                request.model_spec.signature_name = 'predict_images'
                request.inputs['images'].CopyFrom(
                    tf.contrib.util.make_tensor_proto(data, shape=[1]))
                result = stub.Predict(request, 5.0)  # 10 secs timeout
                #print(result)
                exception = result.exception()
                if exception:
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_failure.fire(request_type="grpc", name='inception', response_time=total_time, exception=e)
                else:
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_success.fire(request_type="grpc", name='inception', response_time=total_time, response_length=0)