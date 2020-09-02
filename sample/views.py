from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import auth
from json import loads,dumps
from django.contrib.auth.decorators import login_required
import os
from .models import PathItem,FileItem
from django.views.decorators.csrf import csrf_exempt
import shutil
from django.contrib.auth.models import User
from datetime import datetime
from datetime import datetime,timedelta
from django.template import loader
from . import models
import random
from django.utils import timezone
import requests
from . import  forms

def createRandomString(len):
    print ('wet'.center(10,'*'))
    raw = ""
    range1 = range(58, 65) # between 0~9 and A~Z
    range2 = range(91, 97) # between A~Z and a~z

    i = 0
    while i < len:
        seed = random.randint(48, 122)
        if ((seed in range1) or (seed in range2)):
            continue;
        raw += chr(seed);
        i += 1
    # print(raw)
    return raw

def login(request):
    if not 'name' in request.COOKIES:
        t1 = loader.get_template('userinfo1.html')
        namea = createRandomString(10)
        context_dic = {}
        context_dic['name'] = namea
        response = HttpResponse(t1.render(context_dic))
        response.set_cookie('name', namea)
    else:
        namea = request.COOKIES['name']
        context_dic = {}
        context_dic['name'] = namea
        t1 = loader.get_template('userinfo.html')
        response = HttpResponse(t1.render(context_dic))
    return response

def munue(request):
    username = None
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
    context_dic = {}
    context_dic['username'] = username
    context_dic['problem'] = [{"pid":"1", "sid":"实验一","title":"javaspringboot入门"},{"pid":"2","sid":"实验二", "title":"javaspring连接mysql"}]
    return render(request, 'mune.html', context_dic)

def index(request,pid):
    if not 'name' in request.COOKIES:
        return HttpResponse('生成用户信息')
    a = [{"pid": "1", "sid": "实验一", "title": "javaspringboot入门","detail":"入门springboot并且在123路由下输出index\n数据库账号:root\n数据库密码：123456\n端口:127.0.0.1:3307"},
                              {"pid": "2", "sid": "实验二", "title": "javaspring连接mysql","detail":"连接数据库并且读取向数据库中插入数据并且读取\n数据库账号:root\n数据库密码：123456\n端口:127.0.0.1:3307"}]
    current1 = '/home/ubuntu/exp/first-app-by-maven'
    current = '/home/ubuntu/exp/'+ request.COOKIES['name']
    username = request.COOKIES['name']
    fuport = models.CSpringports.objects.filter(user=username)
    if (len(fuport) == 0):
        return render(request, 'porterror.html',locals())
    if not os.path.exists(current):
        command = 'sudo cp -r ' + current1 + ' ' + current
        a = os.system(command)
        print(a)
    context_dic = {}
    print(int(pid)-1)
    try:
        context_dic['pdetail'] = a[int(pid)-1]
    except:
        return HttpResponse('正在创建文件夹，刷新一下稍等')
    context_dic['current'] = current
    context_dic['port'] = fuport[0].port+13470
    ps = os.listdir(current)
    path = []
    file = []
    for n in ps:
        if (n == '.DS_Store'):
            continue
        v = os.path.join(current, n)
        if os.path.isdir(v):
            p = PathItem(n, '',True)
            print(p.url)
            path.append(p)
        else:
            f = FileItem(n, '')
            file.append(f)

    context_dic['path'] = path
    context_dic['file'] = file
    context_dic['parentu'] = '/'
    print(context_dic)
    return render(request, 'index1.html', context_dic)


