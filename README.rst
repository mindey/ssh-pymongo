ssh-pymongo
-----------

Just for convenience. Note: `uri` parameter is assumed as local, after ssh.

``pip install ssh-pymongo``

Example 1
---------

.. code:: python

    from ssh_pymongo import MongoSession

    session = MongoSession('db.example.com')

    db = session.connection['db-name']

Example 2
---------

.. code:: python

    session = MongoSession(
        host='db.example.com',
        uri='mongodb://user:password@127.0.0.1/?authSource=admin&authMechanism=SCRAM-SHA-256'
    )
    ...
    session.stop()

Example 3
---------

.. code:: python

    session = MongoSession(
        host='db.example.com',
        user='myuser',
        password='mypassword',
    )
    ...
    session.stop()

Example 4
---------

.. code:: python

    session = MongoSession(
        host='db.example.com',
        port='21',
        user='myuser',
        key='/home/myplace/.ssh/id_rsa2',
        to_port='37017',
        to_host='0.0.0.0'
    )
    ...
    session.stop()

