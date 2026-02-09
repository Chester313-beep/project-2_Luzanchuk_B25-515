install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	powershell -c "pip install (Get-ChildItem dist\*.whl | Select -First 1)"
