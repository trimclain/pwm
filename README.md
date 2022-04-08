# PWM
PWM is a simple CLI Password Manager written in Python.
It uses [cryptography](https://pypi.org/project/cryptography/)
and its [Fernet](https://cryptography.io/en/latest/fernet/) encryption.

## How to install

- (Recommended) To install PWM for current user run `make install`.
  Now you can run `pwm` from anywhere to launch PWM

- To install the venv, the requirements and run pwm from this folder:
    1. `make`
    2. `source venv/bin/activate`
    3. `make install_reqs`
    4. `./pwm.py`
