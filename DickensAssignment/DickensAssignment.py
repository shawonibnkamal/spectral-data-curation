import os
import csv

# Create a folder named OutputFiles
if not os.path.exists("OutputFiles"):
    os.makedirs("OutputFiles")


def patch_name(a):
    if a == "H":
        return "Head"
    elif a == "R":
        return "Rump"
    elif a == "T":
        return "Upper Tail"
    elif a == "U":
        return "Chest"
    elif a == "S":
        return "Sub-terminal tail band"
    elif a == "M":
        return "Mantle"
    elif a == "B":
        return "Belly"
    elif a == "MB":
        return "Male Belly"


# copy the filenames from the directory
filenames = [name for path, subdirs, files in os.walk("DataFiles")
             for name in files]

print(len(filenames), "no. of files")

# opens the csv of meta data and stores it in list data
with open('template.csv', newline='') as templateCsvFile:
    reader = csv.reader(templateCsvFile)
    data = list(reader)

# opens a csv for filenames that do not have a meta data
missingMetaCsvFile = open('OutputFiles/MissingMeta.csv', 'w', newline='')
missingMeta = csv.writer(missingMetaCsvFile)
missingMeta.writerow(['notmatched'])

# counts
matchFound = 0
matchNotFound = 0

# copies the list of meta data to another list
# will contain the list of meta data that do not have any files
missingFiles = list(data)


def compareWithTemplate(writer, patch, id, replicate, filename, modify):
    global matchFound, matchNotFound
    matchBool = False
    for i in data:  # loops through the list of meta data
        templateId = i[1]+i[3]
        if id == templateId:  # if match found
            matchBool = True
            matchFound += 1
            i[0] = modify
            i[20] = patch_name(patch)
            i[25] = replicate
            writer.writerow(i)  # add infos and write it to Result.csv
            exit

    if(matchBool == False):  # if match not found
        matchNotFound += 1
        missingMeta.writerow([filename])  # add filename to MissingMeta.csv

    for j in missingFiles:
        templateId = j[1]+j[3]
        if id == templateId:
            missingFiles.remove(j)
            exit


with open('OutputFiles/Result.csv', 'w', newline='') as resultCsvFile:
    writer = csv.writer(resultCsvFile)
    writer.writerow(data[0])

    # loop through list of filenames
    for i in range(len(filenames)):
        splittedFilename = filenames[i].split(".")
        if (splittedFilename[4] == "spec"):
            patch = splittedFilename[1]
            id = splittedFilename[2]
            modify = splittedFilename[0]+"."+splittedFilename[1]+"." + \
                splittedFilename[2]+"." + \
                splittedFilename[3] + "."+splittedFilename[4]
            replicate = splittedFilename[3]
        elif(splittedFilename[4] == "csv"):
            patch = splittedFilename[1]
            id = splittedFilename[2]
            modify = splittedFilename[0]+"."+splittedFilename[1] + \
                "."+splittedFilename[2]+"."+splittedFilename[3]
            replicate = splittedFilename[3]
        elif((len(splittedFilename[1]) == 1) and (len(splittedFilename[2]) == 1)):
            patch = splittedFilename[1] + splittedFilename[2]
            id = splittedFilename[3]
            modify = splittedFilename[0]+"."+splittedFilename[1]+"." + \
                splittedFilename[2]+"."+splittedFilename[3] + \
                "."+splittedFilename[4]
            replicate = splittedFilename[4]

        else:
            patch = splittedFilename[1]
            id = splittedFilename[2]
            modify = splittedFilename[0]+"."+splittedFilename[1] + \
                "."+splittedFilename[2]+"."+splittedFilename[3]
            replicate = splittedFilename[3]

        compareWithTemplate(writer, patch, id, replicate, filenames[i], modify)

with open('OutputFiles/MissingFiles.csv', 'w', newline='') as missingFilesCsv:
    missingFilesWriter = csv.writer(missingFilesCsv)
    for row in missingFiles:
        missingFilesWriter.writerow(row)

print(matchFound, "match found")
print(matchNotFound, "match not found")
print("Complete")

# Close all opened files
templateCsvFile.close()
resultCsvFile.close()
missingFilesCsv.close()
missingMetaCsvFile.close()
