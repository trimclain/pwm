SHELL := /bin/bash

all:
	@# Create venv
	@if [[ ! -d "venv" ]]; then echo "Creating venv..." && python3 -m venv venv; \
		else echo "venv already exists"; fi

help:
	@echo "Run 'make' to create the venv"
	@echo "Run 'make install_reqs' after sourcing the venv to install modules requirements.txt"
	@echo "Run 'make install' to be able to run PWM from anywhere

install_reqs:
	@# Install required modules
	@echo "Installing requirements..."
	@pip install -r requirements.txt
	@echo "Done"

install: install_reqs
	@echo "Creating an executable in .local/bin..."
	@# Make sure ~/.local/bin exists
	@mkdir -p ~/.local/bin
	@# Create an executable in .local/bin
	@./install.py
	@echo "Done"
	@echo "Now you can run PWM from anywhere by typing 'pwm'"

.PHONY: all help install_reqs install
