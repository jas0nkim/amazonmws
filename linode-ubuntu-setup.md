# Linode Ubuntu (14.04) environment setup 


## Task / Application Server

##### IMPORTANT: minimum system memory 1gb

1. Adding a New User (Securing Your Server)

		https://www.linode.com/docs/security/securing-your-server


2. install LAMP stack

		https://www.linode.com/docs/websites/lamp/how-to-install-a-lamp-stack-on-ubuntu-14-04


2. install pip requirements.txt dependencies

		sudo apt-get install libmysqlclient-dev


2. install more pip requirements.txt dependencies (* skip at first, and come back if ended up with pip installing error)

		sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev

		sudo apt-get install python-dateutil python-docutils python-feedparser python-gdata python-jinja2 python-ldap python-libxslt1 python-lxml python-mako python-mock python-openid python-psycopg2 python-psutil python-pybabel python-pychart python-pydot python-pyparsing python-reportlab python-simplejson python-tz python-unittest2 python-vatnumber python-vobject python-webdav python-werkzeug python-xlwt python-yaml python-zsi

		sudo apt-get install libffi-dev
		sudo apt-get install libxml2-dev libxslt1-dev
		sudo apt-get install libssl-dev
		sudo apt-get install libxml2-dev libxslt-dev


2. install dependencies for pip pyvirtualdisplay package

		sudo apt-get install xvfb
		sudo apt-get install xserver-xephyr
		sudo apt-get install tightvncserver


2. install firefox

		sudo apt-get install firefox


3. create ssh key

		ssh-keygen -t rsa -b 4096 -C "jason.kim.jiho@gmail.com"


4. copy public key into github

		cat ~/.ssh/id_rsa.pub


5. fetch source from repo to /Applications directory and give user permission

		git clone git@github.com:jas0nkim/amazonmws.git
		sudo chown user:user /applications


6. install python-pip

		sudo apt-get install python-pip
	
		http://chrisstrelioff.ws/sandbox/2014/09/04/virtualenv_and_virtualenvwrapper_on_ubuntu_14_04.html


7. install virtualenv

		pip install --user virtualenv


8. install virtualenvwrapper

		pip install --user virtualenvwrapper


9. create /virtualenvs directory and give user permission

		sudo chown group:user /virtualenvs


10. append following lines in ~/.bashrc

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


11. make changes active

		source ~/.bashrc


12. create new virtualenv

		mkvirtualenv amazonmws


13. within /applications/amazonmws, pip install requirements

	pip install -r ./requirements.txt


14. mysql create user and grant permissions

		CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
		GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
		FLUSH PRIVILEGES;


15. install mysql script files

		./init_db.sh


## Log Server - graylog2

##### IMPORTANT: minimum system memory 2gb

1. Adding a New User (Securing Your Server)

		https://www.linode.com/docs/security/securing-your-server


1. install docker

		curl -sSL https://get.docker.com/ | sh


1. create a user for docker

		sudo usermod -aG docker vagrant


1. pull graylog docker container

		docker pull graylog2/allinone


1. create directories for store graylog data and log, and set directory ownership
		
		sudo mkdir /var/opt/graylog
		sudo chown vagrant:vagrant /var/opt/graylog
		mkdir /var/opt/graylog/data
		mkdir /var/opt/graylog/logs
		

1. run graylog docker container

		docker run -t -p 9000:9000 -p 12201:12201 -e GRAYLOG_PASSWORD=20itsit15 -e GRAYLOG_USERNAME=ateadmin -v /graylog/data:/var/opt/graylog/data -v /graylog/logs:/var/opt/graylog/logs graylog2/allinone
