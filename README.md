https://drive.google.com/drive/folders/1r6nmAlrYXFlUtIjO5C_xPLPDvWJjBziC?hl=ru

взяла с kaggle https://www.kaggle.com/datasets/uom190346a/global-coffee-health-dataset/data

Для работы с данными надо настроить окружение. Для этого устанавливаем condamini и в терминале вводим:

conda create -n my_env python=3.13 pip
conda activate my_env

pip install poetry
pip install pandas
poetry new my_project

cd my_project
poetry add jupyterlab pandas matplotlib wget
poetry add click
