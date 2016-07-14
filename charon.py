#!/usr/bin/python

import fnmatch
import os
import sys
import hashlib
import time
import shutil
import paramiko

# todo:
# options
# test script
# hash?
# log and timestamps

# todo option parsing:
# --source (default ./)
# --destination (force user@host:/path/to/what style?)
# --sleep (general pause)
# --changetime (time to sleep to detect file modification, default 4min)
# --test
# --debug ?
# --hash ? compare file hashes?
# --version?

# Define testing defaults
# sshclient needs full path, canonicalize '~/'?
localpath = '/nrims/home3/cpoczatek/mycode/charon/test/source/'
remotepath = '/nrims/home3/cpoczatek/mycode/charon/test/dest/'
hostname = 'buenosaires'
username = 'mimsdata'
sleeptime = 10
changetime = 2

# arguments are dicts keyed on absolute paths,
# but the compare is by basename
def newfiles(new, old):
    newfiles = {}

    # abs paths keyed on basename
    newbase = {}
    oldbase = {}

    for key in new:
        newbase[os.path.basename(key)] = key
    for key in old:
        oldbase[os.path.basename(key)] = key
    for nkey in newbase:
        # stats keyed on abs path for new basenames
        if not nkey in oldbase:
            newfiles[newbase[nkey]] = newbase[nkey]
    return newfiles

# Walk source, make dict of stats keyed on abs path
def collectstats(source):
    files = {}
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
          abspath = os.path.join(root, filename)
          files[abspath] = os.stat(abspath)
    return files

def removechanging(files, new, wait):
    # sleep then check if modtime in different than when called
    time.sleep(wait)
    unmod = files.copy()
    for file in files:
        if not (file in new):
            unmod.pop(file)
        else:
            modtime = files[file].st_mtime
            currenttime = os.stat(file).st_mtime
            if (modtime != currenttime):
                unmod.pop(file, None)
    return unmod

from stat import S_ISDIR
def isdir(stat):
    return S_ISDIR(stat.st_mode)

class Rooted():
  def __init__(self, client):
    self.client = client
  # On entry store working dir
  def __enter__(self):
    self.rootpath = self.client.getcwd()
    return self.client
  # On exit go back to original working dir
  def __exit__(self, type, value, traceback):
    self.client.chdir(self.rootpath)


def collectremotestats(sftpclient):
  print "Collect remote file stats on: ", sftpclient.getcwd()
  files = {}

  for filename in sftpclient.listdir():
    stat = sftpclient.stat(filename)
    if isdir(stat):
      with Rooted(sftpclient):
        sftpclient.chdir(filename)
        files.update(collectstats(sftpclient))
    else:
      # Does getting the abs path this way make sense?
      # os.path module is local filesystem, sftp_client is remote...
      abspath = os.path.normpath(os.path.join(sftpclient.getcwd(), filename))
      files[abspath] = stat
  return files


def main():
    print "local path: ", localpath, "\tremote path: ", remotepath, \
          "\thost: ", hostname, "\tsleeptime: ", sleeptime, \
          "\tchangetime: ", changetime

    # ssh client
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "Connect ", username, "@", hostname, ":", remotepath
    ssh_client.connect(hostname=hostname, username=username, password="")
    print "\nOpen sftp connection... "
    sftp_client = ssh_client.open_sftp()
    sftp_client.chdir(remotepath)
    print "Open."
    try:
        while True:
            localfiles = collectstats(localpath)
            remotefiles = collectremotestats(sftp_client)

            print "Source files:", len(localfiles), "Dest files:", len(remotefiles)

            new = newfiles(localfiles,remotefiles)
            print "New files:", sorted(new.keys())
            if len(new) == 0:
                continue
            # need to copy tree or something for dirs that don't exist in dest
            print "Check for file modifications... ", changetime, " sec"
            unmod = removechanging(localfiles, new, changetime).keys()
            print "New and unmod files: ", unmod
            for f in unmod:
                print f, " --> ", remotepath
                rpath = os.path.join(remotepath, os.path.basename(f))
                sftp_client.put(f,rpath)

            # sleep for some time
            print "sleeping ", sleeptime, " sec..."
            time.sleep(sleeptime)
    except Exception as error:
        print "Unexpected error:"
        print(type(error))
        print(error.args)
        print(error)
    finally:
        # close ftp file and client
        sftp_client.close()
        # close ssh client
        ssh_client.close()
        print "Fin."


if __name__ == "__main__":
    main()
