#!/usr/bin/env bash

/usr/sbin/sshd -D
* * * * * python manage.py send_queued_mail >> send_mail.log 2>&1
