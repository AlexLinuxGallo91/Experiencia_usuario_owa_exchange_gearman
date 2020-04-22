##############################################################################################
##                                                                                          ##
##              INSTALACION DE DEPENDENCIAS NECESARIAS EN DISTRIBUCION CENTOS               ##
##                                                                                          ##
##############################################################################################
#!/bin/bash
# actualizacion de dependencias del SO
echo 'Actualizando distro'
sudo yum update

# instalacion de python y pip (en su version 3)
echo 'Instalando python3 - pip3'
sudo yum install -y python3
sudo yum install -y python3-pip

# se instalan las librerias/modulos necesarios de python
echo 'Instalando dependencias python3'
sudo pip3 install --upgrade --ignore-installed urllib3
sudo pip3 install selenium
sudo pip3 install python3-gearman

# instalacion de Nano
sudo yum install -y nano

# instalacion de git 
echo 'Instalando git'
sudo yum install -y git

# instalacion de wget
echo 'Instalando wget'
sudo yum install -y wget

# instalacion unzip
echo 'Instalando unzip'
sudo yum install -y unzip

# se crea el dir webdrivers y se instalaran los webdrivers necesarios
echo 'Creando dir usr/bin/webdrivers'
sudo mkdir /usr/bin/webdrivers
cd /usr/bin/webdrivers

# se descarga cada uno de los webdrivers dentro del directorio usr/bin/webdrivers
# geckodriver
echo 'Instalando geckodriver'
sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
sudo tar -xf geckodriver-v0.26.0-linux64.tar.gz
sudo rm -fr geckodriver-v0.26.0-linux64.tar.gz

# chromedriver
echo 'Instalando chromedriver'
sudo wget https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip
sudo unzip chromedriver_linux64.zip
sudo rm -fr chromedriver_linux64.zip

# se descarga e instala cada uno de los navegador web a utilizar
# firefox
echo 'Instalando navegador firefox'
cd ~
wget https://ftp.mozilla.org/pub/firefox/releases/64.0/linux-x86_64/en-US/firefox-64.0.tar.bz2
tar xjf firefox-64.0.tar.bz2
sudo rm -fr firefox-64.0.tar.bz2
sudo mv firefox /usr/local/firefox-64.0
sudo ln -s /usr/local/firefox-64.0/firefox /usr/local/bin/firefox
sudo yum install -y Xvfb 
sudo yum -y groupinstall "X Window System" "Desktop" "Fonts" "General Purpose Desktop"
sudo yum -y install gtk3-devel

# chrome (chromium)
echo 'Instalando navegador chrome (chromium)'
sudo yum install -y epel-release
sudo yum install -y chromium

# phantomjs
echo 'Instalando navegador phantomjs'
sudo yum install -y glibc fontconfig freetype freetype-devel fontconfig-devel wget bzip2
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2
sudo rm -fr phantomjs-2.1.1-linux-x86_64.tar.bz2
sudo mv phantomjs-2.1.1-linux-x86_64 /opt/phantomjs-2.1.1-linux-x86_64
sudo ln -sf /opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs
