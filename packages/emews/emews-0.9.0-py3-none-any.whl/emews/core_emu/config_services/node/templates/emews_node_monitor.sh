#!/bin/sh
# eMews monitor node launch template
# node.name is the name of the node as given in the CORE gui
# use 'tail -f emews_node_monitor.log' to view the log in real-time
export PYTHONPATH=${emews_pkg_path}
sleep ${config['emews_start_delay']}
python3 -m emews -n ${node.name}-monitor monitor 1>> emews_node_monitor.log 2>&1