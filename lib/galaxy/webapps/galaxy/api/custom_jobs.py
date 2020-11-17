""" API for asynchronous job running mechanisms can use to fetch or put files
related to running and queued jobs.
"""
import logging
import os
import shutil

from galaxy import (
  exceptions,
  model,
  util
)

from galaxy.webapps.base.controller import BaseAPIController
from galaxy.exceptions import ActionInputError
from galaxy.web import expose_api,expose_api_anonymous_v2
import subprocess
import psycopg2
import time

log = logging.getLogger(__name__)


class CustomJobsAPIController(BaseAPIController):
  """ This job files controller allows remote job running mechanisms to
  read and modify the current state of files for queued and running jobs.
  """

  def __init__(self, app):
    super(CustomJobsAPIController, self).__init__(app)
    self.initialize()

  def initialize(self):
    #self.host = '192.168.0.184'
    self.host = '47.106.136.96'
    self.port = 5432
    self.user = 'postgres'
    self.password = '123456'
    self.db = 'postgres'

  def add_job(self, **kwargs):
    now = int(time.time())
    conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)
    cur = conn.cursor()
    fields = "tool_id,tool_name,tool_version,galaxy_version,cwd,params,session_id,user_id,status,output,real_output,create_time,update_time"
    values = "'%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s','%s',%d,%d" % (kwargs['tool_id'],kwargs['tool_name'],kwargs['tool_version'],
    kwargs['galaxy_version'],kwargs['cwd'],kwargs['params'],kwargs['session_id'],kwargs['user_id'],kwargs['status'],kwargs['output'],
    kwargs['real_output'],now,now)
    sql = "insert into custom_jobs(%s) values(%s) returning id" % (fields, values)
    log.info("sql = %s", sql)
    cur.execute(sql)
    job_id = cur.fetchone()[0]
    log.info("sql = %s, job_id = %d", sql, job_id)
    conn.commit()
    conn.close()
    return job_id
  
  def list_job(self, user_id, galaxy_session, page=1, size=10):
    conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    total = 0
    cond = ""
    if user_id != "":
      cond = " user_id = '%s'"  % (user_id)
    else:
      cond = " session_id = '%s'" % (galaxy_session)
    sql = "select count(*) as total from custom_jobs where " + cond
    cur.execute(sql)
    row = cur.fetchone()
    total = row["total"]

    limit = " limit %d offset %d" % (size, (page-1)*size)
    sql = "select * from custom_jobs where " + cond + limit
    log.info("sql = %s", sql)
    cur.execute(sql)
    jobs = cur.fetchall()
    for job in jobs:
      log.info("job = %s", job)
    conn.close()
    return (total, [job for job in jobs])

  def get_job(self, job_id):
    conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select * from custom_jobs where id = " + str(job_id)
    log.info("sql = %s", sql)
    cur.execute(sql)
    job = cur.fetchone()
    conn.close()
    return job

  def make_sure_root(self, trans):
    file_path = trans.app.config.ftp_upload_dir
    if trans.user:
      root_dir = file_path + "/" + trans.user.email 
    else:
      root_dir = file_path + "/tmp/session-" + str(trans.galaxy_session.id)
    if not os.path.exists(root_dir):
      log.info("create root_dir = %s", trans.user.email)
      os.makedirs(root_dir)
    log.info("root_dir = %s", root_dir)
    return root_dir

  @expose_api_anonymous_v2
  def on_run_job(self, trans, payload, **kwargs):
    """
    * POST /api/custom/job
    """
    missing_arguments = []
    tool_id = payload.get("tool_id", None)
    if not tool_id:
      missing_arguments.append("tool_id")

    if len(missing_arguments) > 0:
      raise ActionInputError("The following required arguments are missing in the payload: {}".format(missing_arguments))

    if tool_id == "__args_index__":
      return self.__on_args(trans, payload, **kwargs)
    if tool_id == "__sargfam__":
      return self.__on_sargfam(trans, payload, **kwargs)
  
    #elif 
    return {"message": "ok"}

  def __on_args(self, trans, payload, **kwargs):
    missing_arguments = []
    tool_id = payload.get("tool_id", None)
    if not tool_id:
      missing_arguments.append("tool_id")

    tool_version = payload.get("tool_version", None)
    if not tool_version:
      missing_arguments.append("tool_version")
    
    input_dir = payload.get("input", None)
    if not input_dir:
      missing_arguments.append("input")

    suffix = payload.get("suffix", ".orf")
    if not suffix:
      missing_arguments.append("suffix")

    if len(missing_arguments) > 0:
      raise ActionInputError("The following required arguments are missing in the payload: {}".format(missing_arguments))

    root_dir = self.make_sure_root(trans)
    real_path = root_dir + input_dir
    log.info("real_path = %s", real_path)
    if not os.path.isdir(real_path):
      raise ActionInputError("input not exist")

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/args"

    user_id = 0
    if trans.user:
      user_id = trans.user.id
    
    params = {
      "tool_id": tool_id,
      "tool_name": "args",
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.version_major,
      "cwd": job_cwd,
      "params": "-i %s -f %s" % (input_dir, suffix),
      "session_id": trans.galaxy_session.id,
      "user_id": user_id,
      "status": 1,
      "output": input_dir + "/output/final.out",
      "real_output": real_path + "/output/final.out"
    }
    if input_dir == "/":
      params["output"] = "/output/final.out"
      params["real_output"] = root_dir + "/output/final.out"
    job_id = self.add_job(**params)
    commandstr = "python job_agent.py %d args.py %s -i %s -f %s" % (
      job_id, job_cwd, real_path, suffix)
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)

    return {"message": "ok", "job_id": job_id}

  def __on_sargfam(self, trans, payload, **kwargs):
    missing_arguments = []
    tool_id = payload.get("tool_id", None)
    if not tool_id:
      missing_arguments.append("tool_id")

    tool_version = payload.get("tool_version", None)
    if not tool_version:
      missing_arguments.append("tool_version")
    
    input1 = payload.get("input1", None)
    if not input1:
      missing_arguments.append("input1")

    if len(missing_arguments) > 0:
      raise ActionInputError("The following required arguments are missing in the payload: {}".format(missing_arguments))

    input_dir = os.path.dirname(input1)
    log.info("input1 = %s, input_dir = %s", input1, input_dir)
    root_dir = self.make_sure_root(trans)
    real_path = root_dir + input1
    log.info("real_path = %s", real_path)
    if not os.path.isfile(real_path):
      raise ActionInputError("input not exist")

    inputdir = os.path.dirname(real_path)
    output_path = inputdir + "/output/final.txt"

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/sargfam"

    user_id = 0
    if trans.user:
      user_id = trans.user.id
    
    params = {
      "tool_id": tool_id,
      "tool_name": "sargfam",
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.version_major,
      "cwd": job_cwd,
      "params": "-i %s" % (input1),
      "session_id": trans.galaxy_session.id,
      "user_id": user_id,
      "status": 1,
      "output": input_dir + "/output/final.txt",
      "real_output": inputdir + "/output/final.txt"
    }
    job_id = self.add_job(**params)
    commandstr = "python job_agent.py %d sargfam.py %s -i %s -o %s" % (
      job_id, job_cwd, real_path, output_path)
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)

    return {"message": "ok", "job_id": job_id}

  @expose_api_anonymous_v2
  def on_job_detail(self, trans, id, **kwargs):
    """
    * GET /api/custom/job/detail/{job_id}
    """
    log.info("job_id = %s", id)
    job = self.get_job(id)
    data = {
      "job_id": job["id"],
      "tool_id": job["tool_id"],
      "tool_version": job["tool_version"],
      "tool_name": job["tool_name"]+"-"+str(job["id"]),
      "status": job["status"],
      "params": job["params"],
      "output": job["output"],
      "create_time": job["create_time"],
      "update_time": job["update_time"]
    }
    return data

  @expose_api_anonymous_v2
  def on_job_list(self, trans, **kwargs):
    """
    * GET /api/custom/job/list
    """
    try:
      page = int(kwargs.get("page_no", 1))
      size = int(kwargs.get("page_size", 10))
    except:
      page = 1
      size = 10

    session_id = trans.galaxy_session.id
    if trans.user:
      user_id =  trans.user.id
      if user_id == "Anonymous":
        user_id = ""
    else:
      user_id = ""
    
    items = []
    total, jobs = self.list_job(user_id, session_id, page, size)
    for job in jobs:
      item = {
        "job_id": job["id"],
        "tool_id": job["tool_id"],
        "tool_version": job["tool_version"],
        "tool_name": job["tool_name"]+"-"+str(job["id"]),
        "status": job["status"],
        "params": job["params"],
        "output": job["output"],
        "create_time": job["create_time"],
        "update_time": job["update_time"]
      }
      items.append(item)

    data = {}
    data["total"] = total
    data["items"] = items
    return data