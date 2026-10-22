from vclocks import VectorClock

p0 = VectorClock(num_processes=3, process_id=0)
p1 = VectorClock(num_processes=3, process_id=1)
p2 = VectorClock(num_processes=3, process_id=2)

p0.increment()
message = p0.send_message()
p1.receive_message(message)

print(p0)
print(p1)
print(p2)