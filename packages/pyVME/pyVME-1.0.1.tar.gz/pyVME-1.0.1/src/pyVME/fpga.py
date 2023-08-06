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
This class can be initialized, if the users wants to run their code
on the same system as the FPGA is connected to (e.g. cbvtrig)
"""

import pyVME.vme_fpga_py as vme

class fpga():
    def __init__(self, baseaddr):
        self.baseaddr = baseaddr
        self.fpga = vme.FPGA(baseaddr)
    def readRegister(self, register):
        return self.fpga.readRegister(register)
    def writeRegister(self, register, value):
        self.fpga.writeRegister(register, value)
    def load_fpga(self, file_path):
        self.fpga.load_fpga(file_path)
    def load_fpga_xml(self, file_path):
        self.fpga.load_fpga_xml(file_path)
    def load_fpga_if_new(self, file_path):
        self.fpga.load_fpga_if_new(file_path)
    def load_fpga_if_new_xml(self, file_path):
        self.fpga.load_fpga_if_new_xml(file_path)
    def load_fpga_from_flash(self, file_path):
        self.fpga.load_fpga_from_flash(file_path)
    def async_load_fpga_from_flash(self, file_path):
        self.fpga.load_fpga_from_flash(file_path)
    def swap_bits(self, inputbits):
        self.fpga.swap_bits(inputbits)
    def getBaseaddress(self):
        return self.fpga.getBaseaddress()
    def getModulePCIBaseAdress(self):
        return self.fpga.getModulePCIBaseAdress()
    def getBoardID(self):
        return self.fpga.getBoardID()
    def getBoardType(self):
        return self.fpga.getBoardType()
    def getFirmwareVersion(self):
        return self.fpga.getFirmwareVersion()
    def getFirmwareType(self):
        return self.fpga.getFirmwareType()
    def getInterfaceVersion(self):
        return self.fpga.getInterfaceVersion()
    def getMezzanineTypes(self, number):
        return self.fpga.getMezzanineTypes(number)
    def getFPGADone(self):
        return self.fpga.getFPGADone()
    def wait_on_fpga_done(self):
        return self.fpga.wait_on_fpga_done()