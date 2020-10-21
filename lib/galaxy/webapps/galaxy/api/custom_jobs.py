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
from galaxy.web import (
  expose_api_anonymous_and_sessionless,
  expose_api_raw_anonymous_and_sessionless,
)
from galaxy.webapps.base.controller import BaseAPIController
from galaxy.exceptions import ActionInputError
import psycopg2
import subprocess

log = logging.getLogger(__name__)


class CustomJobsAPIController(BaseAPIController):
  """ This job files controller allows remote job running mechanisms to
  read and modify the current state of files for queued and running jobs.
  It is certainly not meant to represent part of Galaxy's stable, user
  facing API.

  Furthermore, even if a user key corresponds to the user running the job,
  it should not be accepted for authorization - this API allows access to
  low-level unfiltered files and such authorization would break Galaxy's
  security model for tool execution.
  """

  def initialize(self):
    self.host = '192.168.0.184'
    self.port = 5432
    self.user = 'postgres'
    self.password = '123456'
    self.db = 'postgres'
    self.cwd = '/home/oyq/galaxy/tools/custom'

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

  @expose_api_anonymous_and_sessionless
  def on_run_job(self, trans, payload, **kwargs):
    """
    create( self, trans, payload, **kwargs )
    * POST /api/custom/job
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
    
    input_dir = payload.get("input_dir", None)
    if not input_dir:
      missing_arguments.append("input_dir")

    if len(missing_arguments) > 0:
      raise ActionInputError("The following required arguments are missing in the payload: {}".format(missing_arguments))

    root_dir = self.make_sure_root(trans)
    real_path = os.path.join(root_dir, input_dir)
    if not os.path.isdir(real_path):
      raise ActionInputError("input not exist")

    commandstr = "python %s/args/main.py -i %s -f .orf" % (trans.app.config.tool_path, real_path)
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=self.cwd)


    # conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)
    # cur = conn.cursor()
    # cur.execute("")

    job_id = 1
    return {"message": "ok", "job_id": job_id}

  @expose_api_anonymous_and_sessionless
  def on_get_job(self, trans, id, **kwargs):
    """
    create( self, trans, payload, **kwargs )
    * GET /api/custom/job/{job_id}
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
    return {"message":"ok"}