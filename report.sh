#!/bin/bash

PATH=$PATH:/home/oscarkremer/anaconda3/bin
cd /home/oscarkremer/predictive-maintenance-ifsul
source activate
conda activate predictive-maintenance-ifsul
make report
