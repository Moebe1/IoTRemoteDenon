#Credit:
#Forked from miketeachman/micropython-rotary
#https://github.com/miketeachman/micropython-rotary.git


import time
from rotary_irq_esp import RotaryIRQ

r = RotaryIRQ(pin_num_clk=12, pin_num_dt=13, min_val=0, max_val=99, reverse=True, range_mode=RotaryIRQ.RANGE_WRAP)

lastval = r.value()
while True:
  val = r.value()

  if lastval != val:
      lastval = val
      print('result =', val)

  time.sleep_ms(20)