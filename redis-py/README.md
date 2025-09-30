# python redis pubsub package

## about project:
This is a cli package where you can send (PUBLISH) packages to, and receive packages from it.

## about pattern:
We use pub-sub pattern via redis to design, and build this
It's an event-driven pattern, when a service (publisher) sends messages, and multiple services (subscriber) can receive messages.
Think of TV stations, which the program is sent, and TVs can listen to it.

## how-to run:
First follow general instructions,

then you can make several publish service, and for each services make subscription services as you want.
### general instructs:
1. clone the repo, and go to this directory
``` bash
git clone https://github.com/AbbasDehganzadeh/py-excersize.git
cd redis-py
```
2. create, activate a virtual machine, and install required packages
``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
while in current directory, activating virtual machine, do the following instructions
### publish service:
3. go to redis_python, rename, and overwite .env file; NOTE: **'CHANNEL'** must be defined
``` bash
cd redis_python
mv .env.sample .env
vim .env
```
4. go to the folder, and execute main.py file
``` bash
cd pub.d
python main.py
```

### subscription service:
3. go to redis_python, rename, and overwite .env file; NOTE: **'CHANNEL'** is important!
``` bash
cd redis_python
mv .env.sample .env
vim .env
```
4. go to the folder, and execute main.py file
``` bash
cd sub.d
python main.py
```
