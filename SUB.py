#!python3

import timeslice_pb2 as TimeSlice
import zmq
import time

import csv

# b"" to get byte-string

# Ports between 49152 & 65535 are "free" ports

# --- constants ---

port = 50403    # choose however you want
topic = "Benchmark"
publisher = "localhost"

file_name = "values.csv"
# --- Main ---

print("\n --- Welcome to PB_MQ_Benchmark --- \n")
print("Subscribing to topic '{}' at '{}' on port '{}'\n".format(topic, publisher, port))

print("Starting Socket")

context = zmq.Context()
s = context.socket(zmq.SUB)

print("Connecting")

s.connect("tcp://{}:{}".format(publisher, port))
s.setsockopt_string(zmq.SUBSCRIBE, topic)

msg_in = TimeSlice.timeslice()

print("All ready, waiting to receive")

values = []

while True:
    c = s.recv_multipart()
    topic, msg = c
    msg_in.ParseFromString(msg)

    if msg_in.millis == 0 and msg_in.msg_id == 0:
        break

    values.append((msg_in.msg_id, msg_in.millis))

print("\nValue list:\n")

for elem in values:
    print("ID: {}, ms: {}".format(elem[0], elem[1]))

print("Exporting to {}".format(file_name))

with(open(file_name, 'w')) as csv_file:
    writer = csv.writer(csv_file, lineterminator='\n')
    writer.writerows(values)

print("Done.\n")
