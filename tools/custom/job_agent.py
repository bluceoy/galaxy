import logging
import psycopg2
import subprocess
import os
import sys
import shutil
import subprocess
import time

log = logging.getLogger(__name__)


class JobAgent(object):
  def __init__(self, job_id, tool_id, cwd):
    self.host = '192.168.0.184'
    self.host = '47.106.136.96'
    self.port = 5432
    self.user = 'postgres'
    self.password = '123456'
    self.db = 'postgres'
    self.job_id = job_id
    self.tool_id = tool_id
    self.cwd = cwd

  def update_job_status(self, status):
    now = int(time.time())
    conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)
    cur = conn.cursor()
    sql = "update custom_jobs set status = %d, update_time = %d where id = %d" % (
      status, now, self.job_id)
    log.info("sql = %s", sql)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return 
    
  def run(self, *args):
    commands = ["python", self.tool_id]
    for arg in args:
      commands.append(arg)
    log.info("commands = %s", commands)
    process = subprocess.run(commands, cwd=self.cwd, check=True)
    log.info("returncode = %d", process.returncode)
    if process.returncode == 0:
      self.update_job_status(2)
    else:
      self.update_job_status(3)

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
