#FastAPI do zero com o Dunossauro o brabo! 

pip install --user pipx
pipx install poetry 
pipx inject poetry poetry-plugin-shell
poetry python install 3.13
poetry new --flat fastapi_zero
poetry env use 3.13
poetry install
poetry add 'fastapi[standard]'
poetry shell
fastapi dev fast_zero/app.py
poetry add --group dev pytest pytest-cov taskipy ruff