"""
Copyright (C) 2023 Dominic Schüchter

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

------------------------- Comment -------------------------
This class in used in combination with a server
The user can send queries to the server and recieves
feedback.
To directly communicate with a connected FPGA to the host
machine which runs the python script, use the fpga class
"""

import socket

class remoteFPGA():
    def __init__(self, baseaddr, server_ip, server_port, debug_messages=False):
        self.server_ip = server_ip
        self.server_port = server_port 
        self.baseaddr = baseaddr
        self.debug_messages = debug_messages
        self.data_types = {"readRegister":int,
                "writeRegister":str,
                "load_fpga":bool,
                "load_fpga_xml":bool,
                "load_fpga_if_new":bool,
                "load_fpga_if_new_xml":bool,
                "load_fpga_from_flash":bool,
                "async_load_fpga_from_flash":str,
                "swap_bits":str,
                "getBaseaddress":int,
                "getModulePCIBaseAdress":int,
                "getBoardID":int,
                "getBoardType":int,
                "getFirmwareVersion":int,
                "getFirmwareType":int,
                "getInterfaceVersion":int,
                "getMezzanineTypes":int,
                "getFPGADone":int,
                "wait_on_fpga_done":str,
                "test_connection":str}

    def send(self, query):
        if self.debug_messages: print("Client Message: "+ query)
        command = query.split(" ")[0]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_ip, self.server_port))
            s.sendall(str.encode(str(self.baseaddr)+" "+query))
            data = s.recv(1024)
            if self.debug_messages: print(f"Server Response: "+ data.decode())
            return self.data_types[command](data.decode())
            
    def load_fpga(self, file_path):
        return self.send("load_fpga "+str(file_path))
    def load_fpga_xml(self, file_path):
        return self.send("load_fpga_xml "+str(file_path))
    def load_fpga_if_new(self, file_path):
        return self.send("load_fpga_if_new "+str(file_path))
    def load_fpga_if_new_xml(self, file_path):
        return self.send("load_fpga_if_new_xml "+str(file_path))
    def load_fpga_from_flash(self, file_path):
        return self.send("load_fpga_from_flash "+str(file_path))
    def async_load_fpga_from_flash(self, file_path):
        return self.send("async_load_fpga_from_flash "+str(file_path))
    def readRegister(self, register):
        return self.send("readRegister "+ str(register))
    def writeRegister(self, register, value):
        return self.send("writeRegister "+str(register)+" "+str(value))
    def swap_bits(self, inputbits):
        return self.send("swap_bits "+str(inputbits))
    def getBaseaddress(self):
        return self.send("getBaseaddress")
    def getModulePCIBaseAdress(self):
        return self.send("getModulePCIBaseAdress")
    def getBoardID(self):
        return self.send("getBoardID")
    def getBoardType(self):
        return self.send("getBoardType")
    def getFirmwareVersion(self):
        return self.send("getFirmwareVersion")
    def getFirmwareType(self):
        return self.send("getFirmwareType")
    def getInterfaceVersion(self):
        return self.send("getInterfaceVersion")
    def getMezzanineTypes(self, number):
        return self.send("getMezzanineTypes "+str(number))
    def getFPGADone(self):
        return self.send("getFPGADone")
    def wait_on_fpga_done(self):
        return self.send("wait_on_fpga_done")
    def test_connection(self):
        return self.send("test_connection")
