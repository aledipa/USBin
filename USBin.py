#USBin.py

import os, sys, time, shutil
import PySimpleGUIQt as sg, pyAesCrypt as aes

global drive_path; drive_path = "C:/USBin_data/drive.txt"


def warningPopup(text):
	sg.ChangeLookAndFeel('LightYellow')
	sg.Popup("/!\\ WARNING: " + text + "\n")
	return

def errorPopup(text):
	sg.ChangeLookAndFeel('DarkRed')
	sg.Popup("/x\\ ERROR: " + text + "\n")
	return

def successPopup(text):
	sg.ChangeLookAndFeel('DarkGreen')
	sg.Popup("SUCCESS! " + text + "\n")
	return

def gui(drive):
	valid_types = {"D:/", "E:/", "F:/", "G:/", "H:/", "I:/", "J:/", "K:/", "L:/", "M:/", "N:/", "O:/", "P:/", "Q:/", "R:/", "S:/", "T:/", "U:/", "V:/", "W:/", "X:/", "Y:/", "Z:/"}
	sg.ChangeLookAndFeel('Black')

	global button
	login = [
		[sg.Text('USBin Home', size=(30, 1), font=("Helvetica", 20), text_color='white')],
		[sg.Text('This is the setup menu.', size=(20, 1), font=("Arial", 8), text_color='gray')], 
		[sg.Input(drive ,size=(5, 1)), sg.FolderBrowse('Choose Device', size=(20, 1))],
		[sg.Text('')], 
		[sg.Submit('Done', button_color=('white', 'DarkGreen'), size=(30, 1.5))]
	]

	window = sg.Window('USBin').Layout(login)
	button, device = window.Read()
	window.Hide()


	if button in (None, 'Quit'):
		sys.exit()
	if (button == "Done"):
		try:
			os.mkdir("C:/USBin_data")
		except:
			pass
		with open(drive_path, "w") as f:
				f.write(device[0])
				f.close()
		if (device[0] in valid_types):
			successPopup("Setup completed.")
		else:
			warningPopup("The selected device may be an internal one")
			successPopup("Setup completed.")
	return


if len(sys.argv) > 1:
	# src_path = os.getcwd() + '\\' + sys.argv[1]
	src_path = sys.argv[1]
	print("Current dir: " + os.getcwd())
	print("Selected file: '" + src_path + "'")
	dst_path = ''
	try:
		# with open((os.getcwd()+"\\drive.txt"), "r+") as f:
		with open(drive_path, "r+") as f:
			filename = sys.argv[1].split("\\")
			filename = filename[len(filename)-1]
			dst_path = f.readline() + filename
			print(dst_path)
			f.close()
	except:
		errorPopup("Unable to locate the destination drive. \nTry setting it up from the USBin setup menu")
	


	try:
		shutil.copyfile(src_path, dst_path)
		print("File successfully transfered.")
		os.remove(src_path)
	except:
		errorPopup("Make sure that the destination device " + "(" + dst_path + ") is available.")

else:
	drive = ''
	# with open(drive_path, "r+") as f:
	# 		drive = f.readline()
	# 		print("Selected drive: " + drive)
	# 		f.close()
	try:
		with open(drive_path, "r+") as f:
			drive = f.readline()
			print("Selected drive: " + drive)
			f.close()
	except:
		print("/!\\ 'drive.txt' not found, letting the user choose a new device.")
	gui(drive)
