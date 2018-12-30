PACKAGE = tomate-notify-plugin
AUTHOR = eliostvs
PACKAGE_ROOT = $(CURDIR)
TOMATE_PATH = $(PACKAGE_ROOT)/tomate
DATA_PATH = $(PACKAGE_ROOT)/data
PLUGIN_PATH = $(DATA_PATH)/plugins
PYTHONPATH = PYTHONPATH=$(TOMATE_PATH):$(PLUGIN_PATH)
DOCKER_IMAGE_NAME = $(AUTHOR)/tomate
PROJECT = home:eliostvs:tomate
OBS_API_URL = https://api.opensuse.org/trigger/runservice
WORK_DIR = /code

submodule:
	git submodule init;
	git submodule update;

clean:
	find . \( -iname "*.pyc" -o -iname "__pycache__" \) -print0 | xargs -0 rm -rf
	rm -rf *.egg-info/ .coverage build/ .cache .eggs

test: clean
	$(PYTHONPATH) py.test test_plugin.py --cov=$(PLUGIN_PATH)

docker-clean:
	docker rmi $(DOCKER_IMAGE_NAME) 2> /dev/null || echo $(DOCKER_IMAGE_NAME) not found!

docker-pull:
	docker pull $(DOCKER_IMAGE_NAME)

docker-test:
	docker run --rm -v $(PACKAGE_ROOT):$(WORK_DIR) --workdir $(WORK_DIR) $(DOCKER_IMAGE_NAME)

docker-all: docker-clean docker-pull docker-test

docker-enter:
	docker run --rm -v $(PACKAGE_ROOT):$(WORK_DIR) --workdir $(WORK_DIR) -it --entrypoint="bash" $(DOCKER_IMAGE_NAME)

release-%:
	grep -q '\[Unreleased\]' || echo 'Create the [Unreleased] section in the changelog first!'
	bumpversion --verbose --commit $*
	git flow release start $(CURRENT_VERSION)
	git flow release finish -p $(CURRENT_VERSION)
	git push --tags

trigger-build:
	curl -X POST -H "Authorization: Token $(TOKEN)" $(OBS_API_URL)
