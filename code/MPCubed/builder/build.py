#!/usr/bin/python

from subprocess import call
import os

filenames = []


def ask_build_version():
	return raw_input("Which version do you want to build?\n\nall or toybox/DFPToybox/DFPToyboxPortrait\n>")


def run_build(build_version):
	filenames = []
	if build_version == "toybox":
		filenames = ['../src/js/BrowserTools.js', '../src/js/CubeAd.js']
	elif build_version == "DFPToybox":
		filenames = ['../src/js/BrowserTools.js', '../src/js/CubeAd.js', '../src/js/DFPCubeAd.js']
	elif build_version == "DFPToyboxPortrait":
		filenames = ['../src/js/BrowserTools.js', '../src/js/CubeAd.js', '../src/js/DFPCubeAd.js',
					 '../src/js/DFPPortraitCubeAd.js']
	else:
		print "Version not recognised"
		exit()

	with open('./concat.js', 'w') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					if "CubeAd.prototype.DEBUG = true;" in line:
						line = "CubeAd.prototype.DEBUG = false;"
					outfile.write(line)
				outfile.write("\n\n")
	outfile.close()

	check_success(
		call("java -jar yuicompressor-2.4.8.jar -o ../release/" + build_version + ".min.js concat.js", shell=True),
		build_version)
	os.remove("./concat.js")


def check_success(output, file):
	if output == 0:
		print "Build Success: " + file
	else:
		print "Error building: " + file


build_response = ask_build_version()

if build_response == "all":
	run_build("toybox")
	run_build("DFPToybox")
	run_build("DFPToyboxPortrait")
	check_success(
		call("java -jar yuicompressor-2.4.8.jar -o ../release/toybox.min.css ../src/css/toybox-style.css", shell=True),
		"Toybox CSS")
	print("Output files in ../release")
else:
	run_build(build_response)
	check_success(
		call("java -jar yuicompressor-2.4.8.jar -o ../release/toybox.min.css ../src/css/toybox-style.css", shell=True),
		"Toybox CSS")
	print("Output files in ../release")
