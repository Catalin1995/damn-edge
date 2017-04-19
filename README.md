```
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install virtualenv nginx build-essential python3-pip python3-dev nginx
sudo pip3 install virtualenv
```

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
