build: 
	docker build -t docker.toolforge.io/sigpwned/link-unwinder .

release: build
	docker push docker.toolforge.io/sigpwned/link-unwinder
