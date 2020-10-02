# Hybrid Microfluidics Software Package Installation Guide
*by Kenza Samlali, 2020*

#### System requirements:
Windows XP or up
Python 2.7

## Computer System setup and Installing GSOF_ArduBridge

Optional: Consider using a virtual environment, if you know you might want to use different versions of Python next to each other, or different packages. We have tested this with a [pyenv](https://realpython.com/intro-to-pyenv/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) combo.

1. Install Python 2.7. Our software has ben tested on Python 2.7, so we recommend this. (optional: install it using pyenv `pyenv install 2.7.14`, and then enter your shell in this pyenv python version `pyenv shell 2.7.14`.)
2. There are several extra packages required for you to be able to use the Chipviewer, GUI, or even ArduBridge.
We recommend using Pip (a package manager). If you already have Pip (included in Py>2.7 and Py3), skip this step.
[Tutorial](https://pip.pypa.io/en/stable/installing/). Also, add pip to your env vars if needed. (python/scripts)
3. You can check which version of pip is installed like this: `pip -V` <br>
You can update pip like this: `pip install --upgrade pip`
4. Download the [GSOF_ArduBridge](https://bitbucket.org/gsoffer/gsof_ardubridge/) repository and unzip.
5. Download the quick_start software package and unzip. Place the quick_start package in a convenient location.
6. Open the GSOF_ArduBridge folder > ArduBridge, and locate setup.py. In your terminal, move to the setup.py directory. (optional: create a virtual environment in python 2.7.14 using virtualenvwrapper `mkvirtualenv gsofardubridge_p27` enter the virtualenv `workon gsofardubridge_p27`, go to the setup.py directory )
7. Run `python setup.py install`. This will install most GSOF_ArduBridge dependencies.
8. In your terminal, move to the quick_start_package directory. Install further dependencies needed for this project by running `pip install -r requirements.txt` . (optional: If using a virtualenv, install them in the virtualenv)

##  Setting up your automation system
9. Edit the quick_start_package files to your needs. [See README.md](../quick_start_package/README.md)
10. Connect an Arduino to your computer.
11. Open GSOF> ArduFW_V11 and double-click the xloader.
12. Enter the COM port, baud rate and Arduino version, and press upload. This programs your Arduino.
13. Make sure all other hardware (syringe pumps, optocoupler stack, function generator, power supply) is connected accordingly.
14. You're now ready to roll! See ["How to run and use the software"](../quick_start_package/README.md).
