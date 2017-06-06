#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import threading
import datetime
import time
import os
import signal


class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def run(self, timeout=300):
        def kill(p):
            if not p.poll():
                print 'Timeout! Terminate process!'
                p.terminate()

        process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        timer = threading.Timer(timeout, kill, [process])

        try:
            timer.start()
            stdout, stderr = process.communicate()
            return stdout, stderr
        except Exception, err:
            print 'Exception: %s' % err
        finally:
            timer.cancel()


def runCmd(cmd, isReturnValue=False, timeout=0):
    if isReturnValue:
        start = datetime.datetime.now()
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if timeout != 0:
            while p.poll() is None:
                now = datetime.datetime.now()
                if (now - start).seconds > timeout:
                    os.kill(p.pid, signal.SIGKILL)
                    os.waitpid(-1, os.WNOHANG)
                    return [None, None]
                time.sleep(1)
        stdout, stderr = p.communicate()
        return [stdout, stderr]
    else:
        start = datetime.datetime.now()
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if timeout != 0:
            while p.poll() is None:
                now = datetime.datetime.now()
                if (now - start).seconds > timeout:
                    os.kill(p.pid, signal.SIGKILL)
                    os.waitpid(-1, os.WNOHANG)
                time.sleep(1)
        else:
            p.wait()
        return p.returncode



def main():
    """
    main process
    """


if __name__ == '__main__':
    main()
