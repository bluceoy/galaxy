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
from galaxy.web import expose_api
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

  def initialize(self):
    self.host = '192.168.0.184'
    self.port = 5432
    self.user = 'postgres'
    self.password = '123456'
    self.db = 'postgres'

  def add_job(self, **kwargs):
    now = int(time.time())
    conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)
    cur = conn.cursor()
    fields = "tool_id,tool_name,tool_version,galaxy_version,cwd,params,session_id,user_id,status,output,real_output,create_time,update_time"
    values = "'%s','%s','%s','%s','%s','%s','%s',%d,%d,'%s',%d,%d" % (kwargs['tool_id'],kwargs['tool_name'],kwargs['tool_version'],
    kwargs['galaxy_version'],kwargs['cwd'],kwargs['params'],kwargs['session_id'],kwargs['user_id'],kwargs['status'],kwargs['output'],
    kwargs['real_output'],now,now)
    sql = "insert into custom_jobs(%s) values(%s) returning id" % (fields, values)
    log.info("sql = %s", sql)
    cur.execute(sql)
    job_id, _ = cur.fetchone()
    log.info("sql = %s, job_id = %d", sql, job_id)
    cur.commit()
    conn.close()
    return job_id

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

  @expose_api
  def on_run_job(self, trans, payload, **kwargs):
    """
    * POST /api/custom/job
    :type  trans: galaxy.web.framework.webapp.GalaxyWebTransaction
    :param trans: Galaxy web transaction
    :param kwargs:

    :rtype:  dictionary
    :return: a dictionary containing a `summary` view of the datasets copied from the given cloud-based storage.
    """
    missing_arguments = []
    tool_id = payload.get("tool_id", None)
    if not tool_id:
      missing_arguments.append("tool_id")

    if len(missing_arguments) > 0:
      raise ActionInputError("The following required arguments are missing in the payload: {}".format(missing_arguments))

    if tool_id == "__args_index__":
      return self.__on_args(trans, payload, **kwargs)
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
    #real_path = os.path.join(root_dir, input_dir)
    real_path = root_dir + input_dir
    log.info("real_path = %s", real_path)
    if not os.path.isdir(real_path):
      raise ActionInputError("input not exist")

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/args"
    
    #values = "'%s','%s','%s','%s','%s','%s','%s',%d,%d,'%s',%d,%d" % (kwargs['tool_id'],kwargs['tool_name'],kwargs['tool_version'],
    #kwargs['galaxy_version'],kwargs['cwd'],kwargs['params'],kwargs['session_id'],kwargs['user_id'],kwargs['status'],kwargs['output'],
    #kwargs['create_time'],kwargs['update_time'])
    params = {
      "tool_id": tool_id,
      "tool_name": tool_id,
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.galaxy_version,
      "cwd": job_cwd,
      "params": "-i %s -f %s" % (input_dir, suffix),
      "session_id": trans.galaxy_session.id,
      "user_id": trans.user.id,
      "status": 1,
      "output": input_dir + "/output",
      "real_output": real_path + "/output"
    }
    job_id = self.add_job(**params)


    commandstr = "python job_agent.py %d args.py %s -i %s -f %s" % (
      job_id, job_cwd, real_path, suffix)
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)

    return {"message": "ok", "job_id": job_id}

  @expose_api
  def on_job_detail(self, trans, id, **kwargs):
    """
    * GET /api/custom/job/detail/{job_id}
        Populate an output file (formal dataset, task split part, working
        directory file (such as those related to metadata)). This should be
        a multipart post with a 'file' parameter containing the contents of
        the actual file to create.

    :type   payload:    dict
    :param  payload:    dictionary structure containing::
        'job_key'   = Key authenticating
        'path'      = Path to file to create.

    ..note:
        This API method is intended only for consumption by job runners,
        not end users.

    :rtype:     dict
    :returns:   an okay message
    """
    missing_arguments = []
    job = {
      "job_id": 1,
      "job_name": "args-1",
      "status": 1,
      "params": "",
      "output": "",
      "create_time": 1603346662,
      "update_time": 1603346662
    }
    return job

  @expose_api
  def on_job_list(self, trans, **kwargs):
    """
    * GET /api/custom/job/list
        Populate an output file (formal dataset, task split part, working
        directory file (such as those related to metadata)). This should be
        a multipart post with a 'file' parameter containing the contents of
        the actual file to create.

    :type   payload:    dict
    :param  payload:    dictionary structure containing::
        'job_key'   = Key authenticating
        'path'      = Path to file to create.

    ..note:
        This API method is intended only for consumption by job runners,
        not end users.

    :rtype:     dict
    :returns:   an okay message
    """
    missing_arguments = []

    data = {}
    data["total"] = 0
    data["items"] = []
    return data