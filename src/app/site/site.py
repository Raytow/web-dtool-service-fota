print(__file__)

import json
import re
import time
import sys
import datetime
import os
import shutil
import random
import string
import io

from zipfile import ZipFile
from shutil import copyfile

from io import BytesIO

#import app.database.api as dbapi
#import app.database.model as dbmodel

import config as config
import app.tool as tool
from app.tool import dbg # for print
import app.error as error


# blueprint
from flask import Blueprint
site_blueprint = Blueprint('site', __name__)

#main flask
from flask import Flask, request, g, redirect, abort, make_response, send_file, send_from_directory, jsonify, Response

#login module
from flask_login import login_user, logout_user, login_required, current_user

def need_to_login():
    dbg('need_to_login')
    raise error.ApiError("ERROR_NOT_LOGGED_IN", error.ERROR_NOT_LOGGED_IN)
    
from app import login_manager
login_manager.unauthorized_handler(need_to_login)

# from app import mysqldb

import subprocess

from werkzeug.wsgi import FileWrapper

#from werkzeug import secure_filename # for upload
#see http://flask.pocoo.org/docs/0.10/patterns/fileuploads/

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

@site_blueprint.before_request
def before_request():
    #dbg("site_blueprint.before_request")
    #dbg(request)
    #dbg(request.headers)
    #dbg("Access-Token is %r" % request.headers['Access-Token'])
    
    # request.mysqldb_session = mysqldb.create_scoped_session(options = {'autocommit':False})
    
    dbg('json_params')
    json_params = request.get_json()
    if json_params is not None:
        for k in json_params:
            dbg((k, json_params[k]))
            
    dbg('request.form')
    for k in request.form:
        dbg((k, request.form[k]))
        
    #for k in request.headers:
    #    dbg((k, request.headers[k]))
        
    #if json_params is not None and 'session_key' in json_params:
    #    request.current_user = dbapi.get_wechat_user(session_key = json_params['session_key'])

    try:
        dbg("User-Agent = {}".format(request.headers.get('User-Agent')))
        dbg("request.url_root = {}".format(request.url_root))
    except:
        tool.print_exception_info()


@site_blueprint.teardown_request
def teardown_request(exception):
    #dbg("site_blueprint.teardown_request")
    #dbg(request)
    #dbg(request.mysqldb_session)

    #request.mysqldb_session.close()
    pass
    

@site_blueprint.errorhandler(error.ApiError)
def handle_api_error(current_error):
    #tool.print_exception_info()
    dbg((current_error.msg, current_error.error_no))
    error_info = error.get_error_info(current_error.error_no)
    #msg = error.get_error_text(current_error.error_no)
    
    to_dump = {'code':current_error.error_no, 'msg':error_info[0]}
    
    if current_error.extra_msg is not None:
        to_dump['msg'] += '(%s)' % current_error.extra_msg
    
    if len(current_error.data) != 0:
        to_dump['data'] = current_error.data
        
    if current_error.param != None:
        to_dump = current_error.param
    return make_response(json.dumps(to_dump), error_info[1])
    
@site_blueprint.errorhandler(Exception)
def handle_base_exception(current_error):
    tool.print_exception_info()
    return make_response(json.dumps({'code':99, 'msg':'操作失败'}), 400)


@site_blueprint.route('/test', methods = ['GET', 'POST'])
def test():
    try:
        return 'test ok'
        # raise error.ApiError("ERROR_INVALID_PARAMETER", error.ERROR_INVALID_PARAMETER, extra_msg = 'test')
    finally:
        dbg('test finally')

