#!/usr/local/bin/python3

from bottle import Bottle, redirect,route,static_file,jinja2_template as template,request
from beaker.middleware import SessionMiddleware
import secrets

from utils.processing import Processing

import werkzeug
import os
from datetime import datetime



app = Bottle()

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

apps = SessionMiddleware(app, session_opts)
token = ''


@app.route('/static/<file_path:path>')
def server_static(file_path):
    return static_file(file_path, root='./static/')

@app.route('/download/<file_path:path>')
def download_static(file_path):
    # ファイル名を取得し、ダウンロード時の指定に使っている
    file_name = os.path.basename(file_path)
    return static_file(file_path, root='./static/', download="DL_"+ file_name)

@app.route('/')
def home():
    global token
    session1 = request.environ.get('beaker.session')
    session1['logged_in'] = True
    session1.save()
    token = secrets.token_urlsafe(32)
    data = {
           "token": token,
    }
    return template("home.html",data)

@app.route('/',method="POST")
def upload():
    global token
    if not checkToken():
        redirect("/")
    token = secrets.token_urlsafe(32)
    upload = request.files.get('upload', '')
    if not upload:
        return '<script>alert("画像をアップロードして下さい"); location.href = location.href;</script>'
    
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return '<script>alert("画像をアップロードして下さい"); location.href = location.href;</script>'
    
    save_path = get_save_path()
    saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") + werkzeug.utils.secure_filename(upload.filename)
    upload.save(os.path.join(save_path,saveFileName))
    
    makeimg = Processing.mask_img(save_path,saveFileName)
    if(makeimg):
       data = {
           "img_path": saveFileName,
           "img_change":makeimg
           }
       return template("upload.html",**data)
    else:
        os.remove(os.path.join(save_path,saveFileName))
        return '<script>alert("認識できませんでした。なるべく正面から撮った写真をアップロードして下さい。"); location.href = location.href;</script>'

def get_save_path():
    path_dir = "static/img/output/"
    return path_dir

def checkToken():
    return (secrets.compare_digest(token, request.forms.get("token")))