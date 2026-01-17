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

# Due to how ManageWiki works we only want explicit dependencies,
# otherwise we may get hundreds of test failures from extensions due to
# config or permission overrides.
if 'miraheze/ManageWiki' in os.environ.get('GITHUB_REPOSITORY', ''):
    recurse = False

# Add dependencies of target extension
with open(dependencies_file, 'r') as f:
    dependencies['ext'] = yaml.load(f, Loader=yaml.SafeLoader)

# Define rules for exclusions and inclusions
branch_rules = {
    'REL1_44': {
        'exclude': {
            'PageViewInfo': 'Fails without the Graph extension on REL1_44 only',
            'TestKitchen': 'Doesn\'t exist as itself; labeled as MetricsPlatform',
        },
    },
    'REL1_45': {
        'exclude': {
            'DiscussionTools': 'Unrelated test failures',
            'MobileFrontend': 'Unrelated test failures',
            'SecurePoll': 'Unrelated test failures',
            'TestKitchen': 'Doesn\'t exist as itself; labeled as MetricsPlatform',
        },
    },
    'only': {
        'CheckUser': {
            'branches': ['master'],
            'reason': 'Requires GrowthExperiments in tests',
        },
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
            'reason': 'Requires CirrusSearch in tests and is failing on REL1_44',
        },
        'IPInfo': {
            'branches': ['master'],
            'reason': 'Requires CheckUser in tests',
        },
        'WebAuthn': {
            'branches': ['master'],
            'reason': 'Composer failures with PHP 8.2',
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
        if 'repos' not in only_rule and branch not in only_rule['branches']:
            print(f"Excluding {dependency} on {branch}: {only_rule['reason']}", file=sys.stderr)
            return True

        current_repo = os.environ.get('GITHUB_REPOSITORY', '')
        if 'repos' in only_rule and current_repo in only_rule['repos'] and branch not in only_rule['branches']:
            print(f"Excluding {dependency} on {branch} for repo {current_repo}: {only_rule['reason']}", file=sys.stderr)
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
