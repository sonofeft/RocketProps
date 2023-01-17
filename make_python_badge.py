import os
import anybadge

with open('setup.py', 'r') as fInp:
    sL = fInp.readlines()

pyL = [] # list of python versions
for s in sL:
    s = s.strip()
    if s.find('Programming Language :: Python') > 0:
        lL = s.split(' ')
        pyL.append( lL[-1][:-2] )

print( pyL )
version_text = '|'.join(pyL)
print( version_text )

badge = anybadge.Badge(label='python', value=version_text, default_color='#0F80C1')

here = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join( here, 'docs', '_static', 'python_version_badge.svg')

badge.write_badge( file_path, overwrite=True )
print( 'wrote badge to:', file_path)