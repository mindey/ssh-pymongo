from sshtunnel import SSHTunnelForwarder
import pymongo
import getpass
import urllib


class MongoSession:

    def __init__(self, host, user=None, password=None, key=None, key_password=None, uri=None, port=22, to_host='127.0.0.1', to_port=27017):

        HOST = (host, port)
        USER = user or getpass.getuser()
        KEY = key or f'/home/{USER}/.ssh/id_rsa'
        KEY_PASSWORD = key_password
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
                ssh_private_key_password=KEY_PASSWORD,
                remote_bind_address=(to_host, to_port)
            )

        self.start()

    def start(self):
        self.server.start()

        params = dict()

        if self.uri:
            uri = urllib.parse.urlparse(self.uri)

            if '@' in uri.netloc:
                user_pass = uri.netloc.split('@', 1)[0]
                if ':' in user_pass:
                    params['username'], params['password'] = user_pass.split(':', 1)
                else:
                    params['username'] = user_pass

            if uri.query:
                auth_mech = urllib.parse.parse_qs(uri.query)
                params.update({key: auth_mech[key][0] for key in auth_mech})

        self.connection = pymongo.MongoClient(
            host=self.to_host,
            port=self.server.local_bind_port,
            **params)

    def stop(self):
        self.connection.close()
        self.server.stop()
        del self.connection

    def close(self):
        self.stop()
