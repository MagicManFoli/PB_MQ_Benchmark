# PB_MQ_Benchmark
primitive benchmarking tools for ZeroMQ + protobuf

Dependencies: pyzmq, protobuf (both installed via pip)

# PUBSUB:
The publisher sends messages, the subscriber prints them to a CSV.
This is only useful when PUb & SUB are on the same host, otherwise the difference in system clock times skewes results.

# RTT (Round-trip-time):
Ping sends message to pong, which mirrors it back.
Both paths are realised through PUBSUB to increase realism to later applications.

Insert correct hosts to communicate between different stations.