def show_folder(request, url):
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
        fuport = models.CSpringports.objects.filter(user=username)
        #user = User.objects.get(username=username)
        #fuport = models.Springports.objects.filter(user=user)
    else:
        return HttpResponse('请登录')
    a = [{"pid": "1", "sid": "实验一", "title": "javaspringboot入门",
          "detail": "入门springboot并且在123路由下输出index\n数据库账号:root\n数据库密码：123456\n端口:127.0.0.1:3307"},
         {"pid": "2", "sid": "实验二", "title": "javaspring连接mysql",
          "detail": "连接数据库并且读取向数据库中插入数据并且读取\n数据库账号:root\n数据库密码：123456\n端口:127.0.0.1:3307"}]
    current = '/home/ubuntu/exp/'+username+'/'+url
    context_dic = {}
    context_dic['current'] = current
    ps = os.listdir(current)
    print(ps)
    path = []
    File = []
    for n in ps:
        if (n == '.DS_Store'):
            continue
        v = os.path.join(current, n)
        if os.path.isdir(v):
            p = PathItem(n, url,True)
            path.append(p)
        else:
            f = FileItem(n, url)
            File.append(f)
    # context_dic['parent'] = os.path.pardir(url)
    context_dic['path'] = path
    context_dic['file'] = File
    context_dic['port'] = fuport[0].port + 13470
    print(url)
    if(url.rfind('/')!=-1):
        context_dic['parent'] = '/folder/'+url[0:url.rfind('/')]
        context_dic['parentu'] = '/'+url
        print('=====')
        print(context_dic['parentu'])
    else:
        context_dic['parent'] = '/problem/'+'1'
        context_dic['parentu'] = '/'+url
        print('------')
        print(context_dic['parentu'])
    return render(request, 'index1.html', context_dic)

