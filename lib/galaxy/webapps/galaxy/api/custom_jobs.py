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
    
    job_id = 1
    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/args"
    commandstr = "python job_agent.py %d args.py %s -i %s -f %s" % (
      job_id, job_cwd, real_path, suffix)
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)


    # conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)
    # cur = conn.cursor()
    # cur.execute("")

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
      "job_id":1,
      "job_name": "args-1",
      "status":1,
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