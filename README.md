# Assignment2-WishingWell
must start mongodb is either "mongod" or "sudo service mongod start"
must run "sudo hciconfig hci0 piscan" every reboot
run as "sudo python3 bridge.py"

--Bluetooth phone Input/Output--
p:<QUEUE_NAME> "<MESSAGE_TEXT>"
c:<QUEUE_NAME>
h:<QUEUE_NAME>
--examples--
p:events "what is happen"
p:food "when is dinner"
p:food "i like burgers"
h:messages
h:food
c:events
(output to phone) what is happen
h:events
c:food
(output to phone) when is dinner
c:food
(output to phone) i like burgers