WatchTogether
===============

With the help of DRF - Django Rest Framework we managed to create a backend server that handles:
- User manager
- Room manager
- Stream manager
- Chat

The whole idea behind this backend service is to create a mobile app & website so shared watching of videos, listening to music, etc could be possible!

___________________________

To start the project you must follow these steps:
1. Navigate to the project folder then open your console and type the following command:
    ```
    python3 -m venv venv
    ```
 2. Run the virtual enviroment
    ```
    source venv/bin/activate
    ```
3. Install the requirements
    ```
    pip install -r requirements.txt
    ```

To be able to use Django Channels alongside with WebSockets, Redis has to be started and used as a message broker!

Install [Redis](https://redis.io/docs/install/install-redis/install-redis-on-mac-os/) on MAC OS:
1. Open your terminal and run the following command in your console:
    ```
    brew install redis
    ```
2. To start the server run the following command in the console:
    ```
    redis-server
    ```

Here is more information on [Redis](https://redis.io/docs/about/)\
\
After installing and starting Redis, you can just run the Django server:
```
python manage.py runserver
```
