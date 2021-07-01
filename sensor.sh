#!/bin/bash

PATH=$PATH:/home/oscar/anaconda3/bin
cd /home/oscar/predictive-maintenance-web
source activate
conda activate predictive-maintenance-ifsul
make sensor
