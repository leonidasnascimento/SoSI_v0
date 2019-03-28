# SoSI
(S)ystem (o)f (S)tock (I)nformation is a system used to gather brazilian stocks information, consolidating them into an unique place.

# Troubleshooting
https://blog.remontti.com.br/2054
https://unix.stackexchange.com/a/446749
https://hostpresto.com/community/tutorials/how-to-connect-to-a-remote-mysql-server-via-an-ssh-tunnel/
https://www.linode.com/community/questions/7934/cant-log-in-to-ssh-via-putty
https://hostpresto.com/community/tutorials/how-to-connect-to-a-remote-mysql-server-via-an-ssh-tunnel/

# Hash
Yt2G9d4aGMrRgwhm
sosiuser|4S86yySdBpLgcVKT

# Befor Running
export PYTHONPATH=.:/var/www/git/sosi/backend/:/usr/src/Python-3.7.2/:
sed -i 's/^# *\(pt_BR.UTF-8\)/\1/' /etc/locale.gen && locale-gen
python3.7 backend/stockLogic/buynhold.py 

