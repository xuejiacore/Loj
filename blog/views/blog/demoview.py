from django.shortcuts import render

from Personal import settings
from lib.io.HttpIO import FileIO

import logging

logger = logging.getLogger('app')


def demo(request, whose):
    print("username = {}".format(whose))
    return render(request, 'blog/upload.html')


def ckeditor(request, whose):
    return render(request, 'blog/ckeditor.html')


def upload_file(request, whose):
    fio = FileIO(logger)
    result = fio.file_uploader(request, f_path=settings.FILE_UPLOAD_PATH)
    logger.debug("* 上传成功：{}".format(result.full_path))


def download_file(request, whose):
    fio = FileIO(logger)
    return fio.single_file_downloader(r'F:\Backup\2016-02-01160728_周一_跟据PPT内容进行修改wxzh.7z',
                                      lambda: "2016-02-21 16:58:26")
