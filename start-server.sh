#!/bin/bash
tmux new -d -s messenger "cd ~/messenger-app && git pull && python3 server.py"

