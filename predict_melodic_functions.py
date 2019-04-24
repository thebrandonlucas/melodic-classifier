# indent json file
def indent(indentationLevel, myFile):
        for i in range(0, indentationLevel):
                myFile.write("\t")

# Loop through each string, writing each data element
# in surrounding braces
def writeInBraces(stringArray, myFile, indentationLevel, isLastDataPoint):
        # top brace
        indent(indentationLevel, myFile)
        myFile.write("{\n")
        # strings
        for str in stringArray:
                # if last element, no comma
                if str is stringArray[-1]:
                        indent(indentationLevel + 1, myFile)
                        myFile.write(str + "\n")
                else:
                        indent(indentationLevel + 1, myFile)
                        myFile.write(str + ",\n")
        # bottom brace
        indent(indentationLevel, myFile)
        if isLastDataPoint is 1:
                myFile.write("}\n")
        else:
                myFile.write("},\n")

# Write element to file with the given indentation level, without brace wrap
def writeNoBraces(stringArray, myFile, indentationLevel, isLastDataPoint):
        for str in stringArray:
                # if last element, no comma
                if str is stringArray[-1] and isLastDataPoint is 1:
                        indent(indentationLevel, myFile)
                        myFile.write(str + "\n")
                else:
                        indent(indentationLevel, myFile)
                        myFile.write(str + ",\n")
