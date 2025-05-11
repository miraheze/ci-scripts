# A script to resolve dependencies of MediaWiki extension for Quibble test
import os
import sys
import yaml

# pf for https://raw.githubusercontent.com/wikimedia/integration-config/master/zuul/parameter_functions.py
from pf import dependencies, get_dependencies

# Get dependency file path from argument
dependencies_file = sys.argv[1]

# Global default: recurse unless --no-recurse passed
default_recurse = True
if len(sys.argv) >= 3 and sys.argv[2] == '--no-recurse':
    default_recurse = False

# Add dependencies of target extension
with open(dependencies_file, 'r') as f:
    dependencies['ext'] = yaml.load(f, Loader=yaml.SafeLoader)

# Define rules for exclusions and inclusions
branch_rules = {
    'REL1_42': {
        'exclude': {
            'CommunityConfiguration': 'Fails without CommunityConfigurationExample on REL1_42',
            'CommunityConfigurationExample': 'Does not exist on REL1_42',
        },
    },
    'only': {
        'DiscussionTools': {
            'branches': ['master'],
            'reason': 'Inconsistently failing',
        },
    },
}

def should_exclude(dependency, branch):
    """
    Determines whether a dependency should be excluded for a given branch.
    
    Checks branch-specific exclusion and inclusion rules to decide if the dependency
    should be skipped. Prints the exclusion reason to standard error if excluded.
    
    Args:
        dependency: The name of the dependency to check.
        branch: The branch name to evaluate rules against.
    
    Returns:
        True if the dependency should be excluded for the branch, False otherwise.
    """
    # Exclusions specific to the branch
    if branch in branch_rules and 'exclude' in branch_rules[branch]:
        exclusions = branch_rules[branch]['exclude']
        if dependency in exclusions:
            print(f'Excluding {dependency} on {branch}: {exclusions[dependency]}', file=sys.stderr)
            return True

    # Exclusions defined in the 'only' rule
    if dependency in branch_rules.get('only', {}):
        only_rule = branch_rules['only'][dependency]
        if branch not in only_rule['branches']:
            print(f"Excluding {dependency} on {branch}: {only_rule['reason']}", file=sys.stderr)
            return True

    return False

# Determine per-dependency override for recurse
def should_recurse(dep_name):
    """
    Determines whether to recurse into a dependency during resolution.
    
    Checks the dependency's configuration for a 'recurse' override; if not set,
    returns the global default recursion setting.
    
    Args:
        dep_name: The name of the dependency to check.
    
    Returns:
        True if recursion should occur for this dependency, otherwise False.
    """
    config = dependencies['ext'].get(dep_name, {})
    return config.get('recurse', default_recurse)

# Resolve dependencies
resolved_dependencies = []
for d in get_dependencies('ext', dependencies, should_recurse):
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
