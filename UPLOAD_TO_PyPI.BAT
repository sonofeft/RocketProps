python setup.py sdist bdist_wheel

C:\Python310\Scripts\twine.exe  upload --skip-existing dist/* --config-file "%HOMEPATh%\.pypirc"

rem use:  twine check dist/*  OR twine check dist/*24.tar.gz (where: 24 is current version)


