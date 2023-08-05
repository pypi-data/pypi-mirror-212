rm dist/*

python3 -m build

# install locall:
# pip install -e .

# publish to pypi test:
# python -m twine upload -r testypi dist/*

# publish to real pypi:
# python -m twine upload dist/*
