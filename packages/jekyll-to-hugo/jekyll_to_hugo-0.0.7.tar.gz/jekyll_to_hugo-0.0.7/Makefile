# Formats the code
format:
	autoflake --exclude venv -ri . && black . && isort -r .
# Run tests
test:
	pytest .
# Build package
build:
	python -m build
# Upload package to PyPI
upload:
	hatch publish
release:
	hatch clean && hatch build && hatch publish
# Build the tox docker image, use docker run -v "$(pwd)":"/code" jekyll-to-hugo-tox -e ci to run tox
build-tox:
	docker build . -f ./docker/Tox.Dockerfile -t jekyll-to-hugo-tox