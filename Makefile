.PHONY: install dev build preview check clean

export PATH := /opt/homebrew/bin:$(PATH)

FRONTEND_DIR := frontend

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
