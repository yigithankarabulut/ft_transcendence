all:
	docker build . -t nginx
	docker run -d -p 8080:80 --name nginx nginx
clean:
	docker stop nginx
	echo y | docker system prune -a

re: clean all