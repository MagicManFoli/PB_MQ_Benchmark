#!python3

import RTT_timeslice_pb2 as timeslice
import zmq

import time
import csv

from multiprocessing import Process

# Ports between 49152 & 65535 are "free" ports

# --- constants ---

pub_port = 50403  # choose however you want
sub_port = 50404

topic = "Benchmark"
publisher = "localhost"

values_file = "values.csv"

# number of decimals
n_dec = 8

t_sleep_ms = 10

# --- functions ---


# called in response to other message
def pub(msg):
    msg_string = msg.SerializeToString()  # bytes
    s_pub.send_multipart((topic.encode('utf-8'), msg_string))


def recv():
        c = s_sub.recv_multipart()  # blocking, RTT from here

        recv_topic, recv_msg = c
        msg_in.ParseFromString(recv_msg)

        return msg_in


def get_time():
    return round(time.perf_counter(), n_dec)


# --- Main ---


print("\n --- Welcome to PB_MQ_Benchmark: Ping --- \n")
print("Subscribing to topic '{}' at '{}' on port '{}'\n".format(topic, publisher, pub_port))

print("I hope you started pong first, or else this is blocking indefinitely")

print("Starting Socket")

context = zmq.Context()
s_pub = context.socket(zmq.PUB)
s_sub = context.socket(zmq.SUB)

s_pub.bind("tcp://*:{}".format(pub_port))
s_sub.connect("tcp://{}:{}".format(publisher, sub_port))
s_sub.setsockopt_string(zmq.SUBSCRIBE, topic)

print("Creating message")

msg_in = timeslice.timeslice()      # used for sub
msg_out = timeslice.timeslice()     # used for pub

values = []

print("All ready, starting to spam:\n")

# wait for subscribers
time.sleep(1)


for i in range(1, 50):
    msg_out.msg_id = i

    send_time = get_time()
    pub(msg_out)

    msg_in = recv()     # blocking, RTT happens here

    # extract values

    msg_id = msg_in.msg_id

    curr_time = get_time()
    diff_time = round(curr_time - send_time, n_dec)

    values.append((msg_id, send_time, curr_time, diff_time))

    time.sleep(t_sleep_ms / 1000)

print("Send & received all, converting to usable data")

print("\nValue list:")

for elem in values:
    print(f"ID: {elem[0]:>3}, send: {elem[1]:<{n_dec + 3}}, recv: {elem[2]:<{n_dec + 3}}, diff: {elem[3]:<{n_dec + 3}}")

print("Exporting to {}".format(values_file))

with(open(values_file, 'w')) as csv_file:
    writer = csv.writer(csv_file, lineterminator='\n')
    writer.writerows(values)

print("Done.\n")

# -----------------------





