build: 
	docker build -t docker.toolforge.io/toolforgeio/hello-toolforge .

release:
	docker push docker.toolforge.io/toolforgeio/hello-toolforge
