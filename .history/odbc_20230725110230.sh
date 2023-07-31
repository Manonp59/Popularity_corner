curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

ln -s /usr/lib64/libodbcinst.so.2 /lib/x86_64-linux-gnu/libodbcinst.so.2
ln -s /usr/lib64/libodbc.so.2 /lib/x86_64-linux-gnu/libodbc.so.2

apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
apt-get install -y unixodbc-dev
