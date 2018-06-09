#!/bin/sh -x

usage() {
    echo "Usage: $0 <host>"
    exit 1
}

if [ $# -ge 1 ]; then
    host=$1
else
    usage
fi

sshpass -p 'bsn' ssh -o StrictHostKeyChecking=no recovery@$host 'sudo mkdir -p ~admin/.ssh && sudo bash -c "cat >> ~admin/.ssh/authorized_keys" && sudo chown -R admin:admin ~admin/.ssh' < /home/admin/.ssh/id_rsa.pub

