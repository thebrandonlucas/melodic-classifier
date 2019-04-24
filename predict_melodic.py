import os, sys
import random
import PySimpleGUI as sg
from predict_melodic_functions import *
#from sklearn.externals import joblib

def predict(): 
	return random.uniform(0, 100)

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
		with open("fix_s8_predictions.json", "w") as file: 
		#	 model = joblib.load("melodic_model.pkl")
			subject = "Preclin_2_1"
			threshold = 85
			file.write('[\n')
			subjectCount = 0
			for i in range(0, 50): 
		#	 for subject in subjects 
				subjectCount += 1
				file.write("\t{\n")
				subjectLine = ['"subject": ', '"', subject, '"']
				file.write('\t\t"subject": "' + subject + '",\n')
				file.write('\t\t"predictions": [\n')
				scanCount = 0
				predictions = []
				artifact_files = []
				manual_review = []
				for j in range(0, 50): 
		#	   for scan in scans 
					scanCount += 1
					prediction = predict()
		#	     prediction = predict(scan)
					if prediction > threshold: 
						artifactPredictionLine = str(scanCount) + ':' + '{"artifact": ' +  str(prediction) + '}'
						artifact_files.append(scanCount)
					else: # prediction <= threshold
						artifactPredictionLine = str(scanCount) + ':' + '{"non_artifact": ' + str(prediction) + '}'
					if prediction > 50 and prediction < threshold: 
						manual_review.append(scanCount)
					#if scans[scanCount - 1] == scans[-1]: 
					predictions.append(artifactPredictionLine)
					#if j + 1 == 50: 
					#	writeNoBraces(artifactPredictionLine, file, 3, 1)
					#else: 
					#	writeNoBraces(artifactPredictionLine, file, 3, 0)
				writeNoBraces(predictions, file, 3, 1)
				file.write('\t\t],\n')
				# write artifact files
				file.write('\t\t"artifact_files": [')
				for artifact in artifact_files: 
					if artifact == artifact_files[-1]: 
						file.write(str(artifact))
						break
					file.write(str(artifact) + ", ")
				file.write('],\n')
				# write files to review
				file.write('\t\t"manual_review": [')
				for review in manual_review: 
					if review == manual_review[-1]: 
						file.write(str(review))
						break
					file.write(str(review) + ", ")
				file.write(']\n')
				#if subjects[subjectCount - 1] == subjects[-1]: 
				if i + 1 == 50: 
					file.write('\t}\n')
				else: 
					file.write('\t},\n')
			file.write(']')
