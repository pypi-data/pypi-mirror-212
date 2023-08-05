#!/bin/sh
# eMews host node launch template
# node.name is the name of the host as given in the CORE gui
export PYTHONPATH=${emews_pkg_path}
python3 -m emews -n ${node.name} host 1>> emews_node_host.log 2>&1