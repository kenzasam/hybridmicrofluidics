# Hybrid Microfluidics Software Package Installation Guide
by Kenza Samlali

#### System requirements:
Windows XP or up
Python 2.7

## Computer System setup
1. Install Python 2.7. Our software has ben tested on Python 2.7, so we recommend this.
2. There are several extra packages required for you to be able to use the Chipviewer, GUI, or even ArduBridge.
We recommend installation of Pip (a package manager). If you already have Pip (included in Py>2.7 and Py3), skip this step.
[Tutorial](https://pip.pypa.io/en/stable/installing/). Also, add pip to your env vars if needed. (python/scripts)
3. You can check which version of pip is installed like this: `pip -V` <br>
You can update pip like this: `pip install --upgrade pip`
4. Optional: Consider using a virtual environment, if you know you might want to use different versions of Python next to each other, or different packages. f.e. for one project you need python 3 with several packages, but for another project you need python 2.7 with other packages.... With a virtual environment, you can install python packages in a specific project folder.

## Installing GSOF_ArduBridge and setting up your automation system
1. Make sure your system is set up correctly for the software. Use Python 2.7 [See system setup](## Computer System setup)
2. Download the [GSOF_ArduBridge](https://bitbucket.org/gsoffer/gsof_ardubridge/) repository and unzip.
3. Download the quick_start software package and unzip. Place the quick_start package in a convenient location.
4. Install further dependencies needed for this project by running `pip install -r requirements.txt` . If using a virtualenv, install them in the virtualenv.
4. Open the GSOF_ArduBridge folder > ArduBridge, and locate setup.py
5. Run setup.py . This will install most GSOF_ArduBridge dependencies.
6. Edit the quick_start_package files to your needs. [See README.md](../quick_start_package/README.md)
7. Connect an Arduino to your computer.
8. Open GSOF> ArduFW_V11 and double-click the xloader.
9. Enter the COM port, baud rate and Arduino version, and press upload. This programs your Arduino.
10. Make sure all other hardware (syringe pumps, optocoupler stack, function generator, power supply) is connected accordingly.
11. You're now ready to roll! See ["How to run and use the software"](../quick_start_package/README.md).
