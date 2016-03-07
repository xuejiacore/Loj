import logging
import os
import time

from django.http import StreamingHttpResponse


class FileIO(object):
    """
    文件IO类
    """

    def __init__(self, log=None):
        if not log:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S')
            self.logger = logging
        else:
            self.logger = log
        self.sub_dir = time.strftime("%Y/%m/%d/%H/%M/%S/")

    def file_uploader(self, req, f_path=None, child_path=None, namer=None):
        """
        Http文件上传
        :param req:带有Mutipart的Http请求
        :param f_path:指定文件上传目录
        :param child_path:指定子目录的生成方式，function
        :param namer:上传的文件命名方法，function
        :return:返回上传结果字典：status, size, path, file_name
        """
        path = ''
        if req.method == 'POST':
            if f_path:
                self.logger.debug("* File will be upload into '{}'.".format(f_path))
                path = f_path
            else:
                # 如果不指定上传目录，将自动设置为工程的upload_dir目录下为文件的上传目录
                path = 'upload_dir/'
                self.logger.warning("* You have no specify any directory. "
                                    "Use default directory named '{}'".format(path))
        else:
            self.logger.debug("* The request method is not POST, end.")

        if child_path:
            self.sub_dir = child_path()
            self.logger.debug("* Use specified sub directory: {}".format(self.sub_dir))
        else:
            self.logger.debug("* Use default sub directory: {}".format(self.sub_dir))

        path += self.sub_dir
        self.logger.debug("* The full directory is: {}".format(path))

        full_path = path
        f = req.FILES['file']
        file_name = namer() if namer else f.name
        if not os.path.exists(path):
            self.logger.debug("* The directory is not exist! Will be create!")
            os.makedirs(path)
            full_path += file_name
            out = open(full_path, 'wb+')
            for chunk in f.chunks():
                out.write(chunk)
            out.close()
        self.logger.debug("* The full path is: '{}'".format(full_path))
        return {"status": "OK",
                "size": os.path.getsize(full_path),
                "path": full_path,
                "file_name": file_name}

    def single_file_downloader(self, file_path, namer=None):
        """
        单文件下载
        :param file_path:需要下载的文件的路径
        :param namer:使用命名方法设置文件的名称，如果不设置，将使用在服务器中的名字
        :return:
        """
        self.logger.debug("* '{}' is a file: {}".format(file_path, os.path.isfile(file_path)))

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, mode='rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
                os.path.basename(file_path) if not namer else (namer() + file_path[file_path.rfind('.'):]))

        return response
