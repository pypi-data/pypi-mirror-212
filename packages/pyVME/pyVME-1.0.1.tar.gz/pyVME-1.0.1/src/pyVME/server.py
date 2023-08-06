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
A simple socket that recieves vme commands, instantiates vme 
connections and sends feedback to the client
"""

import socket
from pyVME.fpga import * 

class server():
    def __init__(self, server_port, debug_messages=False):
        self.server_ip = socket.getfqdn() 
        self.server_port = server_port 
        self.query = ""
        self.created_fpga_objects = []
        self.FPGAs = []
        self.clients = []
        self.debug_messages = True

    def info(self):
        print("\n------ Started Server ------")
        print(self.server_ip+":"+str(self.server_port)+'\n')

    def query_handler(self, query):
        query = query.decode().split()
        if 'test_connection' not in query:
            baseaddr = hex(int(query[0]))
            command = query[1]
            if len(query)>=3:
                arg_1 = query[2] 
            if len(query)>=4:
                arg_2 = query[3]
            if baseaddr in self.created_fpga_objects:
                FPGA = self.FPGAs[self.created_fpga_objects.index(baseaddr)]
            else:
                self.created_fpga_objects.append(baseaddr)
                FPGA = fpga(int(baseaddr,base=16))
                self.FPGAs.append(FPGA)
        else:
            if self.debug_messages: print("Successfull test connection")
            return 'Connection Successfull' 

        if command == 'readRegister':
            get_register = FPGA.readRegister(int(arg_1))
            if self.debug_messages: print("Get register\t", hex(int(arg_1)+ int(baseaddr, base=16)), ":", get_register)
            return get_register

        if command == 'writeRegister':
            FPGA.writeRegister(int(arg_1), int(arg_2))
            if self.debug_messages: print("Wrote Register\t", hex(int(arg_1)+ int(baseaddr, base=16)), ":", int(arg_2))
            return "Register "+hex(int(arg_1))+" -> "+arg_2

        if command == 'load_fpga':
            loaded = FPGA.load_fpga(arg_1)
            if self.debug_messages: print("Loaded FPGA firmware ", arg_1)
            return loaded

        if command == 'load_fpga_xml':
            loaded = FPGA.load_fpga_xml(arg_1)
            if self.debug_messages: print("Loaded XML ", arg_1)
            return loaded

        if command == 'load_fpga_if_new':
            loaded = FPGA.load_fpga_if_new(arg_1)
            if self.debug_messages: print("Loaded FPGA if new ", arg_1)
            return loaded

        if command == 'load_fpga_if_new_xml':
            loaded = FPGA.load_fpga_if_new_xml(arg_1)
            if self.debug_messages: print("Loaded XML if new ", arg_1)
            return loaded
        
        if command == 'load_fpga_from_flash':
            loaded = FPGA.load_fpga_from_flash(arg_1)
            if self.debug_messages: print("Loaded FPGA from flash ", arg_1)
            return loaded
        
        if command == 'async_load_fpga_from_flash':
            FPGA.async_load_fpga_from_flash(arg_1)
            if self.debug_messages: print("Async loaded FPGA from flash ", arg_1)
            return "Async loaded FPGA from flash"

        if command == 'swap_bits':
            FPGA.swap_bits(int(arg_1))
            if self.debug_messages: print("Swapped bits %s"%(arg_1))
            return "Swapped bits %s"%(arg_1)

        if command == 'getBaseaddress':
            read_baseaddress = FPGA.getBaseaddress()
            if self.debug_messages: print("Get baseaddress: ", baseaddr)
            return read_baseaddress

        if command == 'getModulePCIBaseAdress':
            read_modulePCIBaseaddress = FPGA.getModulePCIBaseAdress()
            if self.debug_messages: print("Get Module PCI Baseaddress: ", read_modulePCIBaseaddress)
            return read_modulePCIBaseaddress

        if command == 'getBoardID':
            read_boardID = FPGA.getBoardID()
            if self.debug_messages: print("Get board ID: ", read_boardID)
            return read_boardID

        if command == 'getBoardType':
            read_boardType = FPGA.getBoardType()
            if self.debug_messages: print("Get board type: ", read_boardType)
            return read_boardType

        if command == 'getFirmwareVersion':
            read_firmwareVersion = FPGA.getFirmwareVersion()
            if self.debug_messages: print("Get firmware version: ", read_firmwareVersion)
            return read_firmwareVersion
    
        if command == 'getFirmwareType':
            read_firmwareType = FPGA.getFirmwareType()
            if self.debug_messages: print("Get firmware type: ", read_firmwareType)
            return read_firmwareType

        if command == 'getInterfaceVersion':
            read_interfaceVersion = FPGA.getInterfaceVersion()
            if self.debug_messages: print("Get interface version: ", read_interfaceVersion)
            return read_interfaceVersion

        if command == 'getMezzanineTypes':
            read_mezzanineTypes = FPGA.getMezzanineTypes(int(arg_1))
            if self.debug_messages: print("Get mezzanine types: ", read_mezzanineTypes)
            return read_mezzanineTypes
        
        if command == 'getFPGADone':
            read_fpgaDone = FPGA.getFPGADone()
            if self.debug_messages: print("Get FPGA done: ", read_fpgaDone)
            return read_fpgaDone

        if command == 'wait_on_fpga_done':
            read_wait_on_fpga_done = FPGA.wait_on_fpga_done()
            if self.debug_messages: print("Get wait on fpga done: ", read_wait_on_fpga_done)
            return read_wait_on_fpga_done       

    def run(self):
            self.info()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.server_ip, self.server_port))
                s.listen()
                while True:
                    conn, addr = s.accept()
                    
                    with conn:
                        if addr[0] not in self.clients:
                            self.clients.append(addr[0])
                            print(f"Connected by {addr[0]}\n")
                            
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            self.query = data
                            conn.sendall(str.encode(str(self.query_handler(data))))

