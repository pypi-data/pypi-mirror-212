#!/bin/sh
# eMews hub node launch template
# node.name is the name of the hub as given in the CORE gui
export PYTHONPATH=${emews_pkg_path}
python3 -m emews -n ${node.name} hub 1>> emews_node_hub.log 2>&1