# A script to resolve dependencies of MediaWiki extension for Quibble test
import os
import sys
import yaml

# pf for https://raw.githubusercontent.com/wikimedia/integration-config/master/zuul/parameter_functions.py
from pf import dependencies, get_dependencies

# Get dependency file path from argument
dependencies_file = sys.argv[1]

recurse = True  # Default to recursion
if len(sys.argv) >= 3 and sys.argv[2] == '--no-recurse':
    recurse = False

# Add dependencies of target extension
with open(dependencies_file, 'r') as f:
    dependencies['ext'] = yaml.load(f, Loader=yaml.SafeLoader)

# Define rules for exclusions and inclusions
branch_rules = {
    'only': {
        'CirrusSearch': {
            'branches': ['master'],
            'repos': ['miraheze/MirahezeMagic'],
            'reason': 'Consistently failing',
        },
        'Elastica': {
            'branches': ['master'],
            'repos': ['miraheze/MirahezeMagic'],
            'reason': 'Since we are excluding CirrusSearch',
        },
        'GrowthExperiments': {
            'branches': ['master'],
            'repos': ['miraheze/MirahezeMagic'],
            'reason': 'Requires CirrusSearch in tests',
        },
        'CheckUser': {
            'branches': ['master', 'REL1_43'],
            'repos': ['miraheze/MirahezeMagic'],
            'reason': 'Requires GrowthExperiments in tests',
        },
        'IPInfo': {
            'branches': ['master', 'REL1_43'],
            'repos': ['miraheze/MirahezeMagic'],
            'reason': 'Requires CheckUser in tests',
        },
    },
}

def should_exclude(dependency, branch):
    """Checks if a dependency should be excluded for a specific branch."""
    # Exclusions specific to the branch
    if branch in branch_rules and 'exclude' in branch_rules[branch]:
        exclusions = branch_rules[branch]['exclude']
        if dependency in exclusions:
            print(f'Excluding {dependency} on {branch}: {exclusions[dependency]}', file=sys.stderr)
            return True

    # Exclusions defined in the 'only' rule
    only_rule = branch_rules.get('only', {}).get(dependency)
    if only_rule:
        if branch not in only_rule['branches']:
            print(f"Excluding {dependency} on {branch}: {only_rule['reason']}", file=sys.stderr)
            return True

        current_repo = os.environ.get('GITHUB_REPOSITORY', '')
        if 'repos' in only_rule and current_repo not in only_rule['repos']:
            print(f"Excluding {dependency} for repo {current_repo}: {only_rule['reason']}", file=sys.stderr)
            return True

    return False

# Resolve dependencies
resolved_dependencies = []
for d in get_dependencies('ext', dependencies, recurse):
    repo = ''
    branch = ''
    if d in dependencies['ext']:
        if 'repo' in dependencies['ext'][d] and dependencies['ext'][d]['repo'] != 'auto':
            repo = '|' + dependencies['ext'][d]['repo']
        if 'branch' in dependencies['ext'][d] and dependencies['ext'][d]['branch'] != 'auto':
            branch = dependencies['ext'][d]['branch']

    # Check if the dependency should be excluded
    if should_exclude(d, branch or os.environ.get('MEDIAWIKI_VERSION')):
        continue

    if branch:
        branch = '|' + branch

    d = 'mediawiki/extensions/' + d
    d = d.replace('/extensions/skins/', '/skins/')
    d = d + repo + branch
    resolved_dependencies.append(d)

print(' '.join(resolved_dependencies))
