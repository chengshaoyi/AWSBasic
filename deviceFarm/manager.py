import ConfigParser
import sys
import os.path

# the configuration file contains
# project
# device-pool
# apk
# except apk, all the others can be set to "ADD" which makes
def parseDFRunConfiguration(confFile):
    config = ConfigParser.ConfigParser()
    config.read(confFile)




if __name__ == '__main__':
    assert(len(sys.argv) >= 2), "Please supply the configuration file for device farm run"
    assert(os.path.isfile(sys.argv[1])), "Configuration file does not exist"
    parseDFRunConfiguration(sys.argv[1])
