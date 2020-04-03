PATH=$PATH:/home/oscarkremer/miniconda3/bin
cd /home/oscarkremer/predictive-maintenance
source activate
conda activate predictive-maintenance
make webserver gunicorn dashapp:app -b 0.0.0.0:5000
