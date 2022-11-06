#USBin.py

import os, sys, time, shutil
import PySimpleGUIQt as sg, pyAesCrypt as aes

global drive_path; drive_path = "C:/USBin_data/drive.txt"
global quarantine_path; quarantine_path = "C:/USBin_data/quarantine.txt"

# def fileExists(path):
# 	try:
# 		with open(path, "r+") as f:
# 				f.close()
# 		return True
# 	except:
# 		return False

def fileWrite(position, content):
	with open(position, "w") as f:
		f.write(str(content))
		f.close()

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

def gui(drive, quarantine=False):
	# print("QRT: " + str(bool(quarantine=="True")))
	valid_types = {"D:/", "E:/", "F:/", "G:/", "H:/", "I:/", "J:/", "K:/", "L:/", "M:/", "N:/", "O:/", "P:/", "Q:/", "R:/", "S:/", "T:/", "U:/", "V:/", "W:/", "X:/", "Y:/", "Z:/"}
	sg.ChangeLookAndFeel('Black')
	status_changed = False
	# print("QQQ: " + quarantine)
	# [sg.InputText(password_char='*')],

	setup = [
		[sg.Text('USBin Home', size=(30, 1), font=("Helvetica", 20), text_color='white')],
		[sg.Text('This is the setup menu.', size=(20, 1.5), font=("Arial", 8), text_color='gray')], 
		[sg.Input(drive, size=(5, 1)), sg.FolderBrowse('Choose Device', size=(20, 1))],
		[sg.Checkbox('Create Desktop shortcut', key='SHORTCUT', default=True, size=(30, 1.5))],
		[sg.Checkbox('Keep files in quarantine', key='QUARANTINE', default=bool(quarantine=="True"), enable_events=True)],
		[sg.Text('')],
		[sg.Text('Password:', size=(10, 1), key='LABEL', visible=False), sg.InputText(password_char='*', key='PASSWD', size=(19.5, 1), visible=False)],
		[sg.Submit('Done', button_color=('white', 'DarkGreen'), size=(30, 1.5))]
	]

	window = sg.Window('USBin').Layout(setup).Finalize()
	window.Refresh()

	while True:

		button, device = window.Read()
		# window.Hide()

		print("Button: " + button)
		# print("Device: " + str(device["SHORTCUT"]))

		if button in (None, 'Quit'):
			sys.exit()
		elif (button == "QUARANTINE"):
			print("Quarantining...")
			print(device["QUARANTINE"])
			quarantine = False
			status_changed = True
			try:
				with open(quarantine_path, "r+") as f:
					quarantine = f.readline()
					f.close()
			except:
				with open(quarantine_path, "w") as f:
					print("QRT: "+str(device["QUARANTINE"]))
					f.write(str(device["QUARANTINE"]))
					f.close()

			# if (device["QUARANTINE"]):
			window.Element('LABEL').Update(visible=True)
			window.Element('PASSWD').Update(visible=True)
			# print(str(window.Element('PASSWD').get(visible)))
			# else:
			# window.Element('LABEL').Update(visible=False)
			# window.Element('PASSWD').Update(visible=False)
			window.Refresh()
		elif (button == "Done"):

			try:
				os.mkdir("C:/USBin_data")
			except:
				pass
			try:
				if (device["SHORTCUT"]):
					desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), ('Desktop\\' + sys.argv[0]))
					software = os.getcwd() + '\\' + sys.argv[0]
					os.symlink(software, desktop)
			except:
				pass

			with open(drive_path, "w") as f:
				f.write(device[0])
				f.close()

			if (device[0] in valid_types):
				window.Hide()
				if (status_changed):
					if (len(str(device["PASSWD"])) > 0):
						# print("My passwd: " + device["PASSWD"])
						fileWrite(quarantine_path, device["QUARANTINE"])
						file_list = os.listdir(device[0])
						file_list.remove("System Volume Information")
						if (device["QUARANTINE"]):
							# print("Gotta encrypt")
							for file in file_list:
								if (file[-3:].lower() != "aes"):
									aes.encryptFile((device[0]+file), (device[0]+file+".aes"), device["PASSWD"])
									os.remove(device[0]+file)
						else:
							# print("Gotta decrypt")
							for file in file_list:
								if (file[-3:].lower() == "aes"):
									aes.decryptFile((device[0]+file), (device[0]+file[:-4]), device["PASSWD"])
									os.remove(device[0]+file)
							


					else:
						errorPopup("Not a valid password.")
						# print("ERROR NOT A VALID PASSWORD")
				successPopup("Setup completed.")
				break
			else:
				warningPopup("The selected device may be an internal one")
				successPopup("Setup completed.")
				break
		# return


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
	quarantine = False
	try:
		with open(drive_path, "r+") as f:
			drive = f.readline()
			print("Selected drive: " + drive)
			f.close()
	except:
		print("/!\\ 'drive.txt' not found, letting the user choose a new device.")
	try:
		with open(quarantine_path, "r+") as f:
			quarantine = f.readline()
			print("Quarantining: " + quarantine)
			f.close()
	except:
		print("/!\\ 'quarantine.txt' not found, creating a new one.")
	gui(drive, quarantine)
