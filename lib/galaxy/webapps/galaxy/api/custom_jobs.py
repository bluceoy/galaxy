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
    if not "output2" in kwargs:
      kwargs["output2"] = ""
      kwargs["real_output2"] = ""
    if not "output3" in kwargs:
      kwargs["output3"] = ""
      kwargs["real_output3"] = ""
    if not "output4" in kwargs:
      kwargs["output4"] = ""
      kwargs["real_output4"] = ""
    if not "output5" in kwargs:
      kwargs["output5"] = ""
      kwargs["real_output5"] = ""
    now = int(time.time())
    conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)
    cur = conn.cursor()
    fields = "tool_id,tool_name,tool_version,galaxy_version,cwd,params,session_id,user_id,status,output,real_output,output2,real_output2,output3,real_output3,output4,real_output4,output5,real_output5,create_time,update_time"
    values = "'%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,%d" % (kwargs['tool_id'],kwargs['tool_name'],kwargs['tool_version'],
    kwargs['galaxy_version'],kwargs['cwd'],kwargs['params'],kwargs['session_id'],kwargs['user_id'],kwargs['status'],kwargs['output'],
    kwargs['real_output'],kwargs['output2'],kwargs['real_output2'],kwargs['output3'],kwargs['real_output3'],kwargs['output4'],kwargs['real_output4'],kwargs['output5'],kwargs['real_output5'],now,now)
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

  def make_sure_output_dir(self, tool_name, root, inputdir):
    now = str(int(time.time()*1000))
    outputdir = "/" + tool_name + "-" + now + "/output"
    if inputdir != "/":
      outputdir = inputdir + outputdir
    real_outputdir = root + outputdir
    if not os.path.exists(real_outputdir):
      os.makedirs(real_outputdir)
    log.info("outputdir = %s", outputdir)
    return outputdir

  def make_output_file(self, outputdir, num, ext=".txt"):
    output = outputdir + "/output-" + str(num) + ext
    return output

  def check_args(self, *args):
    for arg in args:
      if arg is None:
        raise ActionInputError("Required arguments are missing in the payload")

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
    if tool_id == "__mst__":
      return self.__on_mst(trans, payload, **kwargs)
    if tool_id == "__argpore__":
      return self.__on_argpore(trans, payload, **kwargs)
    if tool_id == "__argsoap__":
      return self.__on_argsoap(trans, payload, **kwargs)
    if tool_id == "__argsoap2.0__":
      return self.__on_argsoap2_0(trans, payload, **kwargs)
    if tool_id == "__argsoap2.2__":
      return self.__on_argsoap2_2(trans, payload, **kwargs)
  
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
    tool_name = "sargfam"
    tool_dir = "sargfam"
    script = "sargfam.py"
    tool_id = payload.get("tool_id", None)
    tool_version = payload.get("tool_version", None)
    input1 = payload.get("input1", None)


    self.check_args(tool_id, tool_version, input1)

    root_dir = self.make_sure_root(trans)

    real_path1 = root_dir + input1
    if not os.path.isfile(real_path1):
      raise ActionInputError("input1 not exist")

    input1_dir = os.path.dirname(input1)
    output_dir = self.make_sure_output_dir(tool_name, root_dir, input1_dir)
    output1 = self.make_output_file(output_dir, 1)

    abspath_output1 = root_dir + output1

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/" + tool_dir

    user_id = 0
    if trans.user:
      user_id = trans.user.id

    args = [input1, output1]
    xargs = [real_path1, abspath_output1]
    
    params = {
      "tool_id": tool_id,
      "tool_name": tool_name,
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.version_major,
      "cwd": job_cwd,
      "params": " ".join(args),
      "session_id": trans.galaxy_session.id,
      "user_id": user_id,
      "status": 1,
      "output": output1,
      "real_output": abspath_output1
    }

    job_id = self.add_job(**params)
    commandstr = "python job_agent.py %d %s %s %s" % (
      job_id, script, job_cwd, " ".join(xargs))
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)

    return {"message": "ok", "job_id": job_id}

  def __on_mst(self, trans, payload, **kwargs):
    tool_name = "args_oap_v1.0"
    tool_dir = "MST"
    script = "mst.py"
    tool_id = payload.get("tool_id", None)
    tool_version = payload.get("tool_version", None)
    input1 = payload.get("input1", None)
    input2 = payload.get("input2", None)
    input3 = payload.get("input3", None)
    input4 = payload.get("input4", None)


    self.check_args(tool_id, tool_version, 
      input1, input2, input3, input4)

    root_dir = self.make_sure_root(trans)

    real_path1 = root_dir + input1
    if not os.path.isfile(real_path1):
      raise ActionInputError("input1 not exist")


    input1_dir = os.path.dirname(input1)
    output_dir = self.make_sure_output_dir(tool_name, root_dir, input1_dir)
    output1 = self.make_output_file(output_dir, 1)
    output2 = self.make_output_file(output_dir, 2)
    output3 = self.make_output_file(output_dir, 3)
    output4 = self.make_output_file(output_dir, 4)

    abspath_output1 = root_dir + output1
    abspath_output2 = root_dir + output2
    abspath_output3 = root_dir + output3
    abspath_output4 = root_dir + output4

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/" + tool_dir

    user_id = 0
    if trans.user:
      user_id = trans.user.id

    args = [input1, input2, input3, input4, output1, output2]
    xargs = [real_path1, input2, input3, input4, abspath_output1, abspath_output2]
    
    params = {
      "tool_id": tool_id,
      "tool_name": tool_name,
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.version_major,
      "cwd": job_cwd,
      "params": " ".join(args),
      "session_id": trans.galaxy_session.id,
      "user_id": user_id,
      "status": 1,
      "output": output1,
      "real_output": abspath_output1,
      "output2": output2,
      "real_output2": abspath_output2
    }

    job_id = self.add_job(**params)
    commandstr = "python job_agent.py %d %s %s %s" % (
      job_id, script, job_cwd, " ".join(xargs))
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)

    return {"message": "ok", "job_id": job_id}

  def __on_argpore(self, trans, payload, **kwargs):
    tool_name = "argpore"
    tool_dir = "hostract"
    script = "oap.py"
    tool_id = payload.get("tool_id", None)
    tool_version = payload.get("tool_version", None)
    input1 = payload.get("input1", None)

    self.check_args(tool_id, tool_version, input1)

    root_dir = self.make_sure_root(trans)

    real_path1 = root_dir + input1
    if not os.path.isfile(real_path1):
      raise ActionInputError("input1 not exist")

    input1_dir = os.path.dirname(input1)
    output_dir = self.make_sure_output_dir(tool_name, root_dir, input1_dir)
    output1 = self.make_output_file(output_dir, 1)
    output2 = self.make_output_file(output_dir, 2)
    output3 = self.make_output_file(output_dir, 3)
    output4 = self.make_output_file(output_dir, 4)

    abspath_output1 = root_dir + output1
    abspath_output2 = root_dir + output2
    abspath_output3 = root_dir + output3
    abspath_output4 = root_dir + output4

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/hostract"

    user_id = 0
    if trans.user:
      user_id = trans.user.id

    args = [input1, output1, output2, output3, output4]
    xargs = [real_path1, abspath_output1, abspath_output2, abspath_output3, abspath_output4]
    
    params = {
      "tool_id": tool_id,
      "tool_name": tool_name,
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.version_major,
      "cwd": job_cwd,
      "params": " ".join(args),
      "session_id": trans.galaxy_session.id,
      "user_id": user_id,
      "status": 1,
      "output": output1,
      "real_output": abspath_output1,
      "output2": output2,
      "real_output2": abspath_output2,
      "output3": output3,
      "real_output3": abspath_output3,
      "output4": output4,
      "real_output4": abspath_output4
    }
    job_id = self.add_job(**params)
    commandstr = "python job_agent.py %d %s %s %s" % (
      job_id, script, job_cwd, " ".join(xargs))
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)

    return {"message": "ok", "job_id": job_id}

  def __on_argsoap(self, trans, payload, **kwargs):
    tool_name = "args_oap_v1.0"
    tool_dir = "args_oap"
    script = "oap.py"
    tool_id = payload.get("tool_id", None)
    tool_version = payload.get("tool_version", None)
    input1 = payload.get("input1", None)
    input2 = payload.get("input2", None)
    input3 = payload.get("input3", None)
    input4 = payload.get("input4", None)
    input5 = payload.get("input5", None)
    input6 = payload.get("input6", None)
    input7 = payload.get("input7", None)
    input8 = payload.get("input8", None)
    input9 = payload.get("input9", None)

    self.check_args(tool_id, tool_version, 
      input1, input2, input3, input4, input5, 
      input6, input7, input8, input9)

    root_dir = self.make_sure_root(trans)

    real_path1 = root_dir + input1
    if not os.path.isfile(real_path1):
      raise ActionInputError("input1 not exist")

    real_path2 = root_dir + input2
    if not os.path.isfile(real_path2):
      raise ActionInputError("input2 not exist")

    input1_dir = os.path.dirname(input1)
    output_dir = self.make_sure_output_dir(tool_name, root_dir, input1_dir)
    output1 = self.make_output_file(output_dir, 1)
    output2 = self.make_output_file(output_dir, 2)
    output3 = self.make_output_file(output_dir, 3)
    output4 = self.make_output_file(output_dir, 4)
    output5 = self.make_output_file(output_dir, 5)

    abspath_output1 = root_dir + output1
    abspath_output2 = root_dir + output2
    abspath_output3 = root_dir + output3
    abspath_output4 = root_dir + output4
    abspath_output5 = root_dir + output5

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/" + tool_dir

    user_id = 0
    if trans.user:
      user_id = trans.user.id

    args = [input1, input2, input3, input4, input5, input6, input7, input8, input9,
      output1, output2, output3, output4, output5]
    xargs = [real_path1, real_path2, input3, input4, input5, input6, input7, input8, input9,
      abspath_output1, abspath_output2, abspath_output3, abspath_output4, abspath_output5]
    
    params = {
      "tool_id": tool_id,
      "tool_name": tool_name,
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.version_major,
      "cwd": job_cwd,
      "params": " ".join(args),
      "session_id": trans.galaxy_session.id,
      "user_id": user_id,
      "status": 1,
      "output": output1,
      "real_output": abspath_output1,
      "output2": output2,
      "real_output2": abspath_output2,
      "output3": output3,
      "real_output3": abspath_output3,
      "output4": output4,
      "real_output4": abspath_output4,
      "output5": output5,
      "real_output5": abspath_output5
    }

    job_id = self.add_job(**params)
    commandstr = "python job_agent.py %d %s %s %s" % (
      job_id, script, job_cwd, " ".join(xargs))
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)

    return {"message": "ok", "job_id": job_id}

  def __on_argsoap2_0(self, trans, payload, **kwargs):
    tool_name = "args_oap_v2.0"
    tool_dir = "args_oap2.0"
    script = "oap.py"
    tool_id = payload.get("tool_id", None)
    tool_version = payload.get("tool_version", None)
    input1 = payload.get("input1", None)
    input2 = payload.get("input2", None)
    input3 = payload.get("input3", None)
    input4 = payload.get("input4", None)
    input5 = payload.get("input5", None)
    input6 = payload.get("input6", None)
    input7 = payload.get("input7", None)
    input8 = payload.get("input8", None)
    input9 = payload.get("input9", None)

    self.check_args(tool_id, tool_version, 
      input1, input2, input3, input4, input5, 
      input6, input7, input8, input9)

    root_dir = self.make_sure_root(trans)

    real_path1 = root_dir + input1
    if not os.path.isfile(real_path1):
      raise ActionInputError("input1 not exist")

    real_path2 = root_dir + input2
    if not os.path.isfile(real_path2):
      raise ActionInputError("input2 not exist")

    input1_dir = os.path.dirname(input1)
    output_dir = self.make_sure_output_dir(tool_name, root_dir, input1_dir)
    output1 = self.make_output_file(output_dir, 1)
    output2 = self.make_output_file(output_dir, 2)
    output3 = self.make_output_file(output_dir, 3)
    output4 = self.make_output_file(output_dir, 4)
    output5 = self.make_output_file(output_dir, 5)

    abspath_output1 = root_dir + output1
    abspath_output2 = root_dir + output2
    abspath_output3 = root_dir + output3
    abspath_output4 = root_dir + output4
    abspath_output5 = root_dir + output5

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/" + tool_dir

    user_id = 0
    if trans.user:
      user_id = trans.user.id

    args = [input1, input2, input3, input4, input5, input6, input7, input8, input9,
      output1, output2, output3, output4, output5]
    xargs = [real_path1, real_path2, input3, input4, input5, input6, input7, input8, input9,
      abspath_output1, abspath_output2, abspath_output3, abspath_output4, abspath_output5]
    
    params = {
      "tool_id": tool_id,
      "tool_name": tool_name,
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.version_major,
      "cwd": job_cwd,
      "params": " ".join(args),
      "session_id": trans.galaxy_session.id,
      "user_id": user_id,
      "status": 1,
      "output": output1,
      "real_output": abspath_output1,
      "output2": output2,
      "real_output2": abspath_output2,
      "output3": output3,
      "real_output3": abspath_output3,
      "output4": output4,
      "real_output4": abspath_output4,
      "output5": output5,
      "real_output5": abspath_output5
    }

    job_id = self.add_job(**params)
    commandstr = "python job_agent.py %d %s %s %s" % (
      job_id, script, job_cwd, " ".join(xargs))
    log.info("command = %s", commandstr)

    command = commandstr.split(" ")
    subprocess.Popen(command, cwd=agent_cwd)

    return {"message": "ok", "job_id": job_id}

  def __on_argsoap2_2(self, trans, payload, **kwargs):
    tool_name = "args_oap_v2.2"
    tool_dir = "args_oap2.2"
    script = "oap.py"
    tool_id = payload.get("tool_id", None)
    tool_version = payload.get("tool_version", None)
    input1 = payload.get("input1", None)
    input2 = payload.get("input2", None)
    input3 = payload.get("input3", None)
    input4 = payload.get("input4", None)
    input5 = payload.get("input5", None)
    input6 = payload.get("input6", None)
    input7 = payload.get("input7", None)
    input8 = payload.get("input8", None)
    input9 = payload.get("input9", None)

    self.check_args(tool_id, tool_version, 
      input1, input2, input3, input4, input5, 
      input6, input7, input8, input9)

    root_dir = self.make_sure_root(trans)

    real_path1 = root_dir + input1
    if not os.path.isfile(real_path1):
      raise ActionInputError("input1 not exist")

    real_path2 = root_dir + input2
    if not os.path.isfile(real_path2):
      raise ActionInputError("input2 not exist")

    input1_dir = os.path.dirname(input1)
    output_dir = self.make_sure_output_dir(tool_name, root_dir, input1_dir)
    output1 = self.make_output_file(output_dir, 1)
    output2 = self.make_output_file(output_dir, 2)
    output3 = self.make_output_file(output_dir, 3)
    output4 = self.make_output_file(output_dir, 4)
    output5 = self.make_output_file(output_dir, 5)

    abspath_output1 = root_dir + output1
    abspath_output2 = root_dir + output2
    abspath_output3 = root_dir + output3
    abspath_output4 = root_dir + output4
    abspath_output5 = root_dir + output5

    agent_cwd = trans.app.config.tool_path + "/custom"
    job_cwd = trans.app.config.tool_path + "/" + tool_dir

    user_id = 0
    if trans.user:
      user_id = trans.user.id

    args = [input1, input2, input3, input4, input5, input6, input7, input8, input9,
      output1, output2, output3, output4, output5]
    xargs = [real_path1, real_path2, input3, input4, input5, input6, input7, input8, input9,
      abspath_output1, abspath_output2, abspath_output3, abspath_output4, abspath_output5]
    
    params = {
      "tool_id": tool_id,
      "tool_name": tool_name,
      "tool_version": tool_version,
      "galaxy_version": trans.app.config.version_major,
      "cwd": job_cwd,
      "params": " ".join(args),
      "session_id": trans.galaxy_session.id,
      "user_id": user_id,
      "status": 1,
      "output": output1,
      "real_output": abspath_output1,
      "output2": output2,
      "real_output2": abspath_output2,
      "output3": output3,
      "real_output3": abspath_output3,
      "output4": output4,
      "real_output4": abspath_output4,
      "output5": output5,
      "real_output5": abspath_output5
    }

    job_id = self.add_job(**params)
    commandstr = "python job_agent.py %d %s %s %s" % (
      job_id, script, job_cwd, " ".join(xargs))
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
    output = [ job["output"] ]
    if job["output2"]:
      log.info("output2 = %s", job["output2"])
      output.append(job["output2"])
    if job["output3"]:
      log.info("output3 = %s", job["output3"])
      output.append(job["output3"])
    if job["output4"]:
      log.info("output4 = %s", job["output4"])
      output.append(job["output4"])
    if job["output5"]:
      log.info("output5 = %s", job["output5"])
      output.append(job["output5"])
    data = {
      "job_id": job["id"],
      "tool_id": job["tool_id"],
      "tool_version": job["tool_version"],
      "tool_name": job["tool_name"]+"-"+str(job["id"]),
      "status": job["status"],
      "params": job["params"],
      "output": output,
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
      output = [ job["output"] ]
      if job["output2"]:
        output.append(job["output2"])
      if job["output3"]:
        output.append(job["output3"])
      if job["output4"]:
        output.append(job["output4"])
      if job["output5"]:
        output.append(job["output5"])
      item = {
        "job_id": job["id"],
        "tool_id": job["tool_id"],
        "tool_version": job["tool_version"],
        "tool_name": job["tool_name"]+"-"+str(job["id"]),
        "status": job["status"],
        "params": job["params"],
        "output": output,
        "create_time": job["create_time"],
        "update_time": job["update_time"]
      }
      items.append(item)

    data = {}
    data["total"] = total
    data["items"] = items
    return data

