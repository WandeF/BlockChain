#!/bin/bash

# 更新 apt
sudo apt update

# 安装必要的包
sudo apt install -y python3 python3-pip

# 安装您的项目
sudo python3 -m pip install -e .


printf "\nInstallation finished.\n"
exit 0;
