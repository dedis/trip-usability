# Kiosk Credentialing Application

This application is a UI mockup of [TRIP](https://arxiv.org/abs/2202.06692) and designed for use on our kiosk purchased on [Alibaba](https://www.alibaba.com/product-detail/Factory-Direct-Supply-Android-Touch-Screen_1600462916445.html).

## Kiosk Hardware

- 13.3" touchscreen
- 58mm thermal printer
- Barcode/QR code scanner 
- Bluetooth/WiFi 2.4g/Ethernet
- Customized with Linux OS

## Application

1. Clone the repository
1. Install [Pyenv](https://github.com/pyenv/pyenv#installation)
1. Install [Pyenv Virtual Environment](https://github.com/pyenv/pyenv-virtualenv)
1. Install Python version 3.9.18
   - `pyenv install 3.9.18`
1. Create a virtual environment
   - `pyenv virtualenv 3.9.18 venv`
1. Set the local python version for this project
   - `pyenv local venv`
1. Install required packages
   - `pip install -r requirements.txt`
1. Configure Application
   - `cp .env.sample .env`
1. Launch Application
   - `export PYTHONPATH=$(pwd)`
   - `python app/main.py --group 1` specifying the study group from 1 to 5