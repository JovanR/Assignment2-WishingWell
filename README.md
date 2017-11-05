# Assignment2-WishingWell
must start mongodb is either "mongod" or "sudo service mongodb start"
must run "sudo hciconfig hci0 piscan" every reboot
run as "sudo python3 bridge.py"


--Bluetooth phone Input/Output--
p:<QUEUE_NAME> "<MESSAGE_TEXT>"
c:<QUEUE_NAME>
h:<QUEUE_NAME>
--examples--
c:events "what is happen"
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

----checkpoints----
--bridge--
[Checkpoint 01] Connected to database 'squires' on MongoDB server at 'localhost'
[Checkpoint 02] Connected to vhost 'ex_vhost' on RMQ server at 'XXX.XXX.XXX.XXX' as user 'ex_user'
[Checkpoint 03] Created RFCOMM Bluetooth socket on port 1
[Checkpoint 04] Accepted RFCOMM Bluetooth connection from ('XX:XX:XX:XX:XX:XX', 1)
[Checkpoint p-01] Published message with routing_key: 'ex_status'
[Checkpoint p-02] Message: green
[Checkpoint 05] Sending Exchange and Queue names
[Checkpoint 06] Received RFCOMM Bluetooth data: b'p:events "what is happen"'
[Checkpoint p-01] Published message with routing_key: 'ex_status'
[Checkpoint p-02] Message: purple
[Checkpoint m-01] Stored document in collection 'events' in MongoDB database 'squires'
[Checkpoint m-01] Document: {'Subject': 'events'}

--repository--
[Checkpoint 01] Connected to vhost 'ex_vhost' on RMQ server at 'localhost' at user 'ex_user'
[Checkpoint 02] Consuming messages from 'ex_master' queue
[Checkpoint l-01] Flashing LED to green
[Checkpoint l-01] Flashing LED to purple
[Checkpoint 03] Consumed a message published with routing_key: 'events'
[Checkpoint 04] Message: what is happen
[Checkpoint l-01] Flashing LED to purple
3
4
l-01
3
4
l-01
