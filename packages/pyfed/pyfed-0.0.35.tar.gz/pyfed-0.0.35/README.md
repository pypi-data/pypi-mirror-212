# PyFed
PyFed is an open-source framework for federated learning. PyFed is fairly straightforward and brief in comparison to other federated learning frameworks. Furthermore, it allows running federated learning algorithms with any Tensorflow dataset on any preprocessed dataset. PyFed introduces several methods of federated learning implementation such as running multiple processes on a single machine and training on various systems. In addition, PyFed employs Tensorboard to demonstrate the history of training of each client and assess loss and accuracy of each client per round.
</br>
PyFed implements FL using sockets, processes, and threads. Simply put, each client will run its particular process and tries to establish a socket connection with the server, which also has its specific process. 
Once initiated, each connection will be handled by one thread of the server's process. Each thread will communicate with its respective client to receive the trained weights per round. 
Once they receive the result of one round, threads will return the weights to the server's process, which will arrive at a new model using the mentioned weights. The server will send the new model to the clients using newly initiated threads.
</br>
PyFed is mainly based on two classes:
 
- __FL_Server__: which represents the server to which clients communicate in a federated learning problem. The __train()__ function of this class handles socket connections and the FL policy. </br>
- __FL_Client__: which represents each client in a federated learning network. An object of this class handles training procedure of any global model on any local data.

PyFed can run federated learning in 2 ways: 

1. Running FL only on one system and using separate processes.
2. Running FL on multiple systems. 

__Tutorials and installation guides are mentioned on [PyFed webpage](https://pyfed.readthedocs.io/en/latest/).__
