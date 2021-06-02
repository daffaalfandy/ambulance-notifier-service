# Ambulance Notifier RESTful API

This application is backend service for serving [Ambulance Notifier App](https://gitlab.com/musthofaammar/ambulance-notifier), capstone project for BANGKIT 2021.  
This service was built using Flask.

## Installing application

**Make sure using Python 3.9.\***

- First download or clone this repository.

```
git clone https://github.com/daffaalfandy/ambulance-notifier-service.git
curl -LO https://github.com/daffaalfandy/ambulance-notifier-service/archive/refs/heads/main.zip
```

- Instal required dependency.

```
cd [application_directory]
```

> If you have create virtual environment

```
pip install -r requirements.txt
```

> Else

```
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Create and import database. **SQL**

  > Create database with your desired name.  
  > Import table from ambulance_notifier.sql.

- Make copy env file.

```
cp env .env
```

> Please customize .env file match with the machine environment.

- Run the application.

```
python app.py
```

**Deploying Application**
For deployment please refer from this [Article](https://dev.to/brandonwallace/deploy-flask-the-easy-way-with-gunicorn-and-nginx-jgc)

> Change ExecStart in systemd config to this command

```
ExecStart=[Absolute path to your gunicorn package] -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --threads 100 --bind 127.0.0.1:5000 app:app
```

> Change nginx config to

```
server {
        listen 80;
        server_name 34.101.69.158 api.nitiscreative.com;

        access_log [your_access_log_path]
        error_log [your_error_log_path];

        location / {
                include proxy_params;                ambulance-notifier-service-main/ambulance-notifier.sock;
                proxy_pass http://127.0.0.1:5000;
        }
        location /socket.io {
                include proxy_params;
                proxy_http_version 1.1;
                proxy_buffering off;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_pass http://127.0.0.1:5000;
        }
}
```

## Endpoint Documentation

Please refer to this [Documentation](https://github.com/daffaalfandy/ambulance-notifier-service/blob/main/documentation.md).

## Credits

Thanks to:

- [Nanditya Nuswatama](https://github.com/NandityaNuswatama) as Designer and Mobile Developer.
- [Ammar](https://github.com/musthofaammar) as Mobile Developer.
- [Nicholas Nanda](), and [Emanuella Wintari](https://github.com/Imanuella74/) as Machine Learning Engineer.
- [Natalia Syafitri](https://www.linkedin.com/in/natalia-syafitri-kustanto/) as as non technical team member.
