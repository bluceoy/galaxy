"""
API operations on Cloud-based storages, such as Amazon Simple Storage Service (S3).
"""

import os
import logging
import shutil

from galaxy import exceptions
from galaxy.exceptions import ActionInputError
from galaxy.managers import (
    cloud,
    datasets
)
from galaxy.web import expose_api, expose_api_raw, expose_api_raw_v2, expose_api_anonymous_v2
from galaxy.webapps.base.controller import BaseAPIController

log = logging.getLogger(__name__)


class FileUtilController(BaseAPIController):
    """
    RESTfull controller for interaction with Amazon S3.
    """

    def __init__(self, app):
        super(FileUtilController, self).__init__(app)

    def make_sure_root(self, trans):
      file_path = trans.app.config.ftp_upload_dir
      if trans.user:
        root_dir = file_path + "/" + trans.user.email 
      else:
        root_dir = file_path + "/tmp/session-" + str(trans.galaxy_session.id)
      if not os.path.exists(root_dir):
        os.makedirs(root_dir)
      log.info("root_dir = %s", root_dir)
      return root_dir

    def ge_relative_root(self, trans):
      pass

    @expose_api_anonymous_v2
    def get_dir(self, trans, **kwargs):
        """
        * GET /api/file/getdir
        :param trans:
        :param kwargs:
        :return: current dir for user.
        """
        work_dir = trans.galaxy_session.work_dir
        if work_dir == "" or work_dir is None:
          work_dir = "/"
        return {"current_dir": work_dir}

    @expose_api_anonymous_v2
    def set_dir(self, trans, payload, **kwargs):
        """
        * POST /api/file/setdir
        :type  trans: galaxy.web.framework.webapp.GalaxyWebTransaction
        :param trans: Galaxy web transaction
        :param kwargs:

        :rtype:  dictionary
        :return: a dictionary containing a `summary` view of the datasets copied from the given cloud-based storage.
        """
        if not isinstance(payload, dict):
            raise ActionInputError('Invalid payload data type. The payload is expected to be a dictionary, '
                                   'but received data of type `{}`.'.format(str(type(payload))))

        missing_arguments = []
        work_dir = payload.get("path", None)
        if work_dir is None:
            missing_arguments.append("path")

        if len(missing_arguments) > 0:
            raise ActionInputError("The following required arguments are missing in the payload: {}".format(missing_arguments))

        trans.galaxy_session.work_dir = work_dir
        trans.sa_session.add(trans.galaxy_session)
        trans.sa_session.flush()
        return {'work_dir': work_dir}

    @expose_api_anonymous_v2
    def list_dir(self, trans, **kwargs):
        """
        * GET /api/file/list
        :type  trans: galaxy.web.framework.webapp.GalaxyWebTransaction
        :param trans: Galaxy web transaction

        :param kwargs:

        :rtype:     dictionary
        :return:    Information about the (un)successfully submitted dataset send jobs,
                    containing the following keys:
                        *   `bucket_name`:                  The name of bucket to which the listed datasets are queued
                                                            to be sent.
                        *   `sent_dataset_labels`:          A list of JSON objects with the following key-value pair:
                            **  `object`:                   The name of object is queued to be created.
                            **  `job_id`:                   The id of the queued send job.

                        *   `failed_dataset_labels`:        A list of JSON objects with the following key-value pair
                                                            representing the datasets Galaxy failed to create
                                                            (and queue) send job for:
                            **  `object`:                   The name of object is queued to be created.
                            **  `error`:                    A descriptive error message.

        """
        # if not trans.user:
        #   log.info("please login first")
        #   raise ActionInputError("please login first")
        log.info("kwargs = %s", kwargs)
        def sort_func(item):
          return item["type"]

        root_dir = self.make_sure_root(trans)
        work_dir = trans.galaxy_session.work_dir
        if work_dir == "" or work_dir is None:
          work_dir = "/"
        if "dir" in kwargs:
          work_dir = kwargs["dir"]
        if work_dir == "/":
          dir = root_dir
        else:
          dir = root_dir + work_dir
        log.info("listdir, root_dir = %s, work_dir = %s, dir = %s", root_dir, work_dir, dir)
        files = os.listdir(dir)
        items = []
        for file in files:
          if file == "." or file == "..":
            continue
          item = {
            "file": file
          }
          if work_dir == "/":
            item["real_path"] = work_dir + file
          else:
            item["real_path"] = work_dir + "/" + file
          file_path = dir + "/" + file
          ctime = int(os.path.getctime(file_path))
          item["ctime"] = ctime
          if os.path.isdir(file_path):
            item["type"] = "dir"
          else:
            item["type"] = "file"
            fsize = os.path.getsize(file_path)
            item["size"] = fsize
          items.append(item)
        items.sort(key=sort_func)
        return {'files': items}

    @expose_api_anonymous_v2
    def create_dir(self, trans, payload, **kwargs):
        """
        * POST /api/file/addfolder
        :type  trans: galaxy.web.framework.webapp.GalaxyWebTransaction
        :param trans: Galaxy web transaction
        :param kwargs:

        :rtype:  dictionary
        :return: a dictionary containing a `summary` view of the datasets copied from the given cloud-based storage.
        """
        if not isinstance(payload, dict):
            raise ActionInputError('Invalid payload data type. The payload is expected to be a dictionary, '
                                   'but received data of type `{}`.'.format(str(type(payload))))

        missing_arguments = []
        work_dir = payload.get("path", None)
        if work_dir is None:
            missing_arguments.append("path")

        if len(missing_arguments) > 0:
            raise ActionInputError("The following required arguments are missing in the payload: {}".format(missing_arguments))

        # file_path = trans.app.config.ftp_upload_dir
        # dir = file_path + "/" + trans.user.email + work_dir
        root_dir = self.make_sure_root(trans)
        dir = root_dir + work_dir
        log.info("root = %s, dir = %s", root_dir, dir)
        if not os.path.exists(dir):
          os.makedirs(dir)
        
        return {'work_dir': work_dir}

    @expose_api_anonymous_v2
    def remove(self, trans, payload, **kwargs):
        """
        * POST /api/file/remove
        :type  trans: galaxy.web.framework.webapp.GalaxyWebTransaction
        :param trans: Galaxy web transaction
        :param kwargs:

        :rtype:  dictionary
        :return: a dictionary containing a `summary` view of the datasets copied from the given cloud-based storage.
        """
        if not isinstance(payload, dict):
          raise ActionInputError('Invalid payload data type. The payload is expected to be a dictionary, '
                                   'but received data of type `{}`.'.format(str(type(payload))))

        missing_arguments = []
        path = payload.get("path", None)

        if path is None:
          missing_arguments.append("path")

        if len(missing_arguments) > 0:
          raise ActionInputError("The following required arguments are missing in the payload: {}".format(missing_arguments))

        root_dir = self.make_sure_root(trans)
        real_path = root_dir + path

        if not os.path.exists(real_path):
          raise ActionInputError("path: %s not found" % (path))

        if os.path.isdir(real_path):
          shutil.rmtree(real_path, ignore_errors=True)
        else:
          os.remove(real_path)

        return {'message': 'Successful.'}

    @expose_api_raw_v2
    def download(self, trans, payload, **kwargs):
      """
      * POST /api/file/download
      """
      missing_arguments = []
      path = payload.get("path", None)

      log.info("path = %s", path)

      root_dir = self.make_sure_root(trans)
      target_file = root_dir + path
      if not os.path.isfile(target_file):
        raise ActionInputError("file = %s, not found" % (path))
      
      basename = os.path.basename(target_file)
      trans.response.set_content_type('application/octet-stream')
      download_file = open(target_file, "rb")
      trans.response.headers["Content-Disposition"] = 'attachment; filename="%s"' % (basename)
      log.info("target = %s", target_file)
      return download_file.read()