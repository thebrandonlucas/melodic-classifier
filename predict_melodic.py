import os, sys
import numpy as np
import random
import PySimpleGUI as sg
from predict_melodic_functions import *
from sklearn.externals import joblib

# GUI layout
main_form = sg.FlexForm('Melodic Artifact Classifier', default_element_size=(90, 1))
layout = [
	[sg.Text("Choose Melodic Directory", size=(30, 1), font=("Times", 20)), 
	sg.InputText("", size=(15, 1), font=("Times", 20)), 
	sg.FolderBrowse()], 
	[sg.Button("Add Melodic Directory", size=(55, 1), font=("Times", 20))], 
	[sg.Listbox(values=(""), size=(55, 3), font=("Times", 20), key="dataDirs")], 
	[sg.Button("Make Predictions", size=(55, 1), font=("Times", 20))], 
	[sg.Button("Exit", size=(55, 1), font=("Times", 20))]
]

main_form = main_form.Layout(layout)
origDir = os.getcwd()
dataDirs = []
while True: 
	button, values = main_form.Read()
	
	if button is None or button == "Exit": 
		break
	if button == "Add Melodic Directory": 
		if values[0] == "": 
			sg.Popup("Error", "Please enter a directory!")
			continue
		dataDirs.append(values[0])
		main_form.FindElement("dataDirs").Update(dataDirs)
	if button == "Make Predictions": 
		os.chdir("/Users/mac2researchlab/Desktop/brandon_melodic/melodic-classifier")
		with open("fix_s8_predictions.json", "w") as file: 
			model = joblib.load("extra_grd_cv.pkl")
			file.write('[\n')
			subjectCount = 0
			os.chdir(dataDirs[0])
			for root, dirs, files in os.walk(dataDirs[0]):
				# directory is subjects
				for directory in dirs:
					subject = directory
					if "Preclin" in directory:
						mriDirs = []
						for d in os.listdir(directory): 
							if "Encoding1_AP_MB4_2_5mmISO_2" in d: 
								mriDirs.append(d)
						os.chdir(directory)
						for d in mriDirs: 
							for d2 in os.listdir(d): 
								if "melodic_s8" in d2: 
									melodic_folder = d2
							os.chdir(d)
							# switch into melodic dir 
							directory = root + '/' + directory + '/' + d + '/' + melodic_folder + '/report'
							f_files = getFiles(directory, "f", "EV", "index", "IC", "._", ".html", "DS", "png", "fix")
							t_files = getFiles(directory, "t", "EV", "index", "IC", "._", "f", ".html", "DS", "png", "fix")
							os.chdir('..')
						subjectCount += 1
						file.write("\t{\n")
						file.write('\t\t"subject": "' + subject + '",\n')
			#			file.write('\t\t"predictions": [\n')
						scanCount = 0
						predictions = []
						artifact_files = []
						scans = f_files + t_files
						for scan in scans: 
							with open(scan) as scanFile: 
								scanData = scanFile.readlines()
								scanData = [float(s.strip()) for s in scanData]
								median = np.median(scanData)
								while len(scanData) < 282: 
									scanData.append(median)
							scanCount += 1
							prediction = predict(model, [scanData])
							if prediction[0] == 1: 
			#					artifactPredictionLine = str(scanCount) + ':' + '{"artifact": ' +  str(prediction) + '}'
								artifact_files.append(scanCount)
						#	else: 
			#					artifactPredictionLine = str(scanCount) + ':' + '{"non_artifact": ' + str(prediction) + '}'
			#				predictions.append(artifactPredictionLine)
			#			writeNoBraces(predictions, file, 3, 1)
			#			file.write('\t\t],\n')
						# write artifact files
						file.write('\t\t"artifact_files": [')
						for artifact in artifact_files: 
							if artifact == artifact_files[-1]: 
								file.write(str(artifact))
								break
							file.write(str(artifact) + ", ")
						file.write(']\n')
						if directory is dirs[-1]: 
							file.write('\t}\n')
						else: 
							file.write('\t},\n')
					os.chdir(root)
			file.write(']')
		sg.Popup("Done!", "File stored in: " + "/Users/mac2researchlab/Desktop/brandon_melodic/melodic-classifier")
