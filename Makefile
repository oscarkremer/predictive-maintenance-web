
#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = predictive-maintenance-ifsul
PROFILE = default
PROJECT_NAME := predictive-maintenance-ifsul
PYTHON_INTERPRETER := python3
START_POINT= 0
END_POINT= 90


################################################################################
# COMMANDS                                                                     #
# TO SHOW OUTPUT USE LOGGER=stdout                                             #
################################################################################


setup: check_environment
	@echo "---> Running setup.."
	@conda env create -f environment.yml
	@make dirs
	@cp -n .env.example .env
	@echo "---> To complete setup please run \n---> source activate predictive-maintenance-ifsul"


dirs:
	@echo "---> Creating data dirs"
	@mkdir -p data/predicted/prediction
	@mkdir -p data/predicted/evaluation
	@mkdir -p data/predicted/subtraction
	@mkdir -p data/processed
	@mkdir -p data/testing/predicted
	@mkdir -p data/testing/processed
	@mkdir -p data/binary/models
	@mkdir -p data/logs
	@mkdir -p data/plots/evaluation
	@mkdir -p data/plots/prediction
	@mkdir -p data/plots/subtraction
	@echo "---> Done"

install:
	@echo "---> Installing dependencies"
	@conda env update -f environment.yml

download: dirs
	@echo "---> Updating raw data from S3"
	@echo "---> It will take about 5 minutes.."
	aws s3 cp s3://des-forecast/poc.csv data/raw/ 

pipeline:
	@(yes | make download features predict)


clean:
	@echo "---> Cleaning environment.."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -path '*/.ipynb_checkpoints/*' -delete
	@find . -type d -name ".ipynb_checkpoints" -empty -delete


lint:
	@echo "---> Processing lint.."
	@flake8 src


autocorrect:
	@echo "---> Processing autocorrect"
	@autopep8 --in-place --aggressive --aggressive --global-config .flake8 $(shell find . -name '*.py')

console:
	@$(PYTHON_INTERPRETER)

logs:
	@tail -n 50 -f data/logs/output.log

check_environment:
	@echo "---> Checking environment.."
	@python3 test_environment.py

webserver:
	@echo "---> Running Webserver.."
	@gunicorn app:app -b 0.0.0.0:5000
