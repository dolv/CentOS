#!/usr/bin/python
import sys
import os
import time
import datetime
import logging
import syslog
import xml.etree.ElementTree as ET
#print "Processing file " + sys.argv[1]
# ----- Global variables declaration ---------------------------
LOG_FILE = "log"
SCRIPT = os.path.basename(sys.argv[0])
SCRIPT_FOLDER = os.path.dirname(sys.argv[0])
LOG_FILE = SCRIPT_FOLDER+"/"+LOG_FILE

RUN_HELP = "Run command like this: \r\n"+SCRIPT+" /path_to_job_folder/config.xml \
BitMask \r\n" + """
BitMask is a sum of the following values.
  1 = startNotification
  2 = notifySuccess
  4 = notifyAborted
  8 = notifyNotBuilt
 16 = notifyUnstable
 32 = notifyFailure
 64 = notifyBackToNormal
128 = notifyRepeatedFailure
"""
notifications = {
    'startNotification': 1,
    'notifySuccess': 2,
    'notifyAborted': 4,
    'notifyNotBuilt': 8,
    'notifyUnstable': 16,
    'notifyFailure': 32,
    'notifyBackToNormal': 64,
    'notifyRepeatedFailure': 128
}
# ----- Global variables declaration ---------------------------
def logFileExists(file):
    # Check if file exists if not creates it otherwise truncates.
    if (not os.path.isfile(file)):
        try:
            open(file, 'a').close()
        except IOError as ioe:
            print_log("I/O error({0}): {1}".format(ioe.errno, ioe.strerror))
            return False
    else:
        open(file, 'w').close()
        return True

def print_log(message):
    if os.path.isfile(LOG_FILE) and os.access(LOG_FILE, os.R_OK):
        log_file = open(LOG_FILE, "a+")
        for line in message.split(os.linesep):
            log_file.write(datetime.datetime.now().strftime("%x %H:%M:%S.%f") + " [" +
                           SCRIPT + "] " + line + "\n")
        log_file.close
    else:
        syslog.syslog("[" + SCRIPT + "]" + message)
        print message

def testBit(int_type, offset):
#    mask = 1 << offset
#    return(int_type & mask)
    return(int_type & offset)

# ---- Initial verifications  ---------------------------------
# Check if there were commandline arguments provided
#print len(sys.argv)
if (len(sys.argv) != 3):
    print_log(os.linesep + "Please provide command line agruments. There should be 2." + \
              os.linesep + "You provided " + str(len(sys.argv)) + \
              os.linesep + RUN_HELP + os.linesep +
              "Aborting." + os.linesep)
    sys.exit(1)
# Check if provided xml file exists.
if not os.path.isfile(sys.argv[1]):
    print_log(os.linesep + "Provided filename " + sys.argv[1] + \
              "does not exists." + os.linesep + \
              "Aborting." + os.linesep)
    sys.exit(2)
# -------------MAIN BODY -----------------------

#logFileExists(LOG_FILE)
#print "{0:30} ".format(testBit(8, 8))
print_log("Processing the file " + os.path.abspath(sys.argv[1]))
tree = ET.parse(sys.argv[1])
root = tree.getroot()
for notification, offset in notifications.iteritems():
    for xmlNotification in root.iter(notification):
#        print "{0:30}  {1:>3}, {2}".format(notification, offset, testBit(int(sys.argv[2]), offset))
	    if (testBit(int(sys.argv[2]), offset)>0):
		xmlNotification.text = "true"
		print_log("   Setting tag <" + notification + ">true</" + notification + ">")
            else:
                xmlNotification.text = "false"
                print_log("   Setting tag <" + notification + ">false</" + notification + ">")
tree.write(sys.argv[1])
