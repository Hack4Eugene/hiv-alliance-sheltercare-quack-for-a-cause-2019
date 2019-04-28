# preflight.sh
#!/usr/bin/bash

# Verify valid usage
if [ "$#" -ne "1" ]
then
    echo "Usage: ./preflight.sh <appname>"
    echo "<appname> is either HIVA, CARE, or DELETE"
    exit;
fi

# Remove previous app
if [ -d DeployFlaskApp ]
then 
    rm -R DeployFlaskApp
fi

export FLASK_APP=flask_app.py

if [ $1 == "HIVA" ]
then
	# Copy app from DevHIVAllianceApp folder to deployment folder
	cp -R DevHIVAllianceApp DeployFlaskApp
	cd DeployFlaskApp
	python3 -m flask run
	exit;
fi

if [ $1 == "CARE" ]
then
    # Copy app from DevShelterCareApp folder to deployment folder
	cp -R DevShelterCareApp DeployFlaskApp
	cd DeployFlaskApp
	python3 -m flask run
	exit;
fi

if [ $1 == "DELETE" ]
then
    exit;
fi
