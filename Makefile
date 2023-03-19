install_deps :
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	sudo apt-get install espeak
	sudo apt-get install mbrola-de7
