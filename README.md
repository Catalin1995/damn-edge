```
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install virtualenv nginx build-essential python3-dev
```

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
