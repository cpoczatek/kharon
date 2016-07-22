


http://www.paramiko.org/installing.html
http://docs.paramiko.org/en/2.0/api/sftp.html#paramiko.sftp_attr.SFTPAttributes

https://gist.github.com/ghawkgu/944017

http://stackoverflow.com/questions/14819681/upload-files-using-sftp-in-python-but-create-directories-if-path-doesnt-exist

---
Python on windows:
http://stackoverflow.com/questions/4621255/how-do-i-run-a-python-program-in-the-command-prompt-in-windows-7

Omitting the .py extension (editing PATHEXT):

>To further reduce typing, you can tell Windows that .py (and perhaps .pyc files) are executable. To do this, right-click Computer and choose Properties, Advanced, Environment Variables, System Variables. Append ";.PY;.PYC" (without quotes) to the existing PATHEXT variable, or else create it if you're certan it doesn't exist yet. Close and reopen the command prompt. You should now be able to omit the .py (FYI, doing so would cause ApplyRE.exe or ApplyRE.bat to run instead, if one existed).
```
D:\my scripts>ApplyRE lexicon-sample.txt -o
Running... Done.
```

Adding scripts to the system PATH:

>If you're going to use your scripts often from the command prompt (it's less important if doing so via using BAT files), then you'll want to add your scripts' folder to the system PATH. (Next to PATHEXT you should see a PATH variable; append ";D:\my scripts" to it, without quotes.) This way you can run a script from some other location against the files in current location, like this:
```
C:\some files>ApplyRE "some lexicon.txt" "some lexicon OUT.txt" -o
Running... Done.
```

---
Dropbox?
https://github.com/andreafabrizi/Dropbox-Uploader
https://github.com/hartez/PneumaticTube
http://www.codewise-llc.com/blog/2014/7/30/upload-to-dropbox-from-the-command-line-in-windows
