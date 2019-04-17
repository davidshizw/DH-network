# Assignment: Songs Retrieval System

As the project title suggests, this system is able to receives an artist name from client and finds all the song(s) associated to that artist given the server is established. 

## What's included

Two source files (.py)
Two bash scripts (.sh)
One input file (.txt)
Two log files (.log)

Three arbitrary artist names (Oliver, Falco, Mike) were chosen for testing purposing.

## Operating environment

The server socket of this system will listen at the predefined host 127.0.0.1 and port 8000 for incoming TCP/IP requests. The maximum number of queued connections to the server is 5.

This system is implemented in python 3.7 using socket library. Based on current testing results, build-in input function will result in NameError in python 2.X environment.

## How to use

The server socket can be created on the command line of Windows, Mac, and Linux by the following commands:
cd "the Directory Where This README file Stores"
./server.sh OR python Server.py

As long as the server socket is setup, the client socket can be created similarly on a NEW command line window:
cd "the Directory Where This README file Stores"
./client.sh OR python Client.py

If permission-denied exception occurs, open the following page for help: 
https://askubuntu.com/questions/409025/permission-denied-when-running-sh-scripts

