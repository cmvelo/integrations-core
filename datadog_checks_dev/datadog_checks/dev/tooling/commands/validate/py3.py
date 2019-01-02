# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import click
import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from a7 import validate_py3
from six import iteritems

from ..console import CONTEXT_SETTINGS, abort, echo_failure, echo_info, echo_success
from ...constants import get_root, NOT_CHECKS
from ...utils import get_valid_checks


@click.command(
    context_settings=CONTEXT_SETTINGS,
    short_help="Verify if a custom check or integration can run on python 3"
)
@click.argument('check')
def py3(check):
    """Verify if a custom check or integration can run on python 3. CHECK
    can be an integration name or a valid path to a Python module or package folder.
    """

    root = get_root()
    if check == 'datadog_checks_base':
        path_to_module = os.path.join(root, check, 'datadog_checks', 'base')
    elif check in get_valid_checks() and check not in NOT_CHECKS:
        path_to_module = os.path.join(root, check, 'datadog_checks', check)
    else:
        path_to_module = check

    if not os.path.exists(path_to_module):
        abort("{} does not exist.".format(path_to_module))

    echo_info("Validating python3 compatibility of {}...".format(check))
    results = validate_py3(path_to_module)

    if results:
        echo_failure("Incompatibilities were found for {}:".format(check))
        for file, problems in iteritems(results):
            echo_info("File {}:".format(file))
            for problem in problems:
                echo_failure("  {}".format(problem))
        abort()
    else:
        echo_success("{} is compatible with python3".format(check))
