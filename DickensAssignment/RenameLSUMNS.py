# Script to fix typo in files
# Change LSU to LSUMNS
# Change FMNN to FMNH

import os

rootdir = "DataFiles"


def getInstitutionName(filename):
    splittedFilename = filename.split(".")
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

    instituteName = ""
    for letter in id:
        if (letter.isalpha()):
            instituteName += letter
        else:
            return instituteName

    return instituteName


for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        foldername = subdir.split(os.sep)[-1]

        instituteName = getInstitutionName(file)

        if (instituteName == "LSU"):
            newfilepath = filepath.replace("LSU", "LSUMNS")
            os.rename(filepath, newfilepath)

        if (instituteName == "FMNN"):
            newfilepath = filepath.replace("FMNN", "FMNH")
            os.rename(filepath, newfilepath)
