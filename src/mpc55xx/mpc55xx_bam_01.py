# 
# The MIT License (MIT)
# 
# Copyright (c) 2014, 2015 Kobler Systems GmbH
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# 
# this software and 
# associated documentation files (the "Software"), 
# 
# to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Author: Jan Kobler, Kobler Systems GmbH, email: eng1@koblersystems.de
#

import io
import serial

import subprocess
import sys

import traceback

import os

import argparse
import binascii

import time

class bam_01:
    
    def __init__(self):
        self.ser1 = None
        self.pos1 = 0
        self.ser_port1 = '/dev/ttyUSB0'
        self.flag_test1 = "asm" # Test: "echo", "asm"
        self.load_address1 = 0x40000000
        self.sram_size1 = 0x10000
        self.sram_start1 = 0x40000000
        self.flag_test3 = False
        self.file_name1 = "test.bin"
        self.ser_sync1 = False
        self.flag_debug1 = False
        self.password1 = "FEED FACE CAFE BEEF"
        self.send_wait1 = None # Time in seconds, float
        self.ser_baudrate1 = 9600
        self.ser_baudrate2 = 115200
        self.flag_debug2 = False
        self.flag_debug3 = False
	
    
    def test_01(self):
        
        if True:
            self.ser1 = serial.Serial(self.ser_port1, self.ser_baudrate1, timeout=30)
            self.pos1 = 0
            
        pw1 = self.get_password1()
        
        self.send_sync1()
        
        self.show_send_wait1()
        
        # write password
        print("Password", pw1)
        self.write_01(pw1)
 
        sram1 = (self.load_address1,self.sram_size1) # start, len
        image1 = (sram1[0], 0x40)  # image: start, len
        
        if image1[1]%8 != 0:
            raise Exception("Image length has to be multiple of 8 because of 64bit access to SRAM")
        
        # write destination
        self.write_01(image1[0].to_bytes(4,'big'))
        self.write_01(image1[1].to_bytes(4,'big'))
        
        
        print("uploading data to the target")
        self.pos1 = 0
        if self.flag_test1 == "asm":
            code1 = "3c 60 40 00 38 a0 00 00 38 a5 00 01 90 a3 00 20 4b ff ff f8"
            code2 = bytes.fromhex(code1)
            self.write_01(code2)
            
            while self.pos1 < image1[1]:
                self.write_01((0x00).to_bytes(1,'big'))
        elif self.flag_test1 == "echo": 
            for d1 in range(image1[1]//4):
                self.write_01(d1.to_bytes(4,'big'))
        else:
            print("unknown test type", self.flag_test1, file=sys.stderr)
            
        print("Done")


    def test_02(self):
        """
        start1: start address of application, int
        file_name_1: file name, str
        """
        file_name1 = self.file_name1
        
        start1 = self.load_address1
        
        if start1 < self.sram_start1:
            print("Load Address is to small", hex(start1), "instead of", hex(self.sram_start1), file=sys.stderr )

        sram_end1 = self.sram_start1 + self.sram_size1
        if start1 >= sram_end1:
            print("Load Address is to large", hex(start1), "end of sram is", hex(sram_end1), file=sys.stderr )
        
        fs1 = os.stat(file_name1)
        size1 = fs1.st_size
                
        size_max_1 = self.sram_size1
        
        if size1 > size_max_1:
            raise Exception("image is to large")
        
        fb1 = open(file_name1, "rb")
        
        
        
        print("File:", file_name1, "Size:", size1)
        
        if True:
            self.ser1 = serial.Serial(self.ser_port1, self.ser_baudrate1, timeout=30)
            self.pos1 = 0
                                
        pw1 = self.get_password1()

        self.send_sync1()
        
        self.show_send_wait1()
        
        # write password
        print("Password", pw1)
        self.write_01(pw1)
 
        
        size2 = size1 + size1%8
        image1 = ( start1, size2)  # image: start, len
        
        if image1[1]%8 != 0:
            raise Exception("Image length has to be multiple of 8 because of 64bit access to SRAM")
        
        # write destination
        self.write_01(image1[0].to_bytes(4,'big'))
        self.write_01(image1[1].to_bytes(4,'big'))
        
        
        print("uploading data to the target")
        self.pos1 = 0
        if True:
            while True:
                d1 = fb1.read(1024)
                if d1 is None:
                    raise Exception("file is blocked")
                elif len(d1) == 0:
                    print("File end reached")
                    break
            
                self.write_01(d1)
            
            fb1.close()
            
            print("written", self.pos1, "Bytes")
            if self.pos1 != size1:
                print("wrong number written", self.pos1, "instead of", size1)
                
            while self.pos1 < image1[1]:
                self.write_01((0x00).to_bytes(1,'big'))
            
        elif True:
            code1 = "3c 60 40 00 38 a0 00 00 38 a5 00 01 90 a3 00 20 4b ff ff f8"
            code2 = bytes.fromhex(code1)
            self.write_01(code2)
            
            while self.pos1 < image1[1]:
                self.write_01((0x00).to_bytes(1,'big'))
        else:
            for d1 in range(image1[1]//4):
                self.write_01(d1.to_bytes(4,'big'))
            
        print("Done")

            
    def write_01(self, buf1):
        """
        buf1: bytes
        """
        if not isinstance(buf1, bytes):
            raise Exception("buf1 has to be bytes")
        
        for b1 in buf1:
            
            if self.flag_debug2:
                print("pos: ", hex(self.pos1),"write: ", hex(b1))
            elif self.pos1 % 1024 == 0:
                print("pos: ", hex(self.pos1))
                
            if self.ser1 is not None:
                if self.send_wait1:
                    time.sleep(self.send_wait1)
                self.ser1.write(b1.to_bytes(1,byteorder='big'))
                b2 = self.ser1.read()
                if self.flag_debug1:
                    print("read:", b2, "len:", len(b2))

                if len(b2)>1:
                    raise Exception("more than one byte returned")
                
                if b2 is None or len(b2)==0:
                    raise Exception("Nothing returned, time out")
                elif b2[0] != b1:
                    raise Exception("wrong character returned: " + hex(b2[0]) + " expected: " + hex(b1))
            self.pos1 += 1

    def send_sync1(self):
        
        if self.ser_sync1 == True:
            b1 = 0x0
            print("MPC56xx Baud Rate detection, send 0x0 as test frame")
            if self.flag_debug2:
                print("pos: ", hex(self.pos1),"write: ", hex(b1))
            self.ser1.write((0x0).to_bytes(1,byteorder='big'))    
            # No answer expected
            self.pos1 += 1

    def get_password1(self):
        
        # serial boot password
        pw1 = bytes.fromhex(self.password1)
        if len(pw1) != 8:
            print("Warning: Password length:", len(pw1), "is wrong, required", 8, "It will be sent, but the password is definitely wrong")
        return pw1
    
    def show_send_wait1(self):
        if self.send_wait1 is not None:
            print( "Waiting " + str(self.send_wait1) + "s before sending")

    def test_03(self):
        """ read output """
        
        if self.ser1 is not None:
            self.ser1.close()

        speed1 = self.ser_baudrate2
        self.ser1 = serial.Serial(self.ser_port1, speed1, timeout=30)
        self.pos1 = 0
        
        self.input_reset_01()
        
        print("Waiting for output, speed", speed1)
        print()
        
        while True:
            b2 = self.ser1.read(1)
            if b2 is None or len(b2) == 0:
                #raise Exception("None returned, time out: ")
                print()
                print("Timeout: no longer waiting for output")
                break
                
            for b1 in b2:
                if self.flag_debug3:
                    print("Returned: " + hex(b1) + " '" + str(b1) + "' " + chr(b1) )
                else:
                    if b1 == 13:
                        pass
                    elif b1 == 10:
                        print()
                    elif b1 < 32 or b1 == 127:
                        print("("+hex(b1)+")",end='')
                    else:
                        print(chr(b1),end='')
                self.input_state_03(b1, b"This is a test. I am sending something longer. Does it arrive?\n")   # NL at the end is important
                    
    def input_reset_01(self):
        self.input_state_02 = input_state_01("mpc5676>")
        self.input_state_02.reset_state_01()
        
    
    def input_state_03(self, b1, text1):
        """
        b1: int
        """
        
        self.input_state_02.step_01(b1);
        if self.input_state_02.found_prompt2():
            self.input_state_02.found_prompt_ack_01()
            for c2 in text1:
                self.ser1.write((c2,))
                b2 = self.ser1.read(1)
                
                if len(b2)>1:
                    raise Exception("more than one byte returned")
                
                if b2 is None or len(b2)==0:
                    raise Exception("Nothing returned, time out")
                elif b2[0] != c2:
                    raise Exception("wrong character returned: " + hex(b2[0]) + " expected: " + hex(c2))
                
            print("Text:", text1, "has been echoed after prompt")
        
    def parse_args_01(self, test_args1 = None):
        
        p1 = argparse.ArgumentParser()
        
        g1 = p1.add_mutually_exclusive_group()
        g1.add_argument("--test", help="some preconfigured tests", choices=('echo', 'asm',))
        g1.add_argument("--image", help="download binary image")
        
        p1.add_argument("--address", help="load address, hex value, no leading 0x", default="40000000")
        
        if sys.platform.startswith("win32"):
            sys_port1 = "COM1:"
        else:
            sys_port1 = "/dev/ttyUSB0"
        
        
        p1.add_argument("--port", help="serial port", default=sys_port1)
        
        p1.add_argument("--listen", action="store_true", help="listen to serial port AFTER uploading",)
        p1.add_argument("--listen_baudrate", type=int, help="listen to serial port AFTER uploading with this baudrate, e.g. 115200",)

        p1.add_argument("--sync", action="store_true", help="MPC56xx only: send sync byte at the beginning for Baud Rate Detection ")
        p1.add_argument("--start_baudrate", type=int, help="MPC56xx: start with baudrate, MPC55xx: only 9600")

        p1.add_argument("--debug", action="store_true", help="provide debug output")
        p1.add_argument("--debugWrite", action="store_true", help="provide debug output for write to target serial port")
        p1.add_argument("--debugRead", action="store_true", help="provide debug output for read from target serial port")
        
        p1.add_argument("--password", help="Password: 8byte, hex, spaces allowed, e.g. FEED FACE CAFE BEEF")
        p1.add_argument("--sendwait", help="Time to wait before sending a byte, in seconds, may be float number")
        
        # parse
        a1 = p1.parse_args(test_args1)
        
        if not a1.test and not a1.image:
            # only show help
            p1.print_help()
        
        else:
            # info
            
            if a1.test:
                print("test:", a1.test)
            if a1.image:
                print("image:", a1.image)
            if a1.address:
                a2 = binascii.a2b_hex(a1.address)
                a3 = int.from_bytes(a2, byteorder='big')
                print("address: hex", a1.address, "as integer", a3)
                
            if a1.port:
                print("port:", a1.port)
                
            if a1.listen:
                print("wait for output:", a1.listen)
                
            if a1.listen_baudrate:
                print("after uploading wait for output with baudrate:", a1.listen_baudrate)
               
            if a1.sync:
                print("Sync: ", a1.sync)
                
            if a1.start_baudrate:
                print("Start with baudrate: ", a1.start_baudrate)
                
            if a1.debug:
                print("Debug: ", a1.debug)
                
            if a1.password:
                print("Password:", a1.password)
                
            if a1.sendwait:
                print("Sendwait:", a1.sendwait)
                
                
            print()
            # copy settings and start
            
            if a1.port:
                self.ser_port1 = a1.port
            
            if a1.address:
                self.load_address1 = a3
                
            if a1.listen:
                self.flag_test3 = a1.listen
                
            if a1.listen_baudrate:
                self.ser_baudrate2 = a1.listen_baudrate
                
            if a1.sync:
                self.ser_sync1 = a1.sync
                
            if a1.start_baudrate:
                self.ser_baudrate1 = a1.start_baudrate
                
            if a1.debug:
                self.flag_debug1 = a1.debug
                
            if a1.debugWrite:
                self.flag_debug2 = a1.debugWrite

            if a1.debugRead:
                self.flag_debug2 = a1.debugRead
                
            if a1.password:
                self.password1 = a1.password
                
            if a1.sendwait:
                self.send_wait1 = float(a1.sendwait)
                
            # start 
            if a1.test:
                
                self.flag_test1 = a1.test
                self.test_01()
                
            elif a1.image:
                
                self.file_name1 = a1.image
                self.test_02()
                if b1.flag_test3:
                    b1.test_03()

class input_state_01:
    
    def __init__(self, prompt):
        """
        prompt: str
        """
        self.state_list1 = ("wait_prompt", "in_prompt", "wait_NL")
        self.state1 = None
        self.prompt_01 = prompt
        self.prompt_pos_01 = 0
        self.found_prompt1 = False
        self.state_debug1 = False
        
        
    def reset_state_01(self):

        self.prompt_pos_01 = 0
        self.state1 = "wait_prompt"
        self.found_prompt1 = False
        
    def step_01(self, b1):
        
        state0 = self.state1
        
        if self.state1 == "wait_prompt":
            self.found_prompt1 = False # only one cycle True
            if chr(b1) == self.prompt_01[self.prompt_pos_01]:
                self.prompt_pos_01 += 1
                self.state1 = "in_prompt"
        elif self.state1 == "in_prompt":
            if chr(b1) == self.prompt_01[self.prompt_pos_01]:
                self.prompt_pos_01 += 1
                if self.prompt_pos_01 == len(self.prompt_01):
                    self.state1 = "wait_NL"
            else:
                self.reset_state_01()
                
        elif self.state1 == "wait_NL":
            if b1 == 13:
                pass
            elif b1 == 10:
                self.found_prompt1 = True
                self.state1 = "wait_prompt"
                self.prompt_pos_01 = 0
            else:
                self.reset_state_01()
                
        if self.state_debug1:
            print("Input:",b1, hex(b1), chr(b1), end=', ')
            if self.state1 == state0:
                print("State:", self.state1, end=', ')
            else:
                print("State:", state0, "->", self.state1, end=', ')
            if self.state1 == "wait_prompt" or self.state1 == "in_prompt":
                print("prompt_pos_01=", self.prompt_pos_01 , end=', ')
                print("wait for: ", self.prompt_01[self.prompt_pos_01], end=', ')
                
            if self.found_prompt1:
                print("found_prompt1", end=', ')
                
            print()
                
    def found_prompt2(self):
        return self.found_prompt1
    
    def found_prompt_ack_01(self):
        if self.found_prompt1:
            self.found_prompt1 = False
            

def main_01():
    b1 = bam_01()
    b1.parse_args_01()    

if __name__ == '__main__':

    main_01()    
