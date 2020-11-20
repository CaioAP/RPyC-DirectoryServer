# Lookup-RPYC
Automatic discovery of the application server

## Directory Server
Implements a directory server, based on the RPyC API, that keeps the addresses from applications connected to it.

Every connection stablished to the Directory Server creates a new thread on the process.

This server contains two methods:
* Register(name, address, port)
* Lookup(name)

### Register
Receives three parameters from the applications, containing firstly the name, then the IP address and the port.

This method stores the IP address and the port number in a dictionary, which the name of the applicaiton connected is the key of these values.

It looks like this:
```
registry = {}
registry[name] = (address, port)
```

### Lookup
This method receives the application name and return the registry values: IP address and port number.

As the key to the values is the name, it is possible to retrieve the data by passing it directly to the object:
```
return registry[name]
```

## Server Application

The server implements a class from RPyC API that connects to the Directory Server, then uses Sockets to retrieve its local IP address to later pass them to the Register method from the Directory Sever.

After the connectios it starts a loop to listen to incoming requests.

This class has also two methods:
* Append(data)
* Value()

### Append

This method receives the data as a parameter from the Client and pushes it to a list kept as global access in the Server class.

Imagine it like:
```
values = []
values = values + [data]
```

### Value

This method receives no arguments and just returns the values appended to the global variable `values`

```
return values
```

## Client Application

The Client implements its own class that uses RPyC to connect to the Directory Server and calls the method Lookup, passing it the name of the server desired and getting the IP address and port number.

See the lookup:
```
(addr, port) = conn_directory.root.exposed_lookup(<servername>)
```

The IP and port are then used to connect to the Server Application and the Client append some values.
```
conn = rpyc.connect(addr, port)
conn.root.exposed_append(2)
conn.root.exposed_append(4)
```

The values appended are printed as a reference that everything went ok!
