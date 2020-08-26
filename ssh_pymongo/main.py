from sshtunnel import SSHTunnelForwarder
import pymongo
import getpass


class MongoSession:

    def __init__(self, host, user=None, password=None, key=None, port=22, to_host='127.0.0.1', to_port=27017):

        HOST = (host, port)
        USER = user or getpass.getuser()
        KEY = key or f'/home/{USER}/.ssh/id_rsa'
        self.to_host = to_host

        if password:
            self.server = SSHTunnelForwarder(
                HOST,
                ssh_username=USER,
                ssh_password=password,
                remote_bind_address=(to_host, to_port)
            )
        else:
            self.server = SSHTunnelForwarder(
                HOST,
                ssh_username=USER,
                ssh_pkey=KEY,
                remote_bind_address=(to_host, to_port)
            )

        self.start()

    def start(self):
        self.server.start()
        self.connection = pymongo.MongoClient(self.to_host, self.server.local_bind_port)

    def stop(self):
        self.connection.close()
        self.server.stop()
        del self.connection
