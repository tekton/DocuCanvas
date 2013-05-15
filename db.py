#!/usr/bin/python
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Process some module or DB migration.')
parser.add_argument('-i', '--init', help='Adds the inital schemamigration', dest='init_val', action="store_true")
parser.add_argument('string', metavar='N', type=str,
                    help='The name of the module to migrate using the local settings')
args = parser.parse_args()

# set to --settings=project.whatever if not normal settings
base_settings = ""  # not a command line variable as that kind of defeats the purpose

print "Will run the following commands::"
if args.init_val:
    print "\tpython manage.py schemamigration {0} --init {1}".format(args.string, base_settings)
    migration = "--init"
else:
    print "\tpython manage.py schemamigration {0} --auto {1}".format(args.string, base_settings)
    migration = "--auto"
print "\tpython manage.py migrate {0} {1}".format(args.string, base_settings)
print "-----"
print "Schema Migration::"
subprocess.Popen(['python', 'manage.py', 'schemamigration', migration, args.string, base_settings]).wait()
print "Migrate::"
subprocess.Popen(['python', 'manage.py', 'migrate', args.string, base_settings]).wait()
