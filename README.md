# javaweb_online_experience_platform
Run And Edite JavaWeb online
===
# 部署环境
18.04.4 LTS (GNU/Linux 4.15.0-112-generic x86_64)</br>
Docker version 19.03.12</br>
Python 3.6.9</br>
Django 2.0</br>

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
