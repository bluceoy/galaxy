import logging
import psycopg2
import subprocess
import os
import sys
import shutil
import subprocess

log = logging.getLogger(__name__)


class JobAgent(object):
  def __init__(self, job_id, tool_id, cwd):
    self.host = '192.168.0.184'
    self.port = 5432
    self.user = 'postgres'
    self.password = '123456'
    self.db = 'postgres'
    self.job_id = job_id
    self.tool_id = tool_id
    self.cwd = cwd
    
  def run(self, *args):
    commands = ["python", self.tool_id]
    if len(args) > 0:
      commands.append(*args)
    log.info("commands = %s", commands)
    process = subprocess.run(commands, cwd=self.cwd, check=True)
    log.info("returncode = %d", process.returncode)

if __name__ == "__main__":
  job_id = sys.argv[1]
  tool_id = sys.argv[2]
  cwd = sys.argv[3]
  args = sys.argv[4:]
  job = JobAgent(job_id, tool_id, cwd)
  if len(sys.argv) > 4:
    job.run(*sys.argv[4:])
  else:
    job.run()
