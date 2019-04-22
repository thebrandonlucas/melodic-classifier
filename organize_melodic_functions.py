import os
import sys

# Returns file paths whose names contain the given substring in the directory
# "path", and appends those names to return value "array"
def getFiles(path, substring, *args):
    array = []
    for root, dirs, files in os.walk(path):
            for file in files:
                stop = False
                if substring in file:
                    for arg in args: 
                        if arg in file: 
                            stop = True
                    if stop is True: 
                        continue
                    filepath = root + '/' + file
                    array.append(filepath)
                    # print(filepath)
    return array;

# Returns the file path for a specific file within a subfolder
# def findFile(path, filename):
#     for root, dirs, files in os.walk(path):
#         for directory in dirs:
#             os.chdir(directory)
#             fileDoesExist = fileExists(filename)
#             if fileDoesExist:
#                 filepath = root + '/' + directory + '/' + filename
#                 return filepath
#             else:
#                 return None


# Determine whether a file with name "filename" exists
def fileExists(filename):
	if os.path.isfile(filename):
		return True
	else:
		return False
