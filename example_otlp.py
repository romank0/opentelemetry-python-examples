import random
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import DEPLOYMENT_ENVIRONMENT, SERVICE_NAME, Resource

exporter = OTLPMetricExporter(endpoint="localhost:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)

metrics.set_meter_provider(
    MeterProvider(
        resource=Resource(
            attributes={SERVICE_NAME: "test-service", DEPLOYMENT_ENVIRONMENT: "dev"}
        ),
        metric_readers=[reader],
    )
)
meter = metrics.get_meter(__name__)

"""
histogram_metric = meter.create_histogram(
    name="test.example_histogram",
    description="Example histogram metric",
    unit="ms",
)
"""

queue_len = 100
processing_lag = 0


def queue_length_callback(options):
    print(f"observed len: {queue_len}")
    yield metrics.Observation(queue_len)


def queue_processing_lag_callback(options):
    print(f"observed lag: {processing_lag}")
    yield metrics.Observation(1000 * processing_lag)


queue_length_gauge = meter.create_observable_gauge(
    name="test.example-queue-len",
    callbacks=[queue_length_callback],
    description="Example queue len metric",
    unit="items",
)
queue_lag_gauge = meter.create_observable_gauge(
    name="test.example-queue-processing-lag",
    callbacks=[queue_processing_lag_callback],
    description="Example queue processing lag metric",
    unit="ms",
)


while True:
    print(f"len: {queue_len} lag: {processing_lag}")
    # histogram_metric.record(time.time() % 100)
    queue_len += random.randint(-5, 5)
    processing_lag += random.randint(-1 if processing_lag > 1 else -processing_lag, 1)
    time.sleep(1)
