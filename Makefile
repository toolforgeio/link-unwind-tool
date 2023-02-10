build: 
	docker build -t docker.toolforge.io/sigpwned/link-unwinder .

release:
	docker push docker.toolforge.io/sigpwned/link-unwinder
