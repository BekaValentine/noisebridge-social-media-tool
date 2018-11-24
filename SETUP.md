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


== Install production server

pip install gunicorn

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
gunicorn --bind 127.0.0.1:3116 slack_integration

== Start the development server

source venv/bin/activate
python slack_integration.py

== Run a service

Use the noisebridge-social-media-tool.sh script, which wraps up the production server commands, to make a service. In systemd systems:

==== Making a Systemd service

PREREQUISITE:

${SCRIPT_FILE}
${SERVICE_NAME}
${SERVICE_DESCRIPTION}

1. Copy the script to /usr/bin and make it executable:

  sudo cp ${SCRIPT_FILE} /usr/bin/${SCRIPT_FILE}
  sudo chmod +x /usr/bin/${SCRIPT_FILE}

2. Create a Unit file to define a systemd service at the location
/lib/systemd/system/${SERVICE_NAME}.service, containing the following info:

  [Unit]
  Description=${SERVICE_DESCRIPTION}

  [Service]
  Type=simple
  ExecStart=/bin/bash /usr/bin/${SCRIPT_FILE}

  [Install]
  WantedBy=multi-user.target

3. Enable the service:

  sudo systemctl enable ${SERVICE_NAME}

4. Run the service:

  sudo systemctl start ${SERVICE_NAME}
