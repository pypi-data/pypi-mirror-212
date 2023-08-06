import os

import requests
from yaoysTools.log import getLogger, log_info

from checkin_util.constants import request_timeout
from config.checkin_log_config import log_config


class pushPlus(object):
    def __init__(self, token=None, checkin_message=None, logger=None, title=None):
        self.token = token
        self.checkin_message = checkin_message
        self.logger = logger
        self.title = title
        if self.logger is None:
            self.logger = getLogger(log_name=str(os.path.basename(__file__)).split('.')[0],
                                    log_path=log_config['log_path'],
                                    log_level=log_config['log_level'],
                                    save_log2_file=log_config['save_log2_file'],
                                    is_only_file=log_config['is_only_file'],
                                    log_file_name=log_config['log_file_name'],
                                    is_split_log=log_config['is_split_log'],
                                    is_all_file=log_config['is_all_file'])

    def send_message(self):
        if self.token is None or str(self.token) == '':
            return None
        else:
            if self.checkin_message is None:
                self.checkin_message = ''
            content = ''
            for i in range(0, len(self.checkin_message)):
                content += str(self.checkin_message[i])
            # content = '\n'.join(str(i) for i in self.checkin_message)
            payload = {'token': self.token, "channel": "wechat", "template": "html", "content": content, "title": self.title}
            resp = requests.post("http://www.pushplus.plus/send", params=payload, timeout=request_timeout)
            if resp.status_code == 200:
                log_info('push plus success code:' + str(resp.status_code), my_logger=self.logger)
            else:
                log_info('push message to push plus error,the code is:' + str(resp.status_code), my_logger=self.logger)
            resp.close()


class server(object):
    def __init__(self, token=None, checkin_message=None, logger=None, title=None):
        self.token = token
        self.checkin_message = checkin_message
        self.logger = logger
        self.title = title
        if self.logger is None:
            self.logger = getLogger(log_name=str(os.path.basename(__file__)).split('.')[0],
                                    log_path=log_config['log_path'],
                                    log_level=log_config['log_level'],
                                    save_log2_file=log_config['save_log2_file'],
                                    is_only_file=log_config['is_only_file'],
                                    log_file_name=log_config['log_file_name'],
                                    is_split_log=log_config['is_split_log'],
                                    is_all_file=log_config['is_all_file'])

    def send_message(self):

        if self.checkin_message is None:
            self.checkin_message = ''
        content = ''
        for i in range(0, len(self.checkin_message)):
            content += str(self.checkin_message[i])
        payload = {"title": self.title, "desp": content}
        resp = requests.post(f"https://sctapi.ftqq.com/{self.token}.send", params=payload, timeout=request_timeout)
        result = resp.json()

        if result["code"] == 0:
            log_info("Push the message to server success(code:0),the code is:" + str(result["code"]), my_logger=self.logger)
        if result["code"] != 0:
            log_info("Push the message to server error(code!=0),The error message is " + str(result["code"]) + str(result["message"]), my_logger=self.logger)
        code = resp.status_code
        resp.close()
        return code