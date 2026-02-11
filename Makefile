install:
	poetry install

project:
	poetry run database

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	powershell -c "pip install (Get-ChildItem dist\*.whl | Select -First 1)"

make lint:
	poetry run ruff check .
