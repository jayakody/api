#!/bin/sh

usage() {
    echo "Usage: $0 <host>"
    exit 1
}

if [ $# -ge 1 ]; then
    host=$1
else
    usage
fi

sshpass -p 'bsn' ssh -o StrictHostKeyChecking=no bsn@$host 'mkdir -p .ssh && cat >>.ssh/authorized_keys' < /home/admin/.ssh/id_rsa.pub