@csrf_exempt
def gettxt(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
    else:
        return HttpResponse('请登录')
    current = '/home/ubuntu/exp/'+username+'/'+json_result['url']
    print(current)
    with open(current, 'r') as f:
        r = f.readlines()
    str = ''
    for i in r:
        str += i
    return HttpResponse(str)

@csrf_exempt
def puttxt(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
    else:
        return HttpResponse('请登录')
    current = '/home/ubuntu/exp/'+username+'/'+json_result['url']
    print(current)
    print(json_result['content'])
    f= open(current, 'w')
    f.write(json_result['content'])
    return HttpResponse('succeess')

@csrf_exempt
def mkdir(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
    else:
        return HttpResponse('请登录')
    print("++++++j")
    print(json_result['fname'],json_result['froot'])
    current = '/home/ubuntu/exp/'+username + json_result['froot']+'/'+json_result['fname']
    path = current.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        print(path + ' 创建成功')
        return HttpResponse('success')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return HttpResponse('False')

@csrf_exempt
def delete(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
    else:
        return HttpResponse('请登录')
    print(json_result['froot'])
    current = '/home/ubuntu/exp/'+username+'/'+ json_result['froot']
    path = current.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if  isExists:
        # 如果不存在则创建目录
        shutil.rmtree(path)
        print(path + ' 删除成功')
        return HttpResponse('success')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return HttpResponse('False')

@csrf_exempt
def mkfile(request):
    if (request.method == 'POST'):
        postBody = request.body
        json_result = loads(postBody)
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
    else:
        return HttpResponse('请登录')
    print(json_result['fname'],json_result['froot'])
    current = '/home/ubuntu/exp/'+username+'/' + json_result['froot']+json_result['fname']
    print(current)
    path = current.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        fd = open(path, mode="w", encoding="utf-8")
        fd.close()
        print(path + ' 创建成功')
        return HttpResponse('success')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return HttpResponse('False')

@csrf_exempt
def runjar(request):
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
        fuport = models.CSpringports.objects.filter(user=username)
        if(len(fuport)==0):
            return HttpResponse('无端口去个人信息中生成端口')
    else:
        return HttpResponse('请登录')

    expp = '/home/ubuntu/exp/'+username+'D'
    if not os.path.exists(expp):
        command = 'sudo cp -r ' + '/home/ubuntu/exp/1' + ' ' + expp
        a = os.system(command)
    command ='cp /home/ubuntu/exp/'+username.lower()+'/target/first-app-by-maven-1.0.0-SNAPSHOT.jar '+expp+';sudo docker build -t first-app1-'+username.lower()+' '+expp+';sudo docker run -d -p '+str(fuport[0].port)+':8080 first-app1-'+username.lower()
    try:
        os.system(command)
        return HttpResponse('running')
    except:
        return HttpResponse('error')

@csrf_exempt
def endjar(request):
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
        fuport = models.CSpringports.objects.filter(user=username)
        if(len(fuport)==0):
            return HttpResponse('无端口去个人信息中生成端口')
    else:
        return HttpResponse('请登录')
    command = 'sudo docker ps -q --filter ancestor="first-app1-"'+username.lower()+' | xargs -r sudo docker stop;sudo docker ps -a | grep "Exited" |xargs sudo docker rm;sudo docker images|grep first-app1-'+username.lower()+'|xargs sudo docker rmi'
    try:
        os.system(command)
        return HttpResponse('running')
    except:
        return HttpResponse('error')

@csrf_exempt
def makejar(request):
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
    else:
        return HttpResponse('请登录')
    os.chdir('/home/ubuntu/exp/'+username)
    command ='/usr/local/apache-maven-3.6.3/bin/mvn package'
    try:
        a = os.system(command)
        print(a)
        return HttpResponse(a)
    except:
        return HttpResponse('error')

@csrf_exempt
def makemysql(request):
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
        fuport = models.CSpringports.objects.filter(user=username)
        if(len(fuport)==0):
            return HttpResponse('无端口去个人信息中生成端口')
    else:
        return HttpResponse('请登录')
    command = 'sudo docker run -p '+str(fuport[0].port+10000)+':3306 --name mysql1'+username.lower()+' -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7.26'
    try:
        a = os.system(command)
        print(a)
        return HttpResponse(a)
    except:
        return HttpResponse('error')

@csrf_exempt
def stopmysql(request):
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
        fuport = models.CSpringports.objects.filter(user=username)
        if(len(fuport)==0):
            return HttpResponse('无端口去个人信息中生成端口')
    else:
        return HttpResponse('请登录')
    command = 'sudo docker stop  `sudo docker ps -aq --filter name=mysql1'+username.lower()+'`;sudo docker rm    `sudo docker ps -aq --filter name=mysql1`'
    try:
        a = os.system(command)
        print(a)
        return HttpResponse(a)
    except:
        return HttpResponse('error')

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功注销了")
    return redirect('/')


def userinfo(request):
    userinfo = {}
    print(123213)
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
        contect_dic = {}
        contect_dic['username'] = request.COOKIES['name']
        username = request.COOKIES['name']
        fuport = models.CSpringports.objects.filter(user=username)
        if (len(fuport) == 0):
            contect_dic['port'] = 'no'
        else:
            contect_dic['port'] = 'yes'
            contect_dic['sport'] = fuport[0].port
            contect_dic['mport'] = fuport[0].port+10000
    print(contect_dic)
    return render(request, 'userinfo.html', contect_dic)

def addport(request):
    if 'name' in request.COOKIES:
        username = request.COOKIES['name']
        con = {}
        con['name'] = username
        print(type(timezone.now()))
        fuport = models.CSpringports.objects.filter(user = username)
        if(len(fuport)==0):
            print("不存在添加端口")
            sp = models.CSpringports.objects.all()
            temps = list(sp)

            for i in temps:
                print(type(timedelta(hours = 1)))
                if timezone.now()-i.time  > timedelta(hours = 1):
                    print('yes')
                    models.CSpringports.objects.filter(id=i.id).update(user=username,time = timezone.now())
                    break
            #models.Springports.objects.create(user = user)
            #models.Mysqlports.objects.create(user=user)
            return render(request, 'sucport.html',con)
        else:
            print("已存在不添加")
            return render(request, 'sucport.html',con)


