h:
	cat Makefile
u_local:
	docker-compose --profile local up --remove-orphans
b_u_local:
	docker-compose --profile local up --remove-orphans --build
start_local:
	docker exec -it dj-todo-web /bin/bash -c "poetry run task start_local"
attach_web:
	docker exec -it run-make-web /bin/bash