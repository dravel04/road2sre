#!/bin/bash
set -eou pipefail

sudo /etc/init.d/rundeckd start
tail -f $RUNDECK_LOG/service.log