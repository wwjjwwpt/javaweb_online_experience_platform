# javaweb_online_experience_platform
Run And Edite JavaWeb online
===
# 部署环境
18.04.4 LTS (GNU/Linux 4.15.0-112-generic x86_64)</br>
Docker version 19.03.12</br>
Python 3.6.9</br>
Django 2.0</br>
java11</br>
maven 3.5.3</br>

# 安装docker
```
sudo apt-get update
#安装
sudo apt-get install apt-transport-https
sudo apt-get install ca-certificates
sudo apt-get install curl
sudo apt-get install software-properties-common
#安装docker/添加密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get install docker-ce
#测试
sudo docker run hello-world
```

# 部署实验空间和Dockerfile
```
git clone git@github.com:wwjjwwpt/javaspring_docekr.git #部署空间
```
修改view中文件位置，可调整Dockerfile中的配置

# 运行django
```
sudo nuhuo python3 manage runserver 0.0.0.0:8080 &
```

# 主平台部署
```
git clone git@github.com:wwjjwwpt/javaspring_platform.git
cd javaspring_platform
sudo nuhup python3 manage.py runserver 0.0.0.0:8000 &
```
