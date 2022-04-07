SHELL := /bin/bash

all:
	@# Create venv
	@if [[ ! -d "venv" ]]; then echo "Creating venv..." && python3 -m venv venv; \
		else echo "venv already exists"; fi

help:
	@echo "Run 'make' to create the venv"
	@echo "Run 'make install_reqs' after sourcing the venv to install modules requirements.txt"
	@echo "Run 'make install' to copy the executable to ~/.local/bin

install_reqs:
	@# Install required modules
	pip install -r requirements.txt

# TODO:
install:
	@# Copy the executable to a folder in PATH (.local/bin)
	cp ./pwm.py ~/.local/bin/pwm

.PHONY: all help install_reqs install
