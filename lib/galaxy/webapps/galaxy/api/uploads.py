"""
API operations for uploaded files in storage.
"""
import logging
import os
import re

from galaxy import exceptions
from galaxy.web import legacy_expose_api_anonymous
from galaxy.webapps.base.controller import BaseAPIController

log = logging.getLogger(__name__)


class UploadsAPIController(BaseAPIController):

    READ_CHUNK_SIZE = 2 ** 16

    @legacy_expose_api_anonymous
    def index(self, trans, **kwd):
        raise exceptions.NotImplemented("Listing uploads is not implemented.")

    @legacy_expose_api_anonymous
    def create(self, trans, payload, **kwd):
        """
        POST /api/uploads/
        """
        session_id = payload.get("session_id")
        session_start = payload.get("session_start")
        session_chunk = payload.get("session_chunk")
        if re.match(r'^[\w-]+$', session_id) is None:
            #raise exceptions.MessageException("Requires a session id.")
            pass
        if session_start is None:
            raise exceptions.MessageException("Requires a session start.")
        if not hasattr(session_chunk, "file"):
            raise exceptions.MessageException("Requires a session chunk.")
        file_path = trans.app.config.ftp_upload_dir
        if trans.user:
            current_dir = trans.galaxy_session.work_dir
            if not current_dir:
                current_dir = "/"
            root_dir = file_path + "/" + trans.user.email + current_dir
        else:
            root_dir = file_path + "/" + "tmp"
        log.info("root_dir = %s", root_dir)
        #target_file = os.path.join(trans.app.config.new_file_path, session_id)
        target_file = os.path.join(root_dir, session_id)
        log.info('upload, target = %s', target_file)
        target_size = 0
        if os.path.exists(target_file):
            target_size = os.path.getsize(target_file)
        if session_start != target_size:
            raise exceptions.MessageException("Incorrect session start.")
        chunk_size = os.fstat(session_chunk.file.fileno()).st_size
        if chunk_size > trans.app.config.chunk_upload_size:
            raise exceptions.MessageException("Invalid chunk size.")
        #fh = open(target_file+".1", "ab")
        with open(target_file, "ab") as f:
            log.info("open, target_file = %s", target_file)
            while True:
                read_chunk = session_chunk.file.read(self.READ_CHUNK_SIZE)
                if not read_chunk:
                    break
                f.write(read_chunk)
                #fh.write(read_chunk)
        #fh.close()
        session_chunk.file.close()
        return {"message": "Successful."}

    @legacy_expose_api_anonymous
    def create_v2(self, trans, payload, **kwd):
        """
        POST /api/uploads_v2/
        """
        session_id = payload.get("filename")
        session_chunk = payload.get("file")
        # if re.match(r'^[\w-]+$', session_id) is None:
        #     raise exceptions.MessageException("Requires a session id.")
        #     pass
        # if not hasattr(session_chunk, "file"):
        #     raise exceptions.MessageException("Requires a session chunk.")
        file_path = trans.app.config.ftp_upload_dir
        if trans.user:
            current_dir = trans.galaxy_session.work_dir
            if not current_dir:
                current_dir = "/"
            root_dir = file_path + "/" + trans.user.email + current_dir
        else:
            root_dir = file_path + "/tmp/session-" + str(trans.galaxy_session.id)
        log.info("uploadv2, root_dir = %s", root_dir)
        target_file = os.path.join(root_dir, session_id)
        log.info('uploadv2, target = %s', target_file)
        chunk_size = os.fstat(session_chunk.file.fileno()).st_size
        if chunk_size > trans.app.config.chunk_upload_size:
            raise exceptions.MessageException("Invalid chunk size.")
        with open(target_file, "ab") as f:
            while True:
                read_chunk = session_chunk.file.read(self.READ_CHUNK_SIZE)
                if not read_chunk:
                    break
                f.write(read_chunk)
        session_chunk.file.close()
        return {"message": "Successful."}