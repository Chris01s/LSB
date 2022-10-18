import numpy as np
from PIL import Image
import os
import sys
from argparse import ArgumentParser


class FileNotFoundException(Exception):
        def __init__(self):
                print("[!] File does not exist!")
                sys.exit()

class FileSizeException:
        def __init__(self):
                print("[!] Bigger file sie needed!")
                print(" required pixels greater than total pixel of the image")
                sys.exit()


class LSB:
        def __init__(self, filepath):
                self.img_filepath = filepath


        def check_file_exists(self, filepath):
                if not os.path.exists(filepath):
                        raise FileNotFoundException


        def open_image_file(self):
                self.img = Image.open(self.img_filepath)


        def get_image_data(self):
                self.img_array = np.array(list(self.img.getdata()))


        def set_message_filepath(self, message_filepath):
                self.message_filepath = message_filepath


        def set_destination_filepath(self, destinaton):
                self.destination = destination

        def read_message_file(self):
                with open(self.message_filepath,"r") as FILE:
                        self.message = FILE.read()


        def binarize_message(self):
                self.message_bin = ''
                n = len(self.message)
                for i,char in enumerate(self.message):
                        self.update_count(
                                job="Binarizing Message...",
                                count=i,
                                length=n
                        )
                        bin_char = bin(ord(char)).replace('b','')
                        self.message_bin += bin_char
                print("\n")


        def calculate_total_pixels(self):
                if self.img.mode == 'RGB':
                        self.n = 3
                elif self.img.mode == 'RGBA':
                        self.n = 4
                self.total_pixels = self.img_array.size//self.n


        def check_pixel_requirements(self):
                self.required_pixels = len(self.message_bin)
                if self.required_pixels > self.total_pixels:
                        raise FileSizeException


        def hide_message(self):
                index=0
                for p in range(self.total_pixels):
                        self.update_count(
                                job="Hidden Message...",
                                count= p,
                                length=self.total_pixels
                        )

                        for q in range(0, 3):
                                if index < self.required_pixels:
                                        self.img_array[p][q] = int(bin(self.img_array[p][q])[2:9] + self.message_bin[index], 2)
                                        index += 1
                print("\n")


        def get_data_and_attributes(self):
                self.open_image_file()
                self.get_image_data()
                self.width, self.height = self.img.size
                self.calculate_total_pixels()


        def encode(self):
                self.get_data_and_attributes()
                self.message += "$t3g0"
                self.binarize_message()
                self.check_pixel_requirements()
                self.hide_message()
                self.img_array = self.img_array.reshape(self.height, self.width, self.n)
                enc_img = Image.fromarray(self.img_array.astype('uint8'), self.img.mode)
                enc_img.save(self.destination)
                print("[+] Image Encoded Successfully...")


        def get_hidden_bits(self):
                self.hidden_bits = ""
                self.update_count(
                        job="Finding hidden LSBs...",
                        count= 0,
                        length=self.total_pixels
                )
                for p in range(self.total_pixels):
                        self.update_count(
                                job="Finding hidden LSBs...",
                                count= p,
                                length=self.total_pixels 
                        )
                        for q in range(0, 3):
                                self.hidden_bits += (bin(self.img_array[p][q])[2:][-1])
                self.hidden_bits = [self.hidden_bits[i:i+8] for i in range(0, len(self.hidden_bits), 8)]
                print("\n")

        def get_hidden_message_from_bits(self):
                self.message = ""
                n = len(self.hidden_bits)
                for i in range(n):
                        self.update_count(
                                job="Finding Hidden Message...",
                                count= i,
                                length=n
                        )
                        if self.message[-5:] == "$t3g0":
                                break
                        else:
                                self.message += chr(int(self.hidden_bits[i], 2))
                print("\n")


        def check_if_hidden_message_exists(self):
                if "$t3g0" in self.message:
                        print("[+] Hidden Message: ", self.message[:-5])
                else:
                        print("[-] No Hidden Message Found")


        def decode(self):
                self.get_data_and_attributes()
                self.get_hidden_bits()
                self.get_hidden_message_from_bits()
                self.check_if_hidden_message_exists()

        def update_count(self, job, count, length):
                # the exact output you're looking for:
                filled_len = int(20*count/float(length))
                percent = round(100.0 *count/float(length),1)
                bar = "="*filled_len+"-"*(20-filled_len)
                sys.stdout.write(job+": [%s] %s%s...%s\r"%(bar, percent, "%", ''))
                sys.stdout.flush()


if __name__=="__main__":
        os.system("figlet -f lean LSB")
        argparser = ArgumentParser(
                description="LSB Steganography is an image steganography technique in which messages are hidden inside an image by replacing each pixel’s least significant bit with the bits of the message to be hidden."
        )

        argparser.add_argument("--filepath", required=True)
        argparser.add_argument("--mode",help="encode | decode", required=True)
        argparser.add_argument("--message_filepath",help="The filepath of the message to be embedded into the image", required=False)
        argparser.add_argument("--destination", help="Destination filepath of encoded image", required=False)
        args = argparser.parse_args()


        image_filepath = args.filepath

        lsb_obj = LSB(filepath=image_filepath)

        lsb_obj.check_file_exists(image_filepath)

        if args.mode=="encode":
                if args.message_filepath and args.destination:
                        message_filepath = args.message_filepath
                        destination = args.destination
                        lsb_obj.set_destination_filepath(destination)
                        lsb_obj.set_message_filepath(message_filepath)
                        lsb_obj.check_file_exists(message_filepath)
                        lsb_obj.read_message_file()
                        print("[+] Encoding image...")
                        lsb_obj.encode()
                else:
                        print("[!] Must supply a message filepath and destination filepath")
                        sys.exit()
        elif args.mode=="decode":
                print("[+] Decoding message from image...")
                lsb_obj.decode()

