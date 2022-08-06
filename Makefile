SHELL := /bin/bash

all:
	@# Create venv
	@if [[ ! -d "venv" ]]; then echo "Creating venv..." && python3 -m venv venv; \
		else echo "venv already exists"; fi

help:
	@echo "Run 'make' to create the venv"
	@echo "Run 'make reqs' after sourcing the venv to install modules using requirements.txt"
	@echo "Run 'make install' to be able to run PWM from anywhere"

reqs:
	@# Install required modules
	@echo "Installing requirements..."
	@pip install -r requirements.txt
	@echo "Done"

install: reqs
	@echo "Creating an executable in .local/bin..."
	@# Make sure ~/.local/bin exists
	@mkdir -p ~/.local/bin
	@# Create an executable in .local/bin
	@./install.py
	@echo "Done"
	@echo "Now you can run PWM from anywhere by typing 'pwm'"

uninstall:
	@echo "Uninstalling YDT from .local/bin..."
	@rm -f ~/.local/bin/ytd
	@echo "YDT was successfully uninstalled"

.PHONY: all help reqs install uninstall
