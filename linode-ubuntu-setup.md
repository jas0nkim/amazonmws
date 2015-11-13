# Linode Ubuntu (14.04) environment setup 


## Task / Application Server

##### IMPORTANT: minimum system memory 1gb

1. Adding a New User (Securing Your Server)

		https://www.linode.com/docs/security/securing-your-server
		
		./tools/deploy/securing_server.sh

1. install LAMP stack

		https://www.linode.com/docs/websites/lamp/how-to-install-a-lamp-stack-on-ubuntu-14-04

1. mysql create user and grant permissions

		CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
		GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
		FLUSH PRIVILEGES;

1. create ssh key

		ssh-keygen -t rsa -b 4096 -C "jason.kim.jiho@gmail.com"

1. copy public key into github

		cat ~/.ssh/id_rsa.pub

1. fetch source from repo to /applications directory and give user permission
		
		sudo chown jason:jason /applications
		
		sudo apt-get -y install git (* if necessary)
		git clone git@github.com:jas0nkim/amazonmws.git

1. softlink boto config file in /etc directory

		sudo ln -s /applications/amazonmws/amazonmws/.boto /etc/boto.cfg

1. install python-pip

		sudo apt-get -y install python-pip
	
1. install virtualenv and virtualenvwrapper 
	[http://chrisstrelioff.ws/sandbox/2014/09/04/virtualenv_and_virtualenvwrapper_on_ubuntu_14_04.html](http://chrisstrelioff.ws/sandbox/2014/09/04/virtualenv_and_virtualenvwrapper_on_ubuntu_14_04.html)

	
	- install virtualenv

			pip install --user virtualenv

	- install virtualenvwrapper

			pip install --user virtualenvwrapper

	- create /virtualenvs directory and give user permission

			sudo mkdir /virtualenvs
			sudo chown jason:jason /virtualenvs

	- append following lines in ~/.bashrc

			# where virtualenv bin file located
			if [ -d "$HOME/.local/bin" ] ; then
		  		PATH="$HOME/.local/bin:$PATH"
			fi
		
			# where to store our virtual envs
			export WORKON_HOME=/virtualenvs
			# where projects will reside
			export PROJECT_HOME=/applications
			# where is the virtualenvwrapper.sh
			source $HOME/.local/bin/virtualenvwrapper.sh

	- make changes active
	
			source ~/.bashrc
	
	- create new virtualenv
	
			mkvirtualenv amazonmws

1. install pip requirements.txt dependencies
	
		sudo apt-get -y install libmysqlclient-dev

		sudo apt-get -y install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev

		sudo apt-get -y install python-dateutil python-docutils python-feedparser python-gdata python-jinja2 python-ldap python-libxslt1 python-lxml python-mako python-mock python-openid python-psycopg2 python-psutil python-pybabel python-pychart python-pydot python-pyparsing python-reportlab python-simplejson python-tz python-unittest2 python-vatnumber python-vobject python-webdav python-werkzeug python-xlwt python-yaml python-zsi

		sudo apt-get -y install libffi-dev
		sudo apt-get -y install libxml2-dev libxslt1-dev
		sudo apt-get -y install libssl-dev
		sudo apt-get -y install libxml2-dev libxslt-dev

1. install dependencies for pip pyvirtualdisplay package (*skip this*)

		sudo apt-get -y install xvfb
		sudo apt-get -y install xserver-xephyr
		sudo apt-get -y install tightvncserver

1. install firefox (*skip this*)

		sudo apt-get -y install firefox
	
1. within /applications/amazonmws, pip install requirements

		pip install -r ./requirements.txt

1. apache setup for php soap and python restful servers
	- install wsgi for python applications

			sudo apt-get -y install libapache2-mod-wsgi

	- copy apache config files

			sudo cp /applications/amazonmws/install/apache/rest-intra.conf /etc/apache2/sites-available/
			sudo cp /applications/amazonmws/install/apache/soap-ebnl.conf /etc/apache2/sites-available/

			sudo a2ensite rest-intra.conf
			sudo a2ensite soap-ebnl.conf
			
1. *DEPRECATED* install mysql script files

		./init_db.sh

1. load mysql dump file

		mysql -u atewriteuser -p < /applications/amazonmws/tools/db_dump/xxxxxxxx-amazonmws.sql

1. install Oracle Java (JDK) 7 (*skip this for now, just for using remote WebDriver*)
		
		sudo apt-get -y install python-software-properties
		sudo add-apt-repository ppa:webupd8team/java
		sudo apt-get update
		sudo apt-get -y install oracle-java7-installer

1. run selenium server (*skip this for now, just for using remote WebDriver*)

		java -jar /path/to/project/selenium-server-standalone-2.47.1.jar

1. install phantomjs

	- step 1 - install apt-get packages

			sudo apt-get -y install build-essential g++ flex bison gperf ruby perl libsqlite3-dev libfontconfig1-dev libicu-dev libfreetype6 libssl-dev libpng-dev libjpeg-dev python libx11-dev libxext-dev
		
	- step 2 - install ttf-mscorefonts-installer

			echo "deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty multiverse \
			deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates multiverse \
			deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse" | sudo tee /etc/apt/sources.list.d/multiverse.list 
			
			sudo apt-get update && sudo apt-get upgrade
			sudo apt-get -y install ttf-mscorefonts-installer
	
	- get source from github repositiory, and build (**build time approx. 1 hour**)
			
			mkdir ~/opt
			cd ~/opt
			git clone git://github.com/ariya/phantomjs.git
			cd phantomjs
			git checkout 2.0
			./build.sh

	- register executable file

			sudo ln -s /home/jason/opt/phantomjs/bin/phantomjs /usr/local/bin/phantomjs

1. install/config Tor - ref: [https://www.torproject.org/docs/debian.html.en](https://www.torproject.org/docs/debian.html.en)

	- add following lines in /etc/apt/sources.list
		
			deb http://deb.torproject.org/torproject.org trusty main
			deb-src http://deb.torproject.org/torproject.org trusty main

	- run commands
 
			gpg --keyserver keys.gnupg.net --recv 886DDD89
			
				for vagrant run following instead (https://github.com/protobox/protobox/issues/159)
					gpg --keyserver hkp://pool.sks-keyservers.net --recv 886DDD89

			gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | sudo apt-key add -
			
			sudo apt-get update
			sudo apt-get install tor deb.torproject.org-keyring

	- set Tor password
			
			tor --hash-password my_password
			
	- config /etc/tor/torrc

			ControlPort 9051
			# hashed password below is obtained via `tor --hash-password my_password`
			
			HashedControlPassword 16:E600ADC1B52C80BB6022A0E999A7734571A451EB6AE50FED489B72E3DF
			CookieAuthentication 1
	
	- restart
			
			sudo /etc/init.d/tor restart


1. install/config privoxy

	- install
	
			sudo apt-get install privoxy

	- config /etc/privoxy/config (enable forward-socks5)

			listen-address  45.79.140.191:8118 # production (linode) only: specify ip address - line 761

			forward-socks5 / localhost:9050 . # line 1316
	
	- restart

			sudo /etc/init.d/privoxy restart

## Log Server - graylog2

##### IMPORTANT: minimum system memory 2gb

1. Adding a New User (Securing Your Server)

		https://www.linode.com/docs/security/securing-your-server
		
		./tools/deploy/securing_server.sh
		
1. install docker

		curl -sSL https://get.docker.com/ | sh

1. create a user for docker

		sudo usermod -aG docker jason

1. pull graylog docker container

		sudo docker pull graylog2/allinone

1. create directories for store graylog data and log, and set directory ownership
		
		sudo mkdir /graylog
		sudo chown jason:jason /graylog
		
1. run graylog docker container

		sudo docker run -t -p 9000:9000 -p 12201:12201 -p 12201:12201/udp -e GRAYLOG_PASSWORD=20itsit15 -e GRAYLOG_USERNAME=ateadmin -v /graylog/data:/var/opt/graylog/data -v /graylog/logs:/var/opt/graylog graylog2/allinone
