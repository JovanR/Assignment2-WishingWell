#repository.py
import rmq_params.py
import sys
import pika

# 10 for GPIO.BOARD or 11 for GPIO.BCM
gpioMode = sys.argv[2]
redPin = sys.argv[4]
greenPin = sys.argv[6]
bluePin = sys.argv[8]

