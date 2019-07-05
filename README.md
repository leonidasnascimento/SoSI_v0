# SoSI
(S)ystem (o)f (S)tock (I)nformation is a system used to gather brazilian stocks information, consolidating them into an unique place.

# Troubleshooting
https://blog.remontti.com.br/2054
https://unix.stackexchange.com/a/446749
https://hostpresto.com/community/tutorials/how-to-connect-to-a-remote-mysql-server-via-an-ssh-tunnel/
https://www.linode.com/community/questions/7934/cant-log-in-to-ssh-via-putty
https://hostpresto.com/community/tutorials/how-to-connect-to-a-remote-mysql-server-via-an-ssh-tunnel/
https://rewry.blogspot.com/2011/10/desabilitando-o-case-sensitive-do-mysql.html

# Hash
root|Yt2G9d4aGMrRgwhm|sosidb
sosiuser|4S86yySdBpLgcVKT

#################
# Befor Running #
#################

## Local Machine
cd /root/
export PYTHONPATH=.:/var/www/git/sosi/backend/:/usr/src/Python-3.7.2/:
localectl set-locale LANG=pt_BR.utf8
python3.7 /var/www/git/sosi/backend/stockLogic/buynhold.py 

## Pipeline (DevOps) environment
#### Pre Install
sudo dpkg --configure -a
#### Pos Install
sudo apt-get install build-essential checkinstall --assume-yes
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev --assume-yes
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
sudo tar xzf Python-3.7.3.tgz
cd Python-3.7.3
sudo ./configure --enable-optimizations
sudo make altinstall
#### Exec
cd /distelli/envs/SoSI-CICD-Env/backend/stockLogic
export PYTHONPATH=".:/distelli/envs/SoSI-CICD-Env/backend/:/usr/local/lib/python3.7:/usr/local/:/usr/local/bin/"
export PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin"
localectl set-locale LANG=pt_BR.utf8
echo $PYTHONPATH
echo $PATH
python3.7 buynhold.py 
