# -*- coding: utf-8 -*-
'''
Beacon to emit when a screen is available to a linux machine

.. versionadded:: Boron
'''

# Import Python libs
from __future__ import absolute_import
import logging

# Salt libs
import salt.utils

log = logging.getLogger(__name__)

__virtualname__ = 'glxinfo'

last_state = {}


def __virtual__():

    which_result = salt.utils.which('glxinfo')
    if which_result is None:
        return False
    else:
        return __virtualname__


def validate(config):
    '''
    Validate the beacon configuration
    '''
    # Configuration for adb beacon should be a dictionary with states array
    if not isinstance(config, dict):
        log.info('Configuration for glxinfo beacon must be a dict.')
        return False
    return True


def beacon(config):
    '''
    Emit the status of a connected monitor to the minion

    Mainly this is used to detect when the monitor fails to connect for whatever reason.

    .. code-block:: yaml

        beacons:
          glxinfo:
            screen_event: True

    '''

    log.trace('glxinfo beacon starting')
    ret = []

    if not validate(config):
        return ret

    retcode = __salt__['cmd.retcode']('DISPLAY=:0 glxinfo', python_shell=True)

    if 'screen_event' in config and config['screen_event']:
        last_value = last_state.get('screen_available', False)
        screen_available = retcode == 0
        if last_value != screen_available or 'screen_available' not in last_state:
            ret.append({'tag': 'screen_event', 'screen_available': screen_available})

        last_state['screen_available'] = screen_available

    return ret
