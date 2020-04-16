# Hybrid Microfluidics Software Package Installation Guide
by Kenza Samlali

#### System requirements:
Windows XP or up
Python 2.7

## How to set up your automation system
1. Download the software package and unzip.
2. Make sure your system is set up correctly for the software. [See system setup](### System setup)
3. Open the GSOF folder > ArduBridge, and locate setup.py
4. Run setup.py using IDLE. This will install all dependencies.
5. Plug in your Arduino
6. Open GSOF> ArduFW_V11 and double-click the xloader.
7. Enter the COM port, baud rate and arduino version, and press upload.
8. You're now ready to roll!

## Computer System setup
1. Install Python 2.7. Our software has ben tested on Python 2.7, so we recommend this.
2. There are several extra packages required for you to be able to use the Chipviewer, GUI, or even ArduBridge.
We recommend installation of Pip (a package manager). If you already have Pip (included in Py>2.7 and Py3), skip this step.
[Tutorial](https://pip.pypa.io/en/stable/installing/). Also, add pip to your env vars if needed. (python/scripts)
3. You can check which version of pip is installed like this: `pip -V` <br>
You can update pip like this: `pip install --upgrade pip`
4. Install following packages:
pyserial, wxpython, tkinter, pyperclip, numpy,
for Nemesys on python 2.7: enum34 , [pyqmix](https://github.com/psyfood/pyqmix)
use the following command: `pip install ...`
You can find their respective install commands on the pip website.
5. Optional: Consider using a virtual environment, if you know you might want to use different versions of Python next to each other, or different packages. f.e. for one project you need python 3 with several packages, but for another project you need python 2.7 with other packages.... With a virtual environment, you can install python packages in a specific project folder.
