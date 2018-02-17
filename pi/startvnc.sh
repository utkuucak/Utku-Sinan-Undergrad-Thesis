#!/bin/bash

# This script opens a VNC remote desktop server on Raspberry Pi
# This script should be run on Raspberry Pi Terminal

clear
vncserver :1 -geometry 1024x600 -depth 16 -pixelformat rgb565
