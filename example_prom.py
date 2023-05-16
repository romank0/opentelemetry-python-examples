import time
from prometheus_client import start_http_server

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


if __name__ == "__main__":
    # Service name is required for most backends
    resource = Resource(attributes={SERVICE_NAME: "otel-prom-test"})

    # Start Prometheus client
    start_http_server(port=8000, addr="0.0.0.0")
    # Initialize PrometheusMetricReader which pulls metrics from the SDK
    # on-demand to respond to scrape requests
    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    meter = metrics.get_meter_provider().get_meter("getting-started", "0.1.2")

    # Counter
    print("Synchronous counter")
    counter = meter.create_counter("counter")
    while True:
        counter.add(1)
        print("Sleeping for 3 secs.")
        time.sleep(3)
        counter.add(1)
    print("Finished counting.")
