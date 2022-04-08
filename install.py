#!/usr/bin/env python3

# This script will create a bash file in .local/bin to launch pwm


import os
import sys
import subprocess
from pathlib import Path


SCRIPT_PATH = os.path.join(Path.home(), '.local/bin/pwm')
PWM_PATH = sys.path[0]


def main():
    content = (
        f'#!/usr/bin/env bash\n\npushd {PWM_PATH}'
        ' > /dev/null\n./pwm.py\npopd > /dev/null'
    )
    # Create the launcher
    with open(SCRIPT_PATH, 'w') as f:
        f.write(content)

    # Make it executable
    subprocess.run(['chmod', '+x', SCRIPT_PATH])


if __name__ == "__main__":
    main()
