# pyVME
This package uses exposed cpp functions using [```pybind11```](https://pybind11.readthedocs.io/en/stable/index.html) to use the VMEbus (Versa Module Eurocard-bus) to interact with FPGAs. 
The shared object used for this was compiled on a 64bit Linux machine and supports no other platforms.

It is intended for the use at ELSA (University of Bonn) and can be used for many elegant implementations of different tools.

The main functionality comes from a shared object (.so) that ships as a binary blob within this package. 

# Table of Contents
1. [Requierements](#Requierements)
2. [Installation](#Installation)
3. [Building from source](#Building-from-source)
   
## Requierements:
This package needs to be run on a Linux 64bit machine with python >= 3.9 installed

## Installation
This package is available via [```pypi```](https://pypi.org) and can be simply installed by running:

    pip install pyVME

## Features
After installation (e.g. pip install pyVME) you can import this package into your projects via ```import pyVME```.

This gives you access to the three classes that come within this package, returns ```
1. ```pyVME.fpga(baseaddr)```: Allows you to instantiate one FPGA that is directly connected to the CPU your python program is running on
2. ```pyVME.server(int server_port)```: Allows you to run a server on a remote machine that is connected with one or more FPGAs. It will instantiate for each FPGA defined by the client a new instance.  
3. ```pyVME.remoteFPGA(int baseaddr, string server_ip, int server_port)```: Allows you to connect to a running server and call functions of the remote FPGA instances.

Every class has the same set of functions that act differently in the background without the user having to change anything.

### Functions
The following functions are supported:
- ```readRegisters(int register)```, returns ```str```
- ```writeRegisters(int register, int value)```, returns ```str```
- ```load_fpga(string file_path)```, returns ```bool```
- ```load_fpga_xml(string file_path)```, returns ```bool```
- ```load_fpga_if_new(string file_path)```, returns ```bool```
- ```load_fpga_if_new_xml(string file_path)```, returns ```bool```
- ```load_fpga_from_flash(string file_path)```, returns ```bool```
- ```async_load_fpga_from_flash(string file_path)```, returns ```str```
- ```swap_bits(int inputbits)```, returns ```str```
- ```getBaseaddress()```, returns ```int```
- ```getModulePCIBaseAdress()```, returns ```int```
- ```getBoardID()```, returns ```int```
- ```getBoardType()```, returns ```int```
- ```getFirmwareVersion()```, returns ```int```
- ```getFirmwareType()```, returns ```int```
- ```getInterfaceVersion()```, returns ```int```
- ```getMezzanineType()s```, returns ```int```
- ```getFPGADone()```, returns ```int```
- ```wait_on_fpga_done()```, returns ```str```

### Examples
#### Server:
```
import pyVME as vme
server = vme.server(port=5555)
server.run()
```

#### remote FPGA:
```
import pyVME as vme
fpga = vme.remoteFPGA(baseaddr=0xAB000000, server_ip='remote_ip/domain', server_port=5555)
```
#### local FPGA:
```
import pyVME as vme
fpga = vme.fpga(baseaddr=0xAB000000)
```

### Source Code
This project is only partially open source because it comes with a binary blob in form of a shared object (the source code for the ```.so``` is accessable for members of the HISKP only on the [HISKP Gitlab](https://agthoma.hiskp.uni-bonn.de/gitlab/CB/daq/daq-tr/-/tree/master/utilities/pyVME)). 
The source code can be found at [pyVME](https://github.com/dschuechter/pyVME).

## Building from source
To build this package you need to have the build package installed:
```
pip install build
```
No other packages are requiered. You can simply build this package by running:
```
python3 -m build
```
in the root directory of this repository.

It will automatically generate a ```dist```folder with the contents ```pyVME-X.X.X-py3-none-any.whl``` and ```pyVME-X.X.X.tar.gz```.

You can install the build package by running 
```
pip install ./dist/pyVME-X.X.X-py3-none-any.whl
```
or

```
pip install ./dist/pyVME-X.X.X.tar.gz   
```