import sys                      
import platform                 
from datetime import datetime   

import pytest
import selenium
import requests
import pandas
import openpyxl


def print_header():
    print("=" * 70)
    print("SDET ENVIRONMENT VERIFICATION REPORT")
    print("=" * 70)
    print(f"Timestamp         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python Version    : {sys.version}")
    print(f"Platform          : {platform.platform()}")
    print(f"Python Executable : {sys.executable}")
    print("=" * 70)

def print_package_versions():
    print("\nINSTALLED PACKAGE VERSIONS:")
    print("-" * 40)
    print(f"pytest      : {pytest.__version__}")
    print(f"selenium    : {selenium.__version__}")
    print(f"requests    : {requests.__version__}")
    print(f"pandas      : {pandas.__version__}")
    print(f"openpyxl    : {openpyxl.__version__}")
    print("-" * 40)


if __name__ == "__main__":
    print_header()
    print_package_versions()
