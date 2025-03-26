import random
import datetime
import json
import csv

def generate_application_metrics(app_name, timestamp, metrics_config):
    """
    Generates application observable metrics data.
    """
    metrics_data = {
        "application": app_name,
        "timestamp": timestamp.isoformat(),
    }

    for metric, config in metrics_config.items():
        metric_type = config.get("type", "float")
        min_value = config.get("min", 0)
        max_value = config.get("max", 100)

        if metric_type == "float":
            metrics_data[metric] = random.uniform(min_value, max_value)
        elif metric_type == "int":
            metrics_data[metric] = random.randint(min_value, max_value)
        elif metric_type == "boolean":
            metrics_data[metric] = random.choice([True, False])
        elif metric_type == "string":
            options = config.get("options", ["ok", "warning", "error"])
            metrics_data[metric] = random.choice(options)
        else:
            metrics_data[metric] = None

    return metrics_data

def generate_metrics_stream(app_name, start_time, interval, num_points, metrics_config):
    """
    Generates a stream of application metrics data.
    """
    metrics_stream = []
    current_time = start_time

    for _ in range(num_points):
        metrics_stream.append(generate_application_metrics(app_name, current_time, metrics_config))
        metrics_stream.append(generate_application_metrics('web-server-2', current_time, metrics_config))
        metrics_stream.append(generate_application_metrics('web-server-3', current_time, metrics_config))
        metrics_stream.append(generate_application_metrics('web-server-4', current_time, metrics_config))
        current_time += interval

    return metrics_stream

def save_to_csv(data, filename):
    """
    Saves the metrics data to a CSV file.

    Args:
        data (list): A list of metrics data dictionaries.
        filename (str): The name of the CSV file.
    """

    if not data:
        return

    keys = data[0].keys()

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Example Usage
app_name = "web-service-1"
start_time = datetime.datetime.now()
interval = datetime.timedelta(seconds=10)
num_points = 20

metrics_config = {
    "error_rate": {"type": "float", "min": 0, "max": 0.1},
    "cpu_usage_percent": {"type": "float", "min": 10, "max": 90},
    "memory_usage_mb": {"type": "int", "min": 100, "max": 1000},
    "health_status": {"type": "string", "options": ["ok", "warning", "error"]},

}

metrics_stream = generate_metrics_stream(app_name, start_time, interval, num_points, metrics_config)


save_to_csv(metrics_stream, "../data/observability_data.csv")

print("Observability data saved to observability_data.csv")