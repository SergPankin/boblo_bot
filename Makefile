build:
	sudo docker build . -t bot/boblo_bot:0.1

start:
	sudo docker run --rm --name=boblo bot/boblo_bot:0.1

dstart:
	sudo docker run -d --rm --name=boblo bot/boblo_bot:0.1

run:
	sudo docker build . -t bot/boblo_bot:0.1
	sudo docker run --rm --name=boblo bot/boblo_bot:0.1

drun:
	sudo docker build . -t bot/boblo_bot:0.1
	sudo docker run -d --rm --name=boblo bot/boblo_bot:0.1

attach:
	sudo docker attach boblo

stop:
	sudo docker stop boblo

ls:
	sudo docker ps

test:
	python3.8 -m pytest tests
