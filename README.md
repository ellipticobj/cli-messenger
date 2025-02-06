# cli-messenger

simple cli messenger app made with python

# quickstart

git clone this repo:
```bash
git clone https://github.com/ellipticobj/cli-messenger.git
```

cd into the directory:
```bash
cd cli-messenger
```

install requirements:
```bash
pip3 install -r requirements.txt
```

run client.py
```
python3 client.py
```

the default server is **luna.hackclub.app:7171**

# features
## implemented
### clients:
persistent prompt
decent ui
ability to choose different servers

### servers:
easily customizable server settings
extensive logs

## in development
client side commands (fun stuff ;3)
server side commands:
- easy white/blacklist toggling
- profanity filter toggling
server settings in json?
executables for clients using pyinstaller

# hosting your own server
git clone this repo:
```bash
git clone git@github.com:https://github.com/ellipticobj/cli-messenger.git
```

cd into the directory:
```bash
cd cli-messenger
```

install requirements:
```bash
pip3 install -r requirements.txt
```

edit server settings in server.py if you want:
under the init of the server class, you can edit the variables to fit your needs

run server.py
```
python3 server.py
```
