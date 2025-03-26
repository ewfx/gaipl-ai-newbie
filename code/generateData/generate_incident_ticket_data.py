import pandas as pd
import numpy as np
import datetime

def generate_incident_data(num_records=100):
    """Generates test data for incident management."""

    components = ["web-service-1", "web-service-2", "web-service-3", "web-service-4", "database-1", "message-queue-1", "cache-1", "api-gateway-1", "server-1", "server-2","server-3","server-4"]
    users = ["user1", "user2", "user3", "user4", "user5", "system_process"]
    status_values = ["Open", "In Progress", "Resolved", "Closed", "Pending", "Escalated"]
    problem_statements = [
        "Application is slow.",
        "Database connection failed.",
        "Network latency is high.",
        "API Service returned 500 error.",
        "Frontend UI not loading.",
        "Backend Service crashed.",
        "Middleware timeout.",
        "Load Balancer overload.",
        "User unable to login.",
        "Data corruption in Database Y."
    ]

    data = {
        "Ticket ID": [f"INC-{i:05d}" for i in range(1, num_records + 1)],
        "Problem Statement": np.random.choice(problem_statements, num_records),
        "Application": np.random.choice(components, num_records),
        "Logs": [f"Log entry {i}" for i in range(num_records)],
        "User": np.random.choice(users, num_records),
        "Creation Date": [datetime.datetime.now() - datetime.timedelta(days=np.random.randint(1, 30)) for _ in range(num_records)],
        "Resolution Date": [None] * num_records,
        "Comments by Support Person": [None] * num_records,
        "Status": np.random.choice(status_values, num_records)
    }

    df = pd.DataFrame(data)

    # Simulate resolution dates and comments for resolved/closed tickets
    for index, row in df.iterrows():
        if row["Status"] in ["Resolved", "Closed"]:
            df.at[index, "Resolution Date"] = row["Creation Date"] + datetime.timedelta(hours=np.random.randint(1, 24))
            df.at[index, "Comments by Support Person"] = f"Issue resolved. {np.random.choice(['Root cause: Network issue.', 'Fixed by restarting service.', 'Data corrected.'])}"

    return df

# Generate and display the test data
test_data = generate_incident_data(150) # You can change the number of records
test_data.to_csv("incident_data.csv", index=False)