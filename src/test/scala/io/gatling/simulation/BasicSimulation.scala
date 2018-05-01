package io.gatling.simulation

import io.gatling.core.Predef.Simulation
import io.gatling.core.Predef._
import io.gatling.tensorflow.{TensorflowServingClientBuilder, TensorflowServingClientProtocol}
import io.grpc.netty.NettyChannelBuilder
import tensorflow.serving.PredictionServiceGrpc

class BasicSimulation extends Simulation {

  val host = "ec2-52-53-213-166.us-west-1.compute.amazonaws.com"
  val port = 9000
  val channel = NettyChannelBuilder.forAddress(host, port)
    .usePlaintext(true)
    .maxMessageSize(200 * 1024 * 1024)
    .build()

  val blockingStub = PredictionServiceGrpc.newBlockingStub(channel)

  val models = List(("mnist", 1))

  val inputParam = "images"
  val outputParam = "scores"

  val tfServingClientProtocol =
    new TensorflowServingClientProtocol(channel, blockingStub, models, inputParam, outputParam)

  val scn = scenario("Tensorflow Serving Client call").exec(TensorflowServingClientBuilder())

  setUp(scn.inject(rampUsers(1000) over (30 seconds))).protocols(tfServingClientProtocol)
}