#!/usr/bin/python3

import os
import sys
""" Program to find archives with needed extensions to sort and organize them in a new folder """

def source_path(folder):
	folder = os.path.abspath(folder)
	print(folder)
	if os.path.exists(folder):
		return os.chdir(folder)
	else:
		print("Folder don't exists.")

def walk_path(folder):
	""" Function to find given archive extension on given folder """
	for (root, dirs, files) in os.walk(os.getcwd()):
		print(root, dirs, files)

def target():
	""" Function to create new dir and attach the archives """
	pass

if __name__=='__main__':
	starting_path = source_path(sys.argv[1])
	print(starting_path)
	#walk_path(starting_path)