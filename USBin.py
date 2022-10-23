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

	setup = [
		[sg.Text('USBin Home', size=(30, 1), font=("Helvetica", 20), text_color='white')],
		[sg.Text('This is the setup menu.', size=(20, 1.5), font=("Arial", 8), text_color='gray')], 
		[sg.Input(drive ,size=(5, 1)), sg.FolderBrowse('Choose Device', size=(20, 1))],
		[sg.Checkbox('Create Desktop shortcut', key='shortcut', default=True, size=(30, 1.5))],
		[sg.Text('')],
		[sg.Submit('Done', button_color=('white', 'DarkGreen'), size=(30, 1.5))]
	]

	window = sg.Window('USBin').Layout(setup)
	button, device = window.Read()
	window.Hide()

	print("Button: " + button)
	print("Device: " + str(device["shortcut"]))

	if button in (None, 'Quit'):
		sys.exit()
	elif (button == "Done"):

		try:
			os.mkdir("C:/USBin_data")
		except:
			pass
		try:
			if (device["shortcut"]):
				desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), ('Desktop\\' + sys.argv[0]))
				software = os.getcwd() + '\\' + sys.argv[0]
				os.symlink(software, desktop)
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
	src_paths = []
	dst_paths = []
	filenames = []
	for i in range(len(sys.argv)-1):
		src_paths.append(sys.argv[i+1])
		file = sys.argv[i+1].split("\\")
		filenames.append(file[len(file)-1])
	print("Current dir: " + os.getcwd())
	print("Selected file: '" + src_paths[i] + "'")


	try:
		with open(drive_path, "r+") as f:
			dst = f.readline()
			print(dst)
			f.close()
		for i in range(len(filenames)):
			dst_paths.append(dst + filenames[i])
			# errorPopup("Destination: " + dst + filenames[i])
	except:
		errorPopup("Unable to locate the destination drive. \nTry setting it up from the USBin setup menu")
	

	try:
		for i in range(len(dst_paths)):
			shutil.copyfile(src_paths[i], dst_paths[i])
			os.remove(src_paths[i])
			print("File successfully transfered.")
	except:
		errorPopup("Make sure that the destination device " + "(" + dst_paths + ") is available.")

else:
	drive = ''
	try:
		with open(drive_path, "r+") as f:
			drive = f.readline()
			print("Selected drive: " + drive)
			f.close()
	except:
		print("/!\\ 'drive.txt' not found, letting the user choose a new device.")
	gui(drive)
