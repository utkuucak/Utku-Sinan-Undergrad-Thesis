#!/bin/bash

# This script connects to VNC Server of Raspberry Pi.
# It takes the IP of Raspberry Pi as an argument.
# This script should only be run on PCs.

# Usage: sudo bash ./openrmdesktop.sh <ip>

clear
RPI_IP=$1

vncviewer $RPI_IP:5901

