ERROR_OK = 0
ERROR_FAIL = 1
ERROR_UNKNOWN_COMMAND = 2
ERROR_APP_KEY = 3
ERROR_LOGIN = 4
ERROR_BIND = 5
ERROR_PERMISSION = 6
ERROR_TIMEOUT = 7
ERROR_DEVICE_RESULT = 8
ERROR_INVALID_SHARE = 9
ERROR_WRONG_PASSWORD = 10
ERROR_INVALID_DEVICE = 11
ERROR_PARTIALLY_FAILED = 12
ERROR_DTU_OUTPUT_EXIST = 13
ERROR_PERMISSION_DENIED = 14
ERROR_NEED_BIN_FILE = 15
ERROR_INVALID_PARAMETER = 16
ERROR_NOT_LOGGED_IN = 17
ERROR_EXISTS = 18


error_info = {ERROR_OK:["操作成功", 200],
              ERROR_FAIL:["操作失败", 400],
              ERROR_UNKNOWN_COMMAND:["无效的命令", 400],
              ERROR_APP_KEY:["授权失败", 400],
              ERROR_LOGIN:["登录失败", 400],
              ERROR_BIND:["绑定失败", 400],
              ERROR_PERMISSION:["无权限", 400],
              ERROR_TIMEOUT:["设备超时", 400],
              ERROR_DEVICE_RESULT:["设备异常", 400],
              ERROR_INVALID_SHARE:["无效的分享", 400],
              ERROR_WRONG_PASSWORD:["密码错误", 400],
              ERROR_INVALID_DEVICE:["无效的设备", 400],
              ERROR_PARTIALLY_FAILED:["部分操作失败", 400],
              ERROR_DTU_OUTPUT_EXIST:["DTU已出过库", 400],
              ERROR_PERMISSION_DENIED:["无权限", 400],
              ERROR_NEED_BIN_FILE:["升级文件有误,请选择bin文件.", 400],
              ERROR_INVALID_PARAMETER:["参数错误", 400],
              ERROR_NOT_LOGGED_IN:["未登录", 400],
              ERROR_EXISTS:["已存在", 400],
}

def get_error_info(error_no):
    if error_no in error_info:
        return error_info[error_no]
    else:
        return None
        
class ApiError(Exception):
    def __init__(self, msg, error_no = 1, http_status_code = 500, data = {}, param = None, extra_msg = None):
        self.msg = msg
        self.error_no = error_no
        self.http_status_code = http_status_code
        self.data = data
        self.param = param
        self.extra_msg = extra_msg
        
    def __str__(self):
        return repr(self.msg)