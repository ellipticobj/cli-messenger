# cli-messenger
rewrite in progress [here](https://github.com/ellipticobj/cli-messenger/tree/v2/)  
simple cli messenger app made with python

# running
git clone this repo

```bash
git clone https://github.com/ellipticobj/cli-messenger.git
```

## server
to run the server, run server.py

```bash
python server.py
```

you can use something like tmux to keep it running

## clients
run client.py

```bash
python client.py
```

you will be greeted with this prompt:
```
use default config?
HOST=luna.hackclub.app
PORT=7172
[Y/n]>
```
press enter if you want to join the default server (might not be online)

if you self hosted, or are joining a self hosted server, type `n` and hit enter, then enter the server ip and port when prompted to.

# roadmap
documentation
a persistent prompt so that there is a `you:` before messages you send and others' messages wont interrupt yours
better error handling
version codes of some sort so that cilents know when they are outdated
