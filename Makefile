IMAGE := docker.toolforge.io/sigpwned/link-unwinder

build: 
	docker build -t ${IMAGE} .

release: build
	docker push ${IMAGE}
