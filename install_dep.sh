#!/bin/zsh

INSTDIR="$( cd "$( dirname "${(%):-%N}" )" && pwd )"
echo $INSTDIR

SOURCEDIR="$(dirname "$INSTDIR")"
echo $SOURCEDIR

cd /opt

# Create and activate virtual environment
python3.11 -m venv SumTrackerEnv
source SumTrackerEnv/bin/activate

# Change ownership of the virtual environment to the current user
sudo chown -R $USER:$USER /opt/SumTrackerEnv/

cd $INSTDIR
echo "Virtual environment (SumTrackerEnv) has been created."
echo ""
echo "Installing the Python dependencies"
pip install --upgrade pip
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

echo ""
echo "All Python dependencies have been installed"
chmod +x run_server.sh
./run_server.sh
