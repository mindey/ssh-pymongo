from sshtunnel import SSHTunnelForwarder
import pymongo
import getpass
import urllib


class MongoSession:

    def __init__(self, host, user=None, password=None, key=None, uri=None, port=22, to_host='127.0.0.1', to_port=27017):

        HOST = (host, port)
        USER = user or getpass.getuser()
        KEY = key or f'/home/{USER}/.ssh/id_rsa'
        self.to_host = to_host
        self.uri = uri; URI = urllib.parse.urlparse(uri)

        if uri:
            to_host = URI.hostname or to_host
            to_port = URI.port or to_port

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

        if self.uri:
            uri = urllib.parse.urlparse(self.uri)

            if uri.netloc:
                user_pass = uri.netloc.split('@', 1)[0].split(':', 1)
                if len(user_pass) == 2:
                    mongo_user, mongo_pass = user_pass
                elif len(user_pass) == 1:
                    mongo_user, mongo_pass = user_pass, None
                else:
                    mongo_user, mongo_pass = None, None
            else:
                mongo_user, mongo_pass = (None, None)

            if uri.query:
                auth_mech = urllib.parse.parse_qs(uri.query)
                if 'authSource' in auth_mech:
                    auth_db = auth_mech['authSource'][0]
                else:
                    auth_db = None
                if 'authMechanism' in auth_mech:
                    auth_mechanism = auth_mech['authMechanism'][0]
                else:
                    auth_mechanism = None
            else:
                auth_db, auth_mechanism = (None, None)

            if all([mongo_user,  mongo_pass, auth_db, auth_mechanism]):
                self.connection = pymongo.MongoClient(
                    host=self.to_host,
                    port=self.server.local_bind_port,
                    username=mongo_user,
                    password=mongo_pass,
                    authSource=auth_db,
                    authMechanism=auth_mechanism
                )
            else:
                self.connection = pymongo.MongoClient(self.to_host, self.server.local_bind_port)
        else:
            self.connection = pymongo.MongoClient(self.to_host, self.server.local_bind_port)

    def stop(self):
        self.connection.close()
        self.server.stop()
        del self.connection

    def close(self):
        self.stop()
