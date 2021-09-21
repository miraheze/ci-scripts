# A script to resolve dependencies of MediaWiki extension for Quibble test
import yaml

from os import environ
# pf for https://raw.githubusercontent.com/wikimedia/integration-config/master/zuul/parameter_functions.py
from pf import dependencies, get_dependencies

if 'MEDIAWIKI_VERSION' in environ and environ['MEDIAWIKI_VERSION'] == 'REL1_35':
  dependencies['EventLogging'].remove('EventBus')

# Add dependencies of target extension
with open('dependencies.yaml', 'r') as f:
    dependencies['ext'] = yaml.load(f)

# Resolve
resolvedDependencies = []
for d in get_dependencies('ext', dependencies):
  # Skip parsoid which is a virtual extension
  if d == 'parsoid':
    continue
  d = 'mediawiki/extensions/' + d
  d = d.replace('/extensions/skins/', '/skins/')
  resolvedDependencies.append(d)
print(' '.join(resolvedDependencies).'[branch]='.get_dependencies('ext', dependencies)['branch'])
