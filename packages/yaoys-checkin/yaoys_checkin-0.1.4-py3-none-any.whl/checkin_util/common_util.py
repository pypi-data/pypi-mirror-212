import os

from yaoysTools.log import log_error


def print_message(is_print=True, message=None):
    if is_print and message is not None and len(message) > 0:
        print(str(message))


def get_config_path(logger=None):
    config_path = None
    config_path_list = []
    config_path_array = ["/ql/scripts/config.json",
                         "./config/config.json",
                         "./config.json",
                         "../config/config.json"]
    for one_path in config_path_array:
        _config_path = os.path.join(os.getcwd(), one_path)
        if os.path.exists(_config_path):
            config_path = os.path.normpath(_config_path)
            break
        config_path_list.append(os.path.normpath(os.path.dirname(_config_path)))

    if config_path is None:
        log_error("未找到 config.json 配置文件\n请在下方任意目录中添加「config.json」文件:\n" + "\n".join(config_path_list), my_logger=logger)
        raise FileNotFoundError("未找到 config.json 配置文件\n请在下方任意目录中添加「config.json」文件:\n" + "\n".join(config_path_list))
    return config_path
