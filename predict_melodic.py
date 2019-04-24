import os, sys
import PySimpleGUI as sg

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
		
