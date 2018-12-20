# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.kube_controller_manager import KubeControllerManagerCheck

import os
import pytest
import mock


instance = {
    'prometheus_url': 'http://localhost:10252/metrics',
}

# Constants
CHECK_NAME = 'kube_controller_manager'
NAMESPACE = 'kube_controller_manager'

@pytest.fixture
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator

@pytest.fixture()
def mock_metrics():
    f_name = os.path.join(os.path.dirname(__file__), 'fixtures', 'metrics.txt')
    with open(f_name, 'r') as f:
        text_data = f.read()
    mocked = mock.patch(
        'requests.get',
        return_value=mock.MagicMock(
            status_code=200,
            iter_lines=lambda **kwargs: text_data.split("\n"),
            headers={'Content-Type': "text/plain"}
        )
    )
    yield mocked.start()
    mocked.stop()

def test_check_metrics(aggregator, mock_metrics):
    """
    Testing Kube_proxy in iptables mode.
    """

    c = KubeControllerManagerCheck(CHECK_NAME, None, {}, [instance])
    c.check(instance)

    aggregator.assert_metric(NAMESPACE + '.goroutines')
    aggregator.assert_metric(NAMESPACE + '.threads')
    aggregator.assert_metric(NAMESPACE + '.open_fds')

    aggregator.assert_metric(NAMESPACE + '.rate_limiter.use', value=1, tags=["controller:job"])
    aggregator.assert_metric(NAMESPACE + '.rate_limiter.use', value=0, tags=["controller:daemon"])

    aggregator.assert_metric(NAMESPACE + '.queue.adds', metric_type=aggregator.MONOTONIC_COUNT, value=29, tags=["queue:replicaset"])
    aggregator.assert_metric(NAMESPACE + '.queue.depth', metric_type=aggregator.GAUGE, value=3, tags=["queue:service"])
    aggregator.assert_metric(NAMESPACE + '.queue.retries', metric_type=aggregator.MONOTONIC_COUNT, value=13, tags=["queue:deployment"])