'''
@site_blueprint.route('/login', methods = ['POST', 'GET'])
def login():
    dbg('login')
    
    if request.method == 'GET':
        name = request.args.get('name', '', type = str)
        password = request.args.get('password', '', type = str)
    else:
        params = request.get_json()
        dbg(params)
        if params is not None:
            name = params['name']
            password = params['password']
        else:
            name = request.form['name']
            password = request.form['password']
    
    if not openluat_user_api.login_user(name = name, password = password):
        if not openluat_user_api.login_user(phone = name, password = password):
            raise error.ApiError("ERROR_WRONG_PASSWORD", error.ERROR_WRONG_PASSWORD)
        else:
            user = dbapi.get_user(phone = name)
            login_user(user, 1)
    else:
        user = dbapi.get_user(name = name)
        login_user(user, 1)
        
    reply = {'currentAuthority':'admin', 'status':'ok', 'type':'account'}
    
    return make_response(json.dumps(reply), 200)

@site_blueprint.route('/logout', methods = ['POST'])
@login_required
def logout():
    logout_user()
    return make_response('', 200)
'''


@site_blueprint.route('/dfota_diff_image', methods = ['GET', 'POST'])
#@login_required
def dfota_diff_image():
    dbg('dfota_diff_image')

    if request.method == 'POST':
        #dfota_type = request.args.get('dfota_type', '', type = str)
        dfota_type = ""
        return gen_dfota_diff_image(dfota_type, request.files['f1'], request.files['f2'])
    else:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>差分包生成工具</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
                .container { background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); padding: 40px; max-width: 500px; width: 90%; }
                h1 { color: #333; font-size: 28px; margin-bottom: 30px; text-align: center; }
                .file-group { margin-bottom: 25px; }
                label { display: block; color: #555; font-weight: 500; margin-bottom: 8px; font-size: 14px; }
                input[type="file"] { width: 100%; padding: 12px; border: 2px dashed #ddd; border-radius: 8px; cursor: pointer; font-size: 14px; transition: border-color 0.3s; }
                input[type="file"]:hover { border-color: #007bff; }
                .btn-group { display: flex; gap: 10px; margin-top: 30px; }
                button { flex: 1; padding: 14px; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
                #submitBtn { background: #007bff; color: white; }
                #submitBtn:hover { background: #0056b3; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,123,255,0.3); }
                #submitBtn:disabled { background: #6c757d; cursor: not-allowed; transform: none; }
                #downloadBtn { display: none; background: #28a745; color: white; }
                #downloadBtn:hover { background: #218838; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(40,167,69,0.3); }
                #progress { display: none; width: 100%; height: 30px; background: #e9ecef; border-radius: 15px; position: relative; overflow: hidden; margin-top: 20px; }
                #progressBar { width: 0%; height: 100%; background: linear-gradient(90deg, #007bff, #0056b3); transition: width 0.3s; }
                #progressText { position: absolute; width: 100%; text-align: center; line-height: 30px; font-size: 14px; font-weight: 600; color: #333; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>DFOTA差分包生成工具</h1>
                <form id="uploadForm" enctype="multipart/form-data">
                    <div class="file-group">
                        <label>基础版本文件</label>
                        <input type="file" name="f1" id="f1" required>
                    </div>
                    <div class="file-group">
                        <label>目标版本文件</label>
                        <input type="file" name="f2" id="f2" required>
                    </div>
                    <div id="progress"><div id="progressBar"></div><div id="progressText">0%</div></div>
                    <div class="btn-group">
                        <button type="submit" id="submitBtn">生成差分包</button>
                        <button type="button" id="downloadBtn">下载</button>
                    </div>
                </form>
            </div>
            <script>
                let diffBlob = null;
                let filename = '';
                const form = document.getElementById('uploadForm');
                const submitBtn = document.getElementById('submitBtn');
                const downloadBtn = document.getElementById('downloadBtn');
                const progress = document.getElementById('progress');
                const progressBar = document.getElementById('progressBar');
                const progressText = document.getElementById('progressText');

                form.onsubmit = async (e) => {
                    e.preventDefault();
                    submitBtn.textContent = '上传中...';
                    submitBtn.disabled = true;
                    progress.style.display = 'block';

                    const formData = new FormData(form);
                    const xhr = new XMLHttpRequest();

                    xhr.upload.onprogress = (e) => {
                        if (e.lengthComputable) {
                            const percent = Math.round((e.loaded / e.total) * 100);
                            progressBar.style.width = percent + '%';
                            progressText.textContent = percent + '%';
                        }
                    };

                    xhr.onload = () => {
                        if (xhr.status === 200) {
                            diffBlob = xhr.response;
                            filename = xhr.getResponseHeader('x-filename') || 'dfota.bin';
                            progress.style.display = 'none';
                            submitBtn.style.display = 'none';
                            downloadBtn.style.display = 'inline-block';
                        } else {
                            alert('生成失败');
                            submitBtn.textContent = '生成差分包';
                            submitBtn.disabled = false;
                            progress.style.display = 'none';
                        }
                    };

                    xhr.onerror = () => {
                        alert('生成失败');
                        submitBtn.textContent = '生成差分包';
                        submitBtn.disabled = false;
                        progress.style.display = 'none';
                    };

                    xhr.open('POST', '/site/dfota_diff_image');
                    xhr.responseType = 'blob';
                    xhr.send(formData);
                };

                downloadBtn.onclick = () => {
                    const a = document.createElement('a');
                    a.href = URL.createObjectURL(diffBlob);
                    a.download = filename;
                    a.click();
                    location.reload();
                };
            </script>
        </body>
        </html>
        '''

def cleanup_old_dfota_files(keep_count=20):
    try:
        items = []
        for item in os.listdir(config.SITE_DFOTA_DIR):
            item_path = os.path.join(config.SITE_DFOTA_DIR, item)
            if os.path.isdir(item_path):
                items.append((os.path.getmtime(item_path), item_path))

        items.sort(reverse=True)

        for _, path in items[keep_count:]:
            shutil.rmtree(path)
            dbg(f"Deleted old directory: {path}")
    except:
        tool.print_exception_info()

def gen_dfota_diff_image(dfota_type, f1, f2):
    cleanup_old_dfota_files(20)

    dfota_tool_dir = "fota_8910_2"

    file_type = 1
    no_core = False # 不包含core版本

    # 20220209 区分8910和1603的方法
    # 解压.dfota.bin得到.bin。再解压.bin，如果包含fota_pkg.bin就是1603。
    if True:
        now_time = datetime.datetime.now()
        time_string = now_time.strftime('%Y%m%d%H%M%S_%f')

        fota_tool = '8910'

        if file_type == 0: # 两个文件直接差分

            file = f1
            base_file_name = file.filename + "_df_base_" + time_string
            base_file_path = os.path.join(config.SITE_DFOTA_DIR, base_file_name)
            dbg("save file:{}".format(base_file_path))
            file.save(base_file_path)

            file = f2
            target_file_name = file.filename + "_df_target_" + time_string
            target_file_path = os.path.join(config.SITE_DFOTA_DIR, target_file_name)
            dbg("save file:{}".format(target_file_path))
            file.save(target_file_path)

            diff_file_name = 'dfota_diff_%s_%s_%s.bin' % (base_file_name[:6], target_file_name[:6], time_string)

            cmd = "%s --pac %s,%s,%s %s" % (config.SITE_THIRDPARTY_DIR + 'dfota/' + dfota_tool_dir + '/dtools fotacreate2', base_file_path, target_file_path, config.SITE_THIRDPARTY_DIR + 'dfota/' + dfota_tool_dir + '/setting/fota8910.xml', config.SITE_DFOTA_DIR + diff_file_name)

            dbg(cmd)
                
            result = subprocess.call(cmd.split())
            dbg(result)

            if result == 0:
                return make_response(send_file(config.SITE_DFOTA_DIR + diff_file_name))

            else:
                raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "dfota %s return %d" % (dfota_type, result))
        
        elif file_type == 1:
            try:
                random_dir = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
                os.mkdir(config.SITE_DFOTA_DIR + random_dir)

                a_path = config.SITE_DFOTA_DIR + random_dir + '/a/'
                b_path = config.SITE_DFOTA_DIR + random_dir + '/b/'
                os.mkdir(a_path)
                os.mkdir(b_path)
            except:
                tool.print_exception_info()
                raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "系统繁忙")

            dbg((f1.filename, f2.filename))

            # 20210326 lijiaodi 不允许8910从1.2升到1.3
            if re.match("^.*AirM2M_720U_.*$", f1.filename) or re.match("^.*AirM2M_720UH_.*$", f1.filename) or re.match(".*8910.*", f1.filename):
                if re.match("^.*AirM2M_720U_.*$", f2.filename) or re.match("^.*AirM2M_720UH_.*$", f2.filename) or re.match(".*8910.*", f2.filename):
                    match_result = re.match('.*_V(\d{1,}).*', f1.filename)
                    if match_result:
                        core_version_1 = int(match_result.groups()[0])
                        match_result = re.match('.*_V(\d{1,}).*', f2.filename)
                        if match_result:
                            core_version_2 = int(match_result.groups()[0])
                            if core_version_1 < 2000: # 1.2
                                if (3000 <= core_version_2 and core_version_2 < 4000) or (300000 <= core_version_2 and core_version_2 < 310000): # 1.3
                                        raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "cat1不允许从1.2升至1.3")

                            if core_version_2 < core_version_1:
                                dbg((core_version_2, core_version_1))
                                raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "不允许降版本")

            file = f1
            base_file_name = file.filename + "_df_base_" + time_string
            base_file_path = os.path.join(config.SITE_DFOTA_DIR + random_dir, base_file_name)
            dbg("save file:{}".format(base_file_path))
            file.save(base_file_path)

            file = f2
            target_file_name = file.filename + "_df_target_" + time_string
            target_file_path = os.path.join(config.SITE_DFOTA_DIR + random_dir, target_file_name)
            dbg("save file:{}".format(target_file_path))
            file.save(target_file_path)

            try:
                # unzip
                zf = ZipFile(base_file_path) # open
                a_file_names = zf.namelist() # os.listdir(unzip_dir)
                zf.extractall(a_path) # unzip

                zf = ZipFile(target_file_path) # open
                b_file_names = zf.namelist() # os.listdir(unzip_dir)
                zf.extractall(b_path) # unzip
            except:
                tool.print_exception_info()
                raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "解压出错，请检查。")

            a_image_path = None

            for name in a_file_names:
                if name not in ['app.bin', 'fota_pkg.bin']: # first non app.bin
                    a_image_path = a_path + name
                    break

            if a_image_path is None:
                dbg('a_image_path is None')
                raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "基础版本内core文件缺失，请检查(0)。")

            try:
                b_image_path = ''
                b_app_path = ''
                b_fota_pkg_path = ''

                for name in b_file_names:
                    if name not in ['app.bin', 'fota_pkg.bin']:
                        b_image_path = b_path + name
                    elif name == 'app.bin':
                        b_app_path = b_path + name
                    elif name == 'fota_pkg.bin':
                        b_fota_pkg_path = b_path + name

                if b_image_path == '': # or b_app_path == '':
                    #raise
                    # 不存在core。那么只打包lua。
                    if b_app_path == '':
                        raise

                    no_core = True
            except:
                tool.print_exception_info()
                raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "目标版本内文件缺失，请检查。")

            result = 0

            if no_core: # 没有core版本。不用生成差分包
                dbg('no core')
            else:
                # 判断工具
                try:
                    if 'fota_pkg.bin' in a_file_names:
                        fota_tool = '1603'
                except:
                    tool.print_exception_info()

                dbg('fota_tool = %s' % fota_tool)

                diff_file_name = 'dfota_diff_%s_%s_%s.bin' % (base_file_name[:6], target_file_name[:6], time_string)
                diff_file_path = config.SITE_DFOTA_DIR + random_dir + '/' + diff_file_name

                cmd = ''
                if fota_tool == '8910':
                    cmd = "%s --pac %s,%s,%s %s" % (config.SITE_THIRDPARTY_DIR + 'dfota/' + dfota_tool_dir + '/dtools fotacreate2', a_image_path, b_image_path, config.SITE_THIRDPARTY_DIR + 'dfota/' + dfota_tool_dir + '/setting/fota8910.xml', diff_file_path)
                elif fota_tool == '1603':
                    cmd = "%s -p %s %s %s" % (config.SITE_THIRDPARTY_DIR + 'dfota/fota_1603/adiff_lnx_max_path_2048_2', a_image_path, b_image_path, diff_file_path)

                dbg(cmd)
                    
                result = subprocess.call(cmd.split())
                dbg(result)

            if result == 0:
                # 组成最终bin文件
                # see opebluat -> gen_dfota_final_bin

                final_bin_name = f2.filename.rsplit('.', 1)[0] + '_dfota.bin'
                final_bin_path = config.SITE_DFOTA_DIR + final_bin_name
                file_bin_data = None

                #if re.match('.*AirM2M_.*', base_file_name): # if AT
                if re.match('.*AirM2M_.*', base_file_name) and not re.match('.*AirM2M_720C.*', base_file_name): # at直接传差分包(除了1603(720C))
                    copyfile(diff_file_path, final_bin_path) # at 直接传差分包
                else:
                    try:
                        file_count = 0
                        file_data = bytearray([])

                        if not no_core:
                            # 差分文件
                            file_count += 1
                            file_data += bytearray([0x7D]) # dfota_bin

                            dfota_bin_size = int(os.path.getsize(diff_file_path))
                            dbg('dfota_bin_size = %d' % dfota_bin_size)
                            file_data += int(dfota_bin_size).to_bytes(4, 'big')
                            
                            with open(diff_file_path, "rb") as dfota_bin_file:
                                file_data += dfota_bin_file.read()

                        # app文件
                        if b_app_path != '': # 可不含app.bin
                            file_count += 1
                            file_data += bytearray([0x7C]) # app.bin
                        
                            lua_bin_size = int(os.path.getsize(b_app_path))
                            dbg('lua_bin_size = %d' % lua_bin_size)
                            file_data += int(lua_bin_size).to_bytes(4, 'big')
                            
                            with open(b_app_path, "rb") as lua_bin_file:
                                file_data += lua_bin_file.read()

                        # fota_pkg.bin
                        if b_fota_pkg_path != '':
                            file_count += 1
                            file_data += bytearray([0x7B]) # fota_pkg.bin
                        
                            fota_pkg_size = int(os.path.getsize(b_fota_pkg_path))
                            dbg('fota_pkg_size = %d' % fota_pkg_size)
                            file_data += int(fota_pkg_size).to_bytes(4, 'big')
                            
                            with open(b_fota_pkg_path, "rb") as fota_pkg_file:
                                file_data += fota_pkg_file.read()

                        # 写入最终bin文件
                        with open(final_bin_path, "wb") as file:
                            file_bin_data = bytearray([0x7e]) + int(file_count).to_bytes(4, 'big') + file_data
                            #file.write(bytearray([0x7e]))
                            #file.write(int(file_count).to_bytes(4, 'big'))
                            #file.write(file_data)

                            file.write(file_bin_data)

                        dbg('final_bin_path %s' % final_bin_path)
                        dbg(int(os.path.getsize(final_bin_path)))
                    except:
                        tool.print_exception_info()
                        raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "生成bin文件失败")

                filename = final_bin_name
                res = Response(FileWrapper(io.BytesIO(file_bin_data)), mimetype = "application/octet-stream", direct_passthrough = True)
                res.headers["x-filename"] = filename
                res.headers["Content-Disposition"] = "attachment;filename=%s" % filename

                return res
                #return make_response(json.dumps({'url':config.SITE_DFOTA_URL + final_bin_name}, cls = ComplexEncoder), 200) 
            else:
                dbg('dfota fail 1')
                raise error.ApiError("ERROR_FAIL", error.ERROR_FAIL, extra_msg = "dfota %s return %d" % (dfota_type, result))
    else:
        raise error.ApiError("ERROR_INVALID_PARAMETER", error.ERROR_INVALID_PARAMETER)
    
    raise error.ApiError("ERROR_INVALID_PARAMETER", error.ERROR_INVALID_PARAMETER)
    
