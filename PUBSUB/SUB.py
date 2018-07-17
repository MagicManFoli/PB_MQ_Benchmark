#!python3

import timeslice_pb2 as timeslice
import zmq
import time

import csv

# b"" to get byte-string

# Ports between 49152 & 65535 are "free" ports

# --- constants ---

port = 50403    # choose however you want
topic = "Benchmark"
publisher = "localhost"

values_name = "values.csv"

# --- Main ---

print("\n --- Welcome to PB_MQ_Benchmark: SUB --- \n")
print("Subscribing to topic '{}' at '{}' on port '{}'\n".format(topic, publisher, port))

print("Starting Socket")

context = zmq.Context()
s = context.socket(zmq.SUB)

print("Connecting")

s.connect("tcp://{}:{}".format(publisher, port))
s.setsockopt_string(zmq.SUBSCRIBE, topic)

msg_in = timeslice.timeslice()

print("All ready, waiting to receive")

values = []

while True:
    c = s.recv_multipart()
    topic, msg = c
    msg_in.ParseFromString(msg)

    # extract values
    send_time = msg_in.millis
    msg_id = msg_in.msg_id

    if send_time == 0 and msg_id == 0:
        break

    curr_time = int(time.time() * 1000 * 10)
    diff_time = int(curr_time - send_time)

    values.append((msg_id, send_time, curr_time, diff_time))

print("\nValue list:")

for elem in values:
    print("ID: {}, send: {}, recv: {}, diff: {}".format(elem[0], elem[1], elem[2], elem[3]))

print("Exporting to {}".format(values_name))

with(open(values_name, 'w')) as csv_file:
    writer = csv.writer(csv_file, lineterminator='\n')
    writer.writerows(values)

print("Done.\n")
