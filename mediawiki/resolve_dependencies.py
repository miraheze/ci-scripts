# A script to resolve dependencies of MediaWiki extension for Quibble test

from os import environ
# pf for https://raw.githubusercontent.com/wikimedia/integration-config/master/zuul/parameter_functions.py
from pf import dependencies, get_dependencies

if 'MEDIAWIKI_VERSION' in environ and environ['MEDIAWIKI_VERSION'] == 'REL1_35':
  dependencies['EventLogging'].remove('EventBus')

# Add dependencies of target extension
dependencies['ext'] = open('dependencies').read().splitlines()

# Resolve
resolvedDependencies = []
for d in get_dependencies('ext', dependencies):
  # Skip parsoid which is a virtual extension
  if d == 'parsoid':
    continue
  d = 'mediawiki/extensions/' + d
  d = d.replace('/extensions/skins/', '/skins/')
  resolvedDependencies.append(d)
print(' '.join(resolvedDependencies))
