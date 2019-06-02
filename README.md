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
Yt2G9d4aGMrRgwhm
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
cd /distelli/envs/SoSI-CICD-Env/backend/stockLogic/
export PYTHONPATH=.:/distelli/envs/SoSI-CICD-Env/backend/:/usr/src/Python-3.7.2/:
localectl set-locale LANG=pt_BR.utf8
python3.7 buynhold.py 


