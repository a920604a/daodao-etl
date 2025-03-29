PLATFORM ?= linux/amd64



# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

TARGET_MAX_CHAR_NUM=20

## Show help with `make help`
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)


clean:
	sudo rm -rf ./logs ./plugins ./config ./data
init:
	mkdir -p ./logs ./plugins ./config ./data ./data/airflow-db-volume
	docker compose run --rm airflow-init 
up:
	docker compose up -d
	sleep 10
	echo "開始恢復 MongoDB 數據..."
	docker exec mongo-daodao mongorestore --drop --db=2025-01-30-prod /backup/2025-01-30/prod
	docker exec mongo-daodao mongorestore --drop --db=2025-03-29-prod /backup/2025-03-29/prod
	echo "MongoDB 數據恢復完成。"
down:
	docker compose down --volumes --remove-orphans --rmi all

