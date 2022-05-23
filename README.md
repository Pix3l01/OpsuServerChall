# PTC - Pwn The Circles!

## m0leCon CTF 2022 Teaser challenge

[m0leCon CTF 2022 Teaser](https://ctftime.org/event/1615) is an online jeopardy-style CTF organized
by [pwnthem0le](https://pwnthem0le.polito.it/). Top 5 teams will be invited to the final event, that will take place in
Fall 2022 at Politecnico di Torino, alongside with the m0leCon conference.
Finals will be also open to everyone that takes part in the conference, up to the capacity of the rooms.

### Description

Are you better than Cookiezi? Show it to us and win a fantastic prize 🚩!<br>
(P.S. the flag will appear in your pofile page, so use a strong password (; )

### Deploy

Both the `Dockerfile` and the `docker-compose.yaml` files are provided in the `src` folder to launch the server through
[Docker](https://www.docker.com/).<br>
Since the client connects to `https://ptc.m0lecon.fans` to have it connect to the server you have three options:

1. To have an environment as similar to the original as possible the best way would be to expose the server through a
   reverse proxy with an SSL certificate for `ptc.m0lecon.fans` and add the reverse proxy IP to
   your [host file](https://www.howtogeek.com/howto/27350/beginner-geek-how-to-edit-your-hosts-file/): 
   `123.123.123.123 ptc.m0lecon.fans` (change `123.123.123.123` with the actual IP)
2. If you don't want to mess around with the SSL certificate (and reverse proxy) I added an http client
   in `src/app/static/Clienthttp.jar`. Just rename it `Client.jar` and substitute the original https client. Remember to
   run the server on port 80 (so modify the Dockerfile/docker-compose accordingly) and add the server IP to your
   [host file](https://www.howtogeek.com/howto/27350/beginner-geek-how-to-edit-your-hosts-file/): 
   `123.123.123.123 ptc.m0lecon.fans` (change `123.123.123.123` with the actual IP)
3. Find in the client the method(s) it uses to connect to the server and patch the link(s), then replace the patched
   version in `src/app/static/Client.jar` and (re)start the server

### Flag

ptm{I_D!d_Th3_08fUSCati0n_bY_H4nD}

## Solution

In `solv` there's a solver script (`solve.py`). I'll add a simple explanation later on. 
