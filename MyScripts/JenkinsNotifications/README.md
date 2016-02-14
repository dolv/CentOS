usage: set_notification_2_6_.py [-h] [-f CONFIGFILE] [-l] [-lf LF]
                                [-H JENKINS_HOME] [-j JOB]
                                BitMask

This script sets bits for Slak notification plugin configuration of jenkins job config.xml file

positional arguments:
  BitMask               BitMask is a integer number which equals to sum of the following values:
                           1 = startNotification
                           2 = notifySuccess
                           4 = notifyAborted
                           8 = notifyNotBuilt
                          16 = notifyUnstable
                          32 = notifyFailure
                          64 = notifyBackToNormal
                         128 = notifyRepeatedFailure

optional arguments:
  -h, --help            show this help message and exit
  -f CONFIGFILE, --configfile CONFIGFILE
                        path to your jenkins job config.xml file.
  -l, --log             Create a log file. Default filename is log in the script directory.
  -lf LF                Log file location
  -H JENKINS_HOME, --jenkins_home JENKINS_HOME
                        jenkins home folder.
  -j JOB, --job JOB     jenkins job name. Is used in conjunction to --jenkins_home.
                        If -j specified but -lf ommited the script will operate on the config.xml 
                        file of the specified job.
