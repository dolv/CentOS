#!/usr/bin/python
import sys
import os
import time
import datetime
import logging
#import syslog
import argparse
import xml.etree.ElementTree as ET
from argparse import RawTextHelpFormatter

# ----- Global variables declaration ---------------------------
LOG_FILE = "log"
SCRIPT = os.path.basename(sys.argv[0])
SCRIPT_FOLDER = os.path.dirname(sys.argv[0])
LOG_FILE = SCRIPT_FOLDER+"/"+LOG_FILE
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
RUN_HELP = "BitMask is a integer number which equals to sum of the following values:" + os.linesep
for i in range(0, 8):
    mask = 1 << i
    for notification in notifications:
        if (notifications[notification] & mask):
            RUN_HELP += "{0:>4} = {1}".format(notifications[notification], notification)
            RUN_HELP += os.linesep


parser = argparse.ArgumentParser(description='This script sets bits for Slak notification plugin configuration of \
jenkins job config.xml file', formatter_class=RawTextHelpFormatter)
parser.add_argument('-f','--configfile',type=str, default="config.xml", help='path to your jenkins job config.xml file.')
parser.add_argument('BitMask',type=int, help=RUN_HELP)
parser.add_argument('-l','--log',help="Create a log file. Default filename is log in the script directory.",action="store_true")
parser.add_argument('-lf', type=str, help="Log file location")
parser.add_argument('-H','--jenkins_home', default="/var/lib/jenkins", type=str, help="jenkins home folder.")
parser.add_argument('-j','--job', type=str, help="jenkins job name. Is used in conjunction to --jenkins_home." + os.linesep + \
"If -j specified but -lf ommited the script will operate on the config.xml file of the specified job.")
args = parser.parse_args()
print args
# ----- Helper functions definition ---------------------------
def logFileExists():
    global LOG_FILE
    # Checks if logfile exists if not creates it.
    if (args.lf is not None):
        LOG_FILE = args.lf
        if (not os.path.isfile(LOG_FILE)):
            try:
                open(LOG_FILE, 'a').close()

            except IOError as ioe:
                print_log("I/O error({0}): {1}".format(ioe.errno, ioe.strerror))
                return False
        else:
            open(LOG_FILE, 'a').close()
            return True
    elif (args.log):
        try:
            open(LOG_FILE, 'a').close()
        except IOError as ioe:
            print_log("I/O error({0}): {1}".format(ioe.errno, ioe.strerror))
            return False

def print_log(message):
    if os.path.isfile(LOG_FILE) and os.access(LOG_FILE, os.R_OK):
        log_file = open(LOG_FILE, "a+")
        for line in message.split(os.linesep):
            log_file.write(datetime.datetime.now().strftime("%x %H:%M:%S.%f") + " [" +
                           SCRIPT + "] " + line + "\n")
        log_file.close
    else:
#        syslog.syslog("[" + SCRIPT + "]" + message)
        print message

def testBit(int_type, offset):
    return(int_type & offset)

# ---- Initial verifications  ---------------------------------
# Check if provided xml file exists.
if not os.path.isfile(args.configfile):
    print_log(os.linesep + "Provided filename [" + args.configfile + \
              "] does not exists." + os.linesep + \
              "Aborting." + os.linesep)
    sys.exit(2)
# -------------MAIN BODY -----------------------
logFileExists()
#print "{0:30} ".format(testBit(8, 8))
if (args.job is not None):
    args.configfile = os.path.abspath(args.jenkins_home + os.sep + args.configfile)
print_log("Processing the file " + os.path.abspath(args.configfile))
tree = ET.parse(args.configfile)
root = tree.getroot()
for notification, offset in notifications.iteritems():
    for xmlNotification in root.findall(str(".//"+notification)): # it works in 2.6 but is relatively slower
        #        print "{0:30}  {1:>3}, {2}".format(notification, offset, testBit(int(sys.argv[2]), offset))
        if (testBit(int(args.BitMask), offset)>0):
            xmlNotification.text = "true"
            print_log("   Setting tag <" + notification + ">true</" + notification + ">")
        else:
            xmlNotification.text = "false"
            print_log("   Setting tag <" + notification + ">false</" + notification + ">")
tree.write(args.configfile)
