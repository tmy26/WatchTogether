WatchTogether
===============

Django based REST API
___________________________

To run the project you have to run your venv and type the following commands:
    pip install -r requirements.txt

To be using the channels along with WebSockets, redis need to be started and used as a message broker.

Install Redis on MAC OS:
    To install [Redis](https://redis.io/docs/install/install-redis/install-redis-on-mac-os/) open your terminal and run the following command:\
    ```
    {
      brew install redis
    }
    ```
    After the installation finishes, all you need to do, to run the server is to type in your console:\
    ```
    {
      redis-server
    }
    ```
     
Here is more information on [R](https://redis.io/docs/about/)\
\
After installing and starting Redis, you can just run the Django server:\
    ```
    {
      python manage.py runserver
    }
    ```
