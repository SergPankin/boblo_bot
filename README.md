# boblo_bot
Here I store my pet bot

Prerequirements:
1. Cloud Virtual machine (or other serever)
2. PostgreSQL 14 (do not forget to add config-template with its connection string and credentials)
3. Your Telegram bot token (Telegram Bot Father helps to create it)
4. Python >= 3.7 at your virtual machine (server)
5. Additional commands (in case you start from blank Linux machine):
sudo apt-get install postgresql
sudo apt-get install libpq-dev

Start of your bot setup:
1. Copy migrations to DB
2. Install dependencies in your Linux
3. Start main.py at VM in the background (nohup)

How to start in Docker:
1. sudo docker build . -t bot/boblo_bot:0.1
3. sudo docker run --rm --name=boblo bot/boblo_bot:0.1
4. sudo docker stop boblo
