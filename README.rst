ssh-pymongo
-----------

Just for convenience.

``pip install ssh-pymongo``

Example 1
---------

.. code:: python

    from ssh_pymongo import MongoSession

    session = MongoSession('db.example.com')
    # session.connection.database_names()

    db = session.connection['db-name']
    collection = db['collection-name']

    session.stop()
    # session.start()

Example 2
---------

.. code:: python

    session = MongoSession(
        host='db.example.com',
        user='myuser',
        password='mypassword',
    )
    ...
    session.stop()

Example 3
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

