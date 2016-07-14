
_Charon ferries your files across the river Styx._
-----

#What?
Data that is made up of physical measurements is often created on a machine:
- that's simple, underpowered, or has little storage, eg an old laptop or a RaspberryPi
- tied to an instrument physically
- non-upgradeable because of the requirements of it's primary software

These things can limit options available to automatically move data from the
machine of origin into a data processing pipeline.

_Charon_ monitors the directory (or tree) where data is generated and sftp's "new"
files to a remote host if and only if:
- that file doesn't exist at the remote location, _or any sub-directory_.
- that file is no longer growing (note: kludge)

_Charon_ only requires Python and the Paramiko package which are available on
Linux/OS X/Windows.

#Current Problems
_Charon_ should be considered sub-alpha quality. *_Use at your own risk!_*

#Improvements, planned and possible
- actually parse arguments
- store file hashes?
- other transport modes / endpoints? Eg S3 or dropbox?

#How?

_Charon_ is self-documenting:

```
cpoczatek@grepon:charon$ python charon.py --help
blah
blah
blah
```

#inFAQ

_Q:_ Why not just use rsync?
_A:_ Syncing the directory structure is undesirable when the software generating
the raw data restricts that directory structure. This happens quite often. We care
about the *data* not where it's saved.

_Q:_ Why not just use DropBox/Syncthing?
_A:_ Bi-directional sync is *not* the goal. Syncing changes back to the original
machine can useless to impossible.

_Q:_ You should have done XYZ!
_A_: Probably.
