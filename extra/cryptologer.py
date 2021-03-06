#errors cant access vigenere_dec from other folder...
#imports improperly from rsa-encryptor when kept in different

#file should have all ciphers as simple format... just text
#for rsa_dec, file should have text as n:<no...> \n c:<no....> e:<no....>
#same for rsa_enc...


#importing...
import sys
import re
import argparse
import operator
import math
import requests
import json
import binascii

sys.path.append('C:\\Users\\immas\\Desktop\\Main\\Encrypting\\')
sys.path.append('C:\\Users\\immas\\Desktop\\Main\\Decrypting\\')
sys.path.append('C:\\Users\\immas\\Desktop\\Main\\Algorithms\\')

#file imports for encryption
from caeser import julius,bruteforce
from vigenere_enc import encrypt
from affine_enc import aff_enc
from bacon_enc import steak
from railfence_enc import rail
from atbash import atb
from polybius_enc import tsquaree
from substitution_enc import substitute
from rsa_encryptor import rivest

#algorithms import
from Ext_Euclid import reversing

#file imports for decryption
from vigenere_dec import impossible, withkey#import impossible, withkey
from affine_dec import fine
from bacon_dec import pork
from polybius_dec import psquaree
from railfence_dec import fence
from substitution_dec import manual
from simplersa import init
from Weiner import attack

#parsing starts
def initializeParser():

	parser=argparse.ArgumentParser(description="Decryptor for Caeser, Vigenere, types of RSA and more...")

	parser.add_argument("--decrypt","--dec","-d",help="Performs Decryption",action="store_true")
	parser.add_argument("--encrypt","--enc","-e",help="Performs Encryption",action="store_true")
	parser.add_argument("--sourcefile","--sf","-f",help="Input file with ciphertext",type=str)
	parser.add_argument("--caeser","-C",help="If the cipher is caeser cipher",action="store_true")
	parser.add_argument("--vignere","-V",help="If the cipher is vignere cipher",action="store_true")
	parser.add_argument("--key","-k",help="If the key is known (text for vignere, shift for caeser)",type=str)
	parser.add_argument("--affine","-A",help="If the cipher is affine cipher",action="store_true")
	parser.add_argument("--bacon","-B",help="If the cipher is bacon cipher",action="store_true")
	parser.add_argument("--polybius","-P",help="If the cipher is encrypted by a simple 6x6 polybius square",action="store_true")
	parser.add_argument("--railfence","-F",help="If railfence encryption is used",action="store_true")
	parser.add_argument("--atbash","-T",help="If atbash rotation is done on the plaintext",action="store_true")
	parser.add_argument("--substitution","-S",help="If the plaintext in encrypted using simple substitution cipher",action="store_true")
	parser.add_argument("--rsa","-R",help="If the cipher is RSA related",action="store_true") #contains simple and multi_rsa
	
	#parser.add_argument("--factordb","--fb","-O",help="Using factordb to crack the rsa",action="store_true")
	parser.add_argument("--weiner","-W",help="Cracking RSA using Weiner attack",action="store_true")
	parser.add_argument("--smalle","-E",help="Cracking RSA provided e is very small",action="store_true")
	parser.add_argument("--internal","-I",help="If an internal attack for RSA is being performed",action="store_true")
	parser.add_argument("--fermat","-M",help="Fermat's attack on the RSA encrypted text",action="store_true")
	parser.add_argument("--twin","-N",help="If the RSA public is a product of twin prime, use this",action="store_true")
	parser.add_argument("--chinese","-H",help="Using the Chinese Remainder Theorem for cracking RSA from e packets having the same n",action="store_true")

	return parser

def readfile(filename):
	with open(filename,"r") as f1:
		return f1.read()

def read_rsa(filename):
	with open(filename,"r") as f2:
		line=f2.readline()
		while line:
			symbol=line[0]
			if symbol=='n':
				n=int(line[2:])
			elif symbol=='e':
				e=int(line[2:])
			elif symbol=='c':
				c=int(line[2:])
			elif symbol=='m':
				c=line[2:]
			else:
				raise Exception("the contents of the file can't be read properly")
				break
			line=f2.readline()

	return n,e,c


def main():
	parser=initializeParser()
	args=parser.parse_args()

	if args.encrypt or args.decrypt:
		rawtext=readfile(args.sourcefile)
		key=args.key



	if args.encrypt:
		plaintext=rawtext
		if args.caeser:
			shift=int(input("enter shift:"))
			ciphertext=julius(plaintext,shift)
		elif args.vignere:
			key=input("enter key:")
			ciphertext=encrypt(plaintext,key)
		elif args.affine:
			ciphertext=aff_enc(plaintext)
		elif args.bacon:
			ciphertext=steak(plaintext)
		elif args.railfence:
			ciphertext=rail(plaintext)
		elif args.atbash:
			ciphertext=atb(plaintext)
		elif args.polybius:
			ciphertext=tsquaree(plaintext)
		elif args.substitution:
			ciphertext=substitute(plaintext)
		elif args.rsa:
			n,e,m=read_rsa(args.sourcefile)
			ciphertext=rivest(n,e,m)
			display='message:'

		try:
			print("ciphertext:",ciphertext,end='')
		except UnboundLocalError:
			print("NullError: no ciphering technique mentioned")

	elif args.decrypt:
		ciphertext=rawtext
		display='plaintext:'
		if args.caeser:
			if args.key!=None:
				plaintext=julius(ciphertext,-int(key))
			else:
				display=''
				plaintext=bruteforce(ciphertext)

		elif args.vignere:
			if key!=None:
				plaintext=withkey(ciphertext,key)
			else:
				plaintext=impossible(ciphertext)
		elif args.affine:
			plaintext=fine(ciphertext)
		elif args.bacon:
			plaintext=pork(ciphertext)
		elif args.railfence:
			plaintext=fence(ciphertext)
		elif args.atbash:
			plaintext=atb(ciphertext)
		elif args.polybius:
			plaintext=psquaree(ciphertext)
		elif args.substitution:
			plaintext=manual(ciphertext)
		
		elif args.rsa:
			n,e,c=read_rsa(args.sourcefile)
			plaintext=init(n,e,c)
			display='message:'
		elif args.weiner:
			n,e,c=read_rsa(args.sourcefile)
			plaintext=reversing(n,attack(e,n),c)
			


		try:
			print("%s" % display,plaintext,end='')
		except:
			print("NullError: no ciphering technique mentioned")




if __name__=="__main__":
	main()

