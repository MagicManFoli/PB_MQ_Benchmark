#!python3

import timeslice_pb2 as timeslice
import zmq
import time

# b"" to get byte-string

# Ports between 49152 & 65535 are "free" ports

# --- constants ---

port = 50403    # choose however you want
topic = "Benchmark"

t_sleep_ms = 10

# --- Main ---


print("\n --- Welcome to PB_MQ_Benchmark --- \n")
print("Publishing to topic '{}' on port {}\n".format(topic, port))

print("Starting Socket")

context = zmq.Context()
s = context.socket(zmq.PUB)

s.bind("tcp://*:{}".format(port))   # publish on local

print("Creating message")

msg_out = timeslice.timeslice()
msg_out.msg_id = 0
msg_out.millis = int(time.time() * 1000 * 10)

print("All ready, starting to spam:\n")

time.sleep(1)

# safety shutoff if forgotten
for i in range(1, 50):
    
    msg_out.msg_id = i
    msg_out.millis = int(time.time() * 1000)

    msg = msg_out.SerializeToString()   # bytes
    s.send_multipart((topic.encode('utf-8'), msg))
    time.sleep(t_sleep_ms/1000)

msg_out.msg_id = 0
msg_out.millis = 0

msg = msg_out.SerializeToString()   # bytes
s.send_multipart((topic.encode('utf-8'), msg))

print("Done.\n")
