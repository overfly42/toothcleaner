install_deps :
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	sudo apt-get install espeak
	sudo apt-get install mbrola-de7
#https://howtoraspberrypi.com/make-talk-raspberry-pi-espeak/
install : 
	sed "s|<PATH>|$$(pwd)/toothcleaner.service|g" toothcleaner.template > /etc/systemd/system/toothcleaner.service
	systemctl daemon-reload
	systemctl enable toothcleaner.service
	systemctl start toothcleaner.service