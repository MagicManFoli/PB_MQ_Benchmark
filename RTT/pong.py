#!python3

import RTT_timeslice_pb2 as timeslice
import zmq

from multiprocessing import Process

# Ports between 49152 & 65535 are "free" ports

# --- constants ---

# switched from ping
pub_port = 50404  # choose however you want
sub_port = 50403

topic = "Benchmark"
publisher = "localhost"

# --- functions ---


# called in response to other message
def pub(msg):
    msg_string = msg.SerializeToString()  # bytes
    s_pub.send_multipart((topic.encode('utf-8'), msg_string))


def forward():
    while True:
        c = s_sub.recv_multipart()  # blocking, RTT from here

        recv_topic, recv_msg = c
        msg_in.ParseFromString(recv_msg)

        pub(msg_in) # RTT stopped

        # delayed console to minimise RTT
        print("message {} forwarded".format(msg_in.msg_id))


# --- Main ---

print("\n --- Welcome to PB_MQ_Benchmark: Pong --- \n")
print("Subscribing to topic '{}' at '{}' on port '{}'\n".format(topic, publisher, pub_port))

print("Starting Socket")

context = zmq.Context()
s_pub = context.socket(zmq.PUB)
s_sub = context.socket(zmq.SUB)

s_pub.bind("tcp://*:{}".format(pub_port))
s_sub.connect("tcp://{}:{}".format(publisher, sub_port))
s_sub.setsockopt_string(zmq.SUBSCRIBE, topic)

print("Creating message")

msg_in = timeslice.timeslice()      # used for sub

print("All ready, forwarding incoming:\n")

forward()   # blocking

print("Done.\n")

# -----------------------





