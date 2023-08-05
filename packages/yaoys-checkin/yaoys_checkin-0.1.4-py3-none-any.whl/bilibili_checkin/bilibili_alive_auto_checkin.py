import os

import requests
import urllib3
from yaoysTools.log import getLogger, log_info

from model.all_class_parent import allClassParent

from config.checkin_log_config import log_config

bilibili_checkin_url = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign'

# 解决出现警告 Adding certificate verification is strongly advised.
urllib3.disable_warnings()


class bilibili_alive(allClassParent):
    def __init__(self, **kwargs):
        super(bilibili_alive, self).__init__(**kwargs)
        if self.logger is None:
            self.logger = getLogger(log_name=str(os.path.basename(__file__)).split('.')[0],
                                    log_path=log_config['log_path'],
                                    log_level=log_config['log_level'],
                                    save_log2_file=log_config['save_log2_file'],
                                    is_only_file=log_config['is_only_file'],
                                    log_file_name=log_config['log_file_name'],
                                    is_split_log=log_config['is_split_log'],
                                    is_all_file=log_config['is_all_file'])

        self.checkin_message, self.is_success = self.bilibili_alive_sign()

        # self.get_checkin_message()

    def __get_header(self):
        header = {
            'Connection': 'Keep-Alive',
            'Accept': '*/*',
            'Accept-Language': 'zh-cn',
            'Cookie': self.cookie,
            'Host': 'api.live.bilibili.com',
            'Content-Type': 'application/json;charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                          ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                          "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                          "4 clientChannelId/qq proVersion/1.0.6",
            "Referer": "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign",
            "Accept-Encoding": "gzip, deflate",
        }
        return header

    def bilibili_checkin(self):
        header = self.__get_header()
        resp = requests.get(url=bilibili_checkin_url, headers=header, verify=False)
        result = resp.text
        result_json = resp.json()
        resp.close()
        # 签到成功
        if 'code' in result and 'data' in result and result_json['code'] == 0:
            check_message = 'checkin success,the message is: ' + result_json['data']['text']
        # 签到失败
        elif 'code' in result and result_json['code'] == 1011040:
            check_message = result_json['message']
        # 账号未登录,cookie过期
        elif 'code' in result and result_json['code'] == -101:
            check_message = result_json['message'] + ',cookie过期，请更新cookie'
        else:
            check_message = 'bilibili_Alive checkin error'
        check_message = 'The bilibili_Alive checkin message: ' + check_message
        # log_info(check_message, my_logger=checkin_logger)
        return check_message

    def bilibili_alive_checkin_main(self):
        if self.cookie is None or len(self.cookie) <= 0:
            return self.checkin_message

        account_checkin_message = self.bilibili_checkin()

        # 存在账户签到信息，说明成功执行了签到
        if account_checkin_message is not None and len(account_checkin_message) > 0:
            log_info(f"[Bilibili_Alive_Account_{self.account_index}]:" + str(account_checkin_message), my_logger=self.logger)
            self.checkin_message.append(f"[Bilibili_Alive_Account_{self.account_index}] " + str(account_checkin_message) + "      \n")
        return self.checkin_message

    def bilibili_alive_sign(self):
        if self.config is None or self.config == '':
            # checkin_message.append('bilibili_alive cookie is none')
            return ''.join(self.checkin_message), False
        try:
            # bilibili直播签到
            # 单账号
            log_info('*******************************bilibili_alive checkin*******************************', my_logger=self.logger)
            if isinstance(self.config, str) is True:
                self.cookie = self.config
                self.account_index = 1
                self.checkin_message = self.bilibili_alive_checkin_main()
            elif isinstance(self.config, list) is True:
                for i in range(0, len(self.config)):
                    if isinstance(self.config[i], dict) is True:
                        self.cookie = self.config[i]['cookie']
                        self.account_index = i + 1
                        self.checkin_message = self.bilibili_alive_checkin_main()
                    else:
                        log_info('bilibili_live config error' + '    \n', my_logger=self.logger)
                        self.checkin_message.append('bilibili_live config error' + '    \n')
            else:
                log_info('bilibili_live config error' + '    \n', my_logger=self.logger)
                self.checkin_message.append('bilibili_live config error' + '    \n')
            log_info('*******************************bilibili_alive checkin complete*******************************', my_logger=self.logger)
            return ''.join(self.checkin_message), True
        except Exception as e:
            self.checkin_message.append('main function: bilibili_live checkin error, the error is ' + str(e) + '    \n')
            log_info('main function: bilibili_live checkin error, the error is ' + str(e) + '    \n', my_logger=self.logger)
            log_info('*******************************bilibili_alive error*******************************', my_logger=self.logger)
            return ''.join(self.checkin_message), False
