== Make a new user

useradd smt
cd /home
mkdir smt
chown smt:smt smt


== Install python3, pip3, virtualenv

apt-get install python3 python3-pip
pip3 install virtualenv


== Install SMT

su smt
cd ~
git clone https://github.com/psygnisfive/noisebridge-social-media-tool
cd noisebridge-social-media-tool

# add secrets.py by whatever means necessary


== Create a virtual environment and install requirements

virtualenv venv
source venv/bin/activate
  -- now inside venv
  pip install -r requirements.txt


== Install production server crap

pip install gunicorn
@TODO: @r should commit wsgi.py

== Setup caddy or other frontend webserver
mkdir caddy && cd caddy
wget 'https://github.com/mholt/caddy/releases/download/v0.11.0/caddy_v0.11.0_linux_amd64.tar.gz'
tar xf caddy_*
cp caddy /usr/local/bin
chown root:root /usr/local/bin/caddy
chmod 755 /usr/local/bin/caddy
apt-get install libcap2-bin
setcap 'cap_net_bind_service=+ep' /usr/local/bin/caddy
mkdir /etc/caddy
# put your Caddyfile in /etc/caddy/Caddyfile
chown -R root:www-data /etc/caddy
mkdir /etc/ssl/caddy
chown -R root:www-data /etc/ssl/caddy
chmod 0770 /etc/ssl/caddy
cp init/linux-systemd/caddy.service /etc/systemd/system/
chown root:root /etc/systemd/system/caddy.service
chmod 644 /etc/systemd/system/caddy.service
systemctl daemon-reload
systemctl enable caddy
systemctl start caddy

== Note: example caddyfile

gothdyke.mom, www.gothdyke.mom {
    tls tls@gothdyke.mom
    proxy /nb/smt localhost:3116 {
        without /nb/smt
    }
}

== Run production server

source venv/bin/activate
  -- now inside venv
  gunicorn --bind 127.0.0.1:3116 wsgi

== Start the development server

source venv/bin/activate
  -- now inside venv
  python slack_integration.py
