#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt install apache2 -y
sudo ufw allow in "Apache Full"
sudo apt install mariadb-server -y
sudo mysql_secure_installation
#sudo apt -y install lsb-release ca-certificates apt-transport-https software-properties-common
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update
sudo apt-get remove --purge php8.3-* -y
sudo apt install php8.2 php8.2-bcmath php8.2-intl php8.2-soap php8.2-zip php8.2-gd php8.2-curl php8.2-cli php8.2-xml php8.2-xmlrpc php8.2-gmp php8.2-common php8.2-mysqli php8.2-mbstring -y
sudo a2dismod php8.3
sudo a2enmod proxy_cfgi setenvif
sudo a2enconf php8.2
sudo systemctl reload apache2
sudo update-alternatives --set php /usr/bin/php8.2
sudo apt install wget -y
sudo apt install unzip -y
sudo apt install phpmyadmin -y
sudo rm -rf /usr/share/phpmyadmin/*
sudo wget https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.tar.gz
sudo tar xvf phpMyAdmin-5.2.1-all-languages.tar.gz -C /usr/share/phpmyadmin --strip-components=1
sudo chown -R www-data:www-data /usr/share/phpmyadmin
sudo systemctl restart apache2
if ! grep -q "Include /etc/phpmyadmin/apache.conf" /etc/apache2/apache2.conf; then
    echo "Include /etc/phpmyadmin/apache.conf" | sudo tee -a /etc/apache2/apache2.conf > /dev/null
    sudo systemctl restart apache2
fi

