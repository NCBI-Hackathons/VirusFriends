#  process.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import io
import sys
import time
import subprocess

class Process:

  def __init__(self, command):
    self.cmd = [command]
    self.ph = None

  def set_arguments(self, args):
    for i in args:
      if len(i) > 1:
        self.cmd += [str(i[0]), str(i[1])]
      else:
        self.cmd += [str(i[0])]

  def run(self, stdin=None):
    print(self.cmd)
    self.ph = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1, universal_newlines=True)
    if stdin != None:
      self.use_stdin(stdin)
    return self.ph

  def use_stdin(self, data):
    self.ph.stdin.write(data)
    self.ph.stdin.close()

  """
    Code graveyard and ToDo reminder.
    The methods below do not work when using stdout. The process cannot finish
    since  writing to stdout has to occur at the same time
    as reading the stdout by another process. The montioring routines need to
    done  by an indenpenden process than the screen, maybey threading?
  """
  def monitor(self, proc):
    while proc.ph.poll() is None:
      print("\r{}...".format(proc.work), end='', file=sys.stderr)
      time.sleep(5)

    if not self.isSuccess(proc):
      return proc_handle
    self.debrief(proc_handle)

  def isSuccess(self, proc):
    if proc.ph.returncode != 0:
      self.debrief(proc)
      return False
    return True

  def debrief(self, proc):
    print("{} failed with following error:".format(proc.name))
    for i in proc.ph.stdout:
      print(i.decode())
    raise RuntimeError("{} failed. Aborting.".format(proc.name))
