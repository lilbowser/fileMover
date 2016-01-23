import os
import string
import shutil
import re
import time

__version__ = "0.5.3"
minutes = 60
sleepTime = 2 * minutes
subDirScans = True
while (1):

    baseDir = os.getcwd()

    if baseDir[-1] == "\\":  # this is needed incase we are in the root directory which will already end in a \
        baseDirEnd = ""
    else:
        baseDirEnd = "\\"
    # scanDir = baseDir
    sourceScanDir = baseDir + baseDirEnd + "Unsorted-Files"
    # sourceScanDir = baseDir + baseDirEnd + "workspace"

    # animeDir = baseDir
    # animeDir = baseDir + baseDirEnd + "Unsorted-Files"
    animeDir = baseDir + baseDirEnd + "Unsorted Anime"
    tvShowDir = baseDir + baseDirEnd + "TV Shows"

    destinationScanDir = animeDir

    overrideFileName = "fileMoverOverride.ini"
    overrideFilePath = baseDir + baseDirEnd + overrideFileName

    # NonAnimeShowIDs must be entered in lower case
    nonAnimeShowID = ["the.daily.show", "the.nightly.show", "last.week.tonight.with.john.oliver",
                      "the.late.show.with.stephen.colbert"]
    nonAnimeShowBaseDir = sourceScanDir + "\\"

    specialCaseNonAnimeShowID = ["steven.universe"]
    specialCaseNonAnimeBaseDir = sourceScanDir + "\\"

    # print directoryFileList


    # ---Sort the files and directories into individual lists
    fileList = []
    rejectFileList = []
    dirList = []
    overrideList = []

    destDirList = []
    destFileList = []


    # --Begin of SubDir Scans
    if (subDirScans):  # Option to turn sunDir moving off

        directoryFileList1 = os.listdir(sourceScanDir)  # This scans the scanDir
        for item in directoryFileList1:
            if os.path.isdir(sourceScanDir + "\\" + item):
                dirList.append(item)
            elif os.path.isfile(sourceScanDir + "\\" + item):
                fileList.append(item)

        for subDirBasePath in dirList:
            # go into each subdirectory. Scan the first file. if it matches as an ani, move the entire subdir into animeDir.

            subDirURI = sourceScanDir + "\\" + subDirBasePath
            subDirFileList = []  # Create a list of all files in the subDir
            subSubDirList = []  # Create a list of all dirs in the subDir
            # rejectSubDirFileList = []
            lftpDownloading = False
            skipDir = True
            subDirFilesAndFoldersList = os.listdir(subDirURI)  # Create a list of all files and folders in the subdir

            for item in subDirFilesAndFoldersList:  # Seperate files and folders in the scaned subdir
                if os.path.isdir(subDirURI + "\\" + item):
                    subSubDirList.append(item)
                elif os.path.isfile(subDirURI + "\\" + item):
                    subDirFileList.append(item)

            for item in subDirFileList:
                if (item.find("lftp-pget-status") != -1):
                    lftpDownloading = True
                # rejectSubDirFileList.append( item[0:item.rfind('.',0,len(item))] )
                # print item[0:item.rfind('.',0,len(item))]

            for item in subDirFileList:
                seriesName = item.lstrip()  # Strip any leading whitespace from the filename
                if (seriesName[0] == '[' and lftpDownloading == False):
                    # The file (and thus subdir) is an animu folder and we should move it.
                    skipDir = False

            if skipDir == False:  # We need to move the subDir.
                print "Moving subDir into animu folder"
                print subDirURI, animeDir  # + "\\" + subDirBasePath
                try:
                    shutil.move(subDirURI, animeDir)  # sourced dir, dest dir
                except:
                    print "Folder already exsists. Unable to move!"

                # ---
    # end subdir scaning


    # Load the override list
    try:
        overrideFile = open(overrideFilePath, 'r')
        for line in overrideList:
            overrideList.append(line)

    except IOError as e:  # If no override list is found, move on.
        print "No override file found. Continuing."

    # ---Scan through the directory/file list and sort them into the apropriate list
    # Recreate the lists so they are empty
    dirList = []
    fileList = []

    directoryFileList = os.listdir(sourceScanDir)  # Rescan the scanDir incase we changed it after the subDir moving.
    for item in directoryFileList:
        if os.path.isdir(sourceScanDir + "\\" + item):
            dirList.append(item)
        elif os.path.isfile(sourceScanDir + "\\" + item):
            fileList.append(item)

    # ---Scan through the destination directory/file list and sort them into the apropriate list
    destinationFolderList = os.listdir(destinationScanDir)
    for item in destinationFolderList:
        if os.path.isdir(destinationScanDir + "\\" + item):
            destDirList.append(item)
        elif os.path.isfile(destinationScanDir + "\\" + item):
            destFileList.append(item)


        # ---Create a file ignore list based on the presence of .lftp-pget-status files
    for item in fileList:
        if (item.find("lftp-pget-status") != -1):
            rejectFileList.append(item[0:item.rfind('.', 0, len(item))])
        # print item[0:item.rfind('.',0,len(item))]

        # ---Begin iterating through the files.
    for item in fileList:
        lftpDownloading = False
        for rItem in rejectFileList:  # Ensure we do not move a file that is indicated to be downloading.
            if rItem == item:
                lftpDownloading = True

        for oItem in overrideList:  # see if we are overriding the detection of the series.
            if oItem == item:
                lftpDownloading = True

        if item.find(
                'lftp-pget-status') > -1:  # see if file ends with lftp indicator to ensure we do not move the lftp indicator file
            lftpDownloading = True

        seriesName = item.lstrip()  # Strip any leading whitespace from the filename\

        if (seriesName[0] == '[' and lftpDownloading == False):

            regExedSeriesName = re.sub("\[[^]]*\]", "[]", seriesName)

            if regExedSeriesName.find(']') > -1:  # Ensure that the char exsists before we split the string
                regExedSeriesName = regExedSeriesName[regExedSeriesName.find(']') + 1:len(regExedSeriesName)]
            regExedSeriesName = regExedSeriesName.lstrip()

            if regExedSeriesName.rfind('-', 0, len(
                    regExedSeriesName)) > -1:  # Ensure that the char exsists before we split the string
                regExedSeriesName = regExedSeriesName[0:regExedSeriesName.rfind('-', 0, len(regExedSeriesName))]
            regExedSeriesName = regExedSeriesName.rstrip()  # Remove any trailing whitespace from the name.

            regExedSeriesName = regExedSeriesName.replace("_", " ")  # Replace all underscores with spaces.

            sanatizedSeriesName = regExedSeriesName.lower()  # make it all lowercase

            print "AniFile:" + item
            print "Found Series Name:" + regExedSeriesName + "."
            print "Sanatized Series Name:" + sanatizedSeriesName + "."

            # we need to do a few sanitations to improve matching abilities.



            possibleDirCanidates = []  # A list that will store all possible directory canidates.
            # possibleSourceDirCanidates = []
            # stripedPossibleDirCanidates = [] #A list of dir canidates with no whitespace.
            for dirItem in destDirList:
                tmpDirItem = dirItem.lower()  # Convert all chars to lowercase
                # print tmpDirItem
                if tmpDirItem.find(sanatizedSeriesName) > -1:
                    possibleDirCanidates.append(dirItem)  # add the dir to the possible list
                # print dirItem.find(seriesName)
                # print "Dir:" + dirItem + '.'

            # for dirItem in dirList:
            # 	tmpDirItem = dirItem.lower() #Convert all chars to lowercase
            # 	print tmpDirItem
            # 	if tmpDirItem.find(sanatizedSeriesName) > -1:
            # 		possibleSourceDirCanidates.append(dirItem) #add the dir to the possible list
            # 		# print dirItem.find(seriesName)
            # 		# print "Dir:" + dirItem + '.'

            matchedDir = "None"
            dirMatched = False
            # sourceDirMatched = False
            if ((len(
                    possibleDirCanidates) > 0)):  # or (len(possibleSourceDirCanidates) > 0)):#1: #We need to narrow down the posibilities to one. #We will implement narrow down later, for now, take first match.
                stripedSeriesName = sanatizedSeriesName.replace(" ", "")
                print "Striped Series Name:" + stripedSeriesName
                # if stripedSeriesName.rfind('-') > -1:
                # 	stripedSeriesName = stripedSeriesName[0:stripedSeriesName.rfind('-')]
                # 	print "stripedSeriesName:" + stripedSeriesName
                print "There are " + str(len(possibleDirCanidates)) + " Possible directories"
                # print "and " + str(len( possibleSourceDirCanidates)) + " Possible Source directories"
                for dirCan in possibleDirCanidates:  # NOTE: we currently do not escape if we find a match!!
                    stripedDirCan = dirCan.replace(" ", "")
                    stripedDirCan = stripedDirCan.lower()
                    print "SanatizedDirCan:" + stripedDirCan
                    if stripedDirCan.find("-[") > -1:
                        stripedDirCan = stripedDirCan[0:stripedDirCan.find("-[")]
                        print "stripedDirCan:" + stripedDirCan

                    if stripedDirCan == stripedSeriesName:
                        dirMatched = True
                        matchedDir = dirCan
                        print "MatchedDir:" + dirCan


                # for dirCan in possibleSourceDirCanidates: #NOTE: we currently do not escape if we find a match!!
                # 	stripedDirCan = dirCan.replace(" ","")
                # 	stripedDirCan = stripedDirCan.lower()
                # 	print "SanatizedSourceDirCan:" + stripedDirCan
                # 	if stripedDirCan.find("-[") > -1:
                # 		stripedDirCan = stripedDirCan[0:stripedDirCan.find("-[")]
                # 		print "stripedSourceDirCan:" + stripedDirCan

                # 	if stripedDirCan == stripedSeriesName:
                # 		sourceDirMatched = True
                # 		matchedDir = dirCan
                # 		print "MatchedSourceDir:" + dirCan

                # if sourceDirMatched == False:
                # 	sourceDirMatched = True
                # 	matchedDir = possibleSourceDirCanidates[0]
                # 	print "Forced matched Source is dir:" + matchedDir
                if dirMatched == False:
                    # we were not able to strictly match the directory. Lets try loosly matching.
                    # the initial canidate selection is a loose match. Lets just use the first result of that.
                    dirMatched = True
                    matchedDir = possibleDirCanidates[0]
                    print "Forced matched dir:" + matchedDir



            else:
                print "No Canidates were found!"

            if dirMatched == False:
                print "ALERT! We were unable to match a directory for " + seriesName + ". Creating new directory."
                createdDir = regExedSeriesName
                createdDir = createdDir.replace("_", " ")
                createdDir = createdDir + " - [autoDir]"
                print sourceScanDir + "\\" + item, animeDir + "\\" + createdDir + "\\" + item
                os.mkdir(animeDir + "\\" + createdDir)
                shutil.move(sourceScanDir + "\\" + item, animeDir + "\\" + createdDir + "\\" + item)
                destDirList.append(createdDir)  # We have created a directory, it needs to be added to the list

            else:
                print "Moving file into discovered directory"
                print sourceScanDir + "\\" + item, animeDir + "\\" + matchedDir + "\\" + item
                shutil.move(sourceScanDir + "\\" + item, animeDir + "\\" + matchedDir + "\\" + item)

            print " "  # Add a newline at the end of each series.
        # elif ((seriesName.lower().find(TheDailyShowID) > -1) and lftpDownloading == False):#This is a dailyshow vid.
        # 	print "Show matched as non animu series THE.DAILY.SHOW"
        # 	print "Moving it into THE.DAILY.SHOW folder!"
        # 	shutil.move(sourceScanDir + "\\" + item, TheDailyShowDir + "\\" + item)
        else:
            lowerSeriesName = seriesName.lower()
            for nonAnimeShow in nonAnimeShowID:
                if ((lowerSeriesName.find(nonAnimeShow) > -1) and lftpDownloading == False):
                    print "Show matched as non animu series " + nonAnimeShow
                    showDir = nonAnimeShowBaseDir + nonAnimeShow.replace(".", " ")
                    shutil.move(sourceScanDir + "\\" + item, showDir + "\\" + item)

            for specialCaseShow in specialCaseNonAnimeShowID:
                # print "Scaning for " + specialCaseShow
                if ((lowerSeriesName.find(specialCaseShow) > -1) and lftpDownloading == False):
                    print "Found a special case"
                    if specialCaseShow == specialCaseNonAnimeShowID[0]:  # Steven Universe
                        if (lowerSeriesName.find(
                                ".hdtv.") > -1):  # Only the HDTV releases are fucked up. The WebDL Releases are ok
                            print "Show matched as Steven Universe! Preforming Numbering Defuckup Routine."
                            showDir = specialCaseNonAnimeBaseDir + "Steven Universe - [Season Two] - [Unfinished]"

                            # This is a shity way of doing this but......... its late, and I am tired and I just dont give a fuck.

                            epNumIndex = lowerSeriesName.find(".s02e")
                            epNumIndex = epNumIndex + 5  # This is because find will give us the begining of the find string

                            epNumber = item[epNumIndex:(epNumIndex + 2)]  # Find the episode number
                            newEpNumber = int(epNumber) + 3  # Defuck up the number

                            if newEpNumber < 10:  # ensure that eps lower than 10 are 0 padded
                                newEpNumber = "0" + str(newEpNumber)
                            else:
                                newEpNumber = str(newEpNumber)

                            defuckedupName = lowerSeriesName.replace("s02e" + epNumber, "s02e" + newEpNumber)

                            shutil.move(sourceScanDir + "\\" + item, showDir + "\\" + defuckedupName)
                        else:
                            showDir = specialCaseNonAnimeBaseDir + "Steven Universe - [Season Two] - [Unfinished]"
                            shutil.move(sourceScanDir + "\\" + item, showDir + "\\" + seriesName)


    # ---End of baseDir Scan





    print "Going to sleep"
    time.sleep(sleepTime)
    print "Waking Up"
    print " "










