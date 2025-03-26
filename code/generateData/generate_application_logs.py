import random
import datetime
import json
import uuid
import logging

def generate_log_entry(app_name, timestamp, log_level, message, correlation_id, user_id, extra_data=None):
    """
    Generates a log entry with predefined correlation ID and user ID.

    Args:
        app_name (str): The name of the application.
        timestamp (datetime.datetime): The timestamp of the log entry.
        log_level (str): The log level (e.g., INFO, WARNING, ERROR).
        message (str): The log message.
        correlation_id (str): The correlation ID.
        user_id (str): The user ID.
        extra_data (dict, optional): Additional data to include in the log entry.
    """

    log_entry = {
        "application": app_name,
        "timestamp": timestamp.isoformat(),
        "log_level": log_level,
        "message": message,
        "correlation_id": correlation_id,
        "user_id": user_id,
    }

    if extra_data:
        log_entry.update(extra_data)

    return log_entry

def generate_log_stream(app_name, start_time, interval, num_entries, user_ids, correlation_id_gen):
    """
    Generates a stream of application log entries.
    """

    log_stream = []
    current_time = start_time

    log_levels = ["INFO", "WARNING", "ERROR"]
    messages = [
        "Request processed successfully.",
        "Database connection timeout.",
        "User authentication failed.",
        "Resource not found.",
        "Application started.",
        "Unexpected error occurred.",
        "Configuration loaded.",
        "External service unavailable."
    ]

    for _ in range(num_entries):
        user_id = random.choice(user_ids)
        correlation_id = correlation_id_gen()
        log_level = random.choice(log_levels)
        message = random.choice(messages)
        extra_data = {}
        app_nm = random.choice(app_name)
        if log_level == "ERROR":
            extra_data = {"error_code": random.randint(500, 599), "stacktrace": "..."} #example of error specific data.
        log_stream.append(generate_log_entry(app_nm, current_time, log_level, message, correlation_id, user_id, extra_data))
        current_time += interval

    return log_stream

def save_logs_to_file(logs, filename):
    """Saves log data to a file (JSON lines format)."""
    with open(filename, 'w') as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')

# Example Usage
app_name = ["web-service-1","web-service-2","web-service-3"]
start_time = datetime.datetime.now()
interval = datetime.timedelta(seconds=1)
num_entries = 100
user_ids = ["user123", "user456", "user789"]
correlation_id_gen = lambda: str(uuid.uuid4()) #generates unique correlation IDs.

log_stream = generate_log_stream(app_name, start_time, interval, num_entries, user_ids, correlation_id_gen)

save_logs_to_file(log_stream, "../data/application_logs.txt")

print("Application logs saved to application_logs.jsonl")

