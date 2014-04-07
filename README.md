Easyftp
=======

A wrapper around pyftplib with start script and deps to run it as daemon.

On Debian/Ubuntu

    $ sudo apt-get install python-pip build-essential python-dev

Install the server and run the Daemon

    $ pip install -r requirements/common.txt
    $ zdaemon -C conf/zdeamon.conf start

