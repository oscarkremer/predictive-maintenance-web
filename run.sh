PATH=$PATH:/home/oscarkremer/miniconda3/bin
cd /home/oscarkremer/predictive-maintenance-ifsul
source activate
conda activate predictive-maintenance-ifsul
make webserver gunicorn dashapp:app -b 0.0.0.0:5000
