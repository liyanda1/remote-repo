#!safe_shell
rm /tmp/oldfile.txt
mkdir /tmp/testdir user:group 755
cp /etc/hosts /tmp/testdir/hosts_copy
json /tmp/test.json setcurrent status 0

