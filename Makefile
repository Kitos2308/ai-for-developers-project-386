.PHONY: install dev build preview check clean migrate.gen migrate.up migrate.down

export PATH := /opt/homebrew/bin:$(PATH)

FRONTEND_DIR := frontend
BACKEND_DIR := backend

install:
	cd $(FRONTEND_DIR) && npm install

dev:
	cd $(FRONTEND_DIR) && npm run dev

build:
	cd $(FRONTEND_DIR) && npm run build

preview:
	cd $(FRONTEND_DIR) && npm run preview

check:
	cd $(FRONTEND_DIR) && npm run check

clean:
	rm -rf $(FRONTEND_DIR)/node_modules
	rm -rf $(FRONTEND_DIR)/.svelte-kit
	rm -rf $(FRONTEND_DIR)/dist

migrate.gen:
	cd $(BACKEND_DIR) && poetry run alembic revision --autogenerate -m "$(name)"

migrate.up:
	cd $(BACKEND_DIR) && poetry run alembic upgrade head

migrate.down:
	cd $(BACKEND_DIR) && poetry run alembic downgrade -1

backend.up:
	cd $(BACKEND_DIR) && poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
