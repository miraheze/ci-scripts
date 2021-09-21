# A script to resolve dependencies of MediaWiki extension for Quibble test
import yaml

from os import environ
# pf for https://raw.githubusercontent.com/wikimedia/integration-config/master/zuul/parameter_functions.py
from pf import dependencies, get_dependencies

if 'MEDIAWIKI_VERSION' in environ and environ['MEDIAWIKI_VERSION'] == 'REL1_35':
  dependencies['EventLogging'].remove('EventBus')

# Add dependencies of target extension
with open('dependencies', 'r') as f:
    dependencies['ext'] = yaml.load(f, Loader=yaml.FullLoader)

# Resolve
resolvedDependencies = []
for d in get_dependencies('ext', dependencies):
  repo = ''
  branch = ''
  if 'repo' in dependencies['ext'][d]:
    if dependencies['ext'][d]['repo'] not in ('auto','default'):
      repo = '|' + dependencies['ext'][d]['repo']
    if 'branch' in dependencies['ext'][d]:
      if dependencies['ext'][d]['branch'] not in ('auto','default'):
        branch = '|' + dependencies['ext'][d]['branch']

  # Skip parsoid which is a virtual extension
  if d == 'parsoid':
    continue
  d = 'mediawiki/extensions/' + d
  d = d.replace('/extensions/skins/', '/skins/')
  d = d + repo + branch
  resolvedDependencies.append(d)
print(' '.join(resolvedDependencies))
