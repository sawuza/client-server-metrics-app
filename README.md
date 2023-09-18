# Client-server Metrics App

In large projects, with a large number of users, it is necessary to carefully observe all the processes occurring in it. Information about processes can be represented by various numerical indicators, for example: the number of requests to your application, the response time of your service to each request, the number of users per day, and others. We will call these different numerical indicators as metrics.

There are ready-made solutions for collecting, storing and displaying such metrics, e.g. Graphite, InfluxDB. I have developed my own system for collecting and storing metrics based on client-server architecture.

## Client

### Overview

It is necessary to implement the `Client` class, which will encapsulate the connection to the server, the client socket and methods for getting (get) and sending (put) metrics to the server. Sending and receiving data in the `get` and `put` methods must be implemented according to the protocol described above. The address pair `host` and `port`, as well as the optional argument `timeout` (which has the default value of `None`) must be passed to the constructor of the `Client` class. Connection to the server is established when creating an instance of the `Client` class and should not be broken between requests.

### Usage

```bash
>>> from client import Client

>>> client = Client("127.0.0.1", 8888, timeout=15)

>>> client.put("palm.cpu", 0.5, timestamp=1150864247)

>>> client.put("palm.cpu", 2.0, timestamp=1150864248)

>>> client.put("palm.cpu", 0.5, timestamp=1150864248)

>>> client.put("eardrum.cpu", 3, timestamp=1150864250)

>>> client.put("eardrum.cpu", 4, timestamp=1150864251)

>>> client.put("eardrum.memory", 4200000)

>>> print(client.get("*"))
```

## Server

### Overview

This code creates a tcp connection for the address `127.0.0.1:8888` and listens to all incoming requests. When a client connects, a new instance of the `ClientServerProtocol` class will be created, and when new data arrives, the `data_received` method of this object will be called.

### Usage

```bash
$: telnet 127.0.0.1 8888
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
> get test_key
< ok
< 
> got test_key
< error
< wrong command
< 
> put test_key 12.0 1503319740
< ok
< 
> put test_key 13.0 1503319739
< ok
< 
> get test_key 
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< 
> put another_key 10 1503319739
< ok
< 
> get *
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< another_key 10.0 1503319739
<
```
