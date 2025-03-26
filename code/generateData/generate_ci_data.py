import pandas as pd
import random
import datetime

def generate_cmdb_data(num_items=100):
    """Generates sample Configuration Item (CI) data."""

    ci_types = ["Server", "Database", "Application", "NetworkDevice", "LoadBalancer"]
    operating_systems = ["Windows Server 2019", "Linux CentOS 7", "Ubuntu 20.04", "macOS Server"]
    environments = ["Production", "Staging", "Development", "Test"]
    applications = ["web-service-1", "web-service-2", "web-service-3", "web-service-4", "database-1", "message-queue-1", "cache-1", "api-gateway-1", "server-1", "server-2","server-3","server-4"]
    vendors = ["Dell", "HP", "Cisco", "Microsoft", "Oracle", "VMware"]

    data = []
    for i in range(num_items):
        ci_type = random.choice(ci_types)
        item = {
            "CI_ID": f"CI-{i+1:04}",
            "CI_Type": ci_type,
            "Name": f"{ci_type}-{random.randint(100, 999)}",
            "OperatingSystem": random.choice(operating_systems) if ci_type == "Server" else None,
            "Environment": random.choice(environments),
            "Application": random.choice(applications) if ci_type == "Application" else None,
            "Vendor": random.choice(vendors),
            "IP_Address": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}" if ci_type in ["Server", "NetworkDevice", "LoadBalancer"] else None,
            "Version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
            "InstallDate": (datetime.datetime.now() - datetime.timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "Status": random.choice(["Running", "Stopped", "Error", "Maintenance"]),
            "CPU_Cores": random.randint(2, 16) if ci_type == "Server" else None,
            "Memory_GB": random.randint(4, 64) if ci_type == "Server" else None,
            "Database_Type": random.choice(["MySQL", "PostgreSQL", "MongoDB", "OracleDB"]) if ci_type == "Database" else None,
            "Network_Interface": random.choice(["Ethernet", "Fiber", "Wireless"]) if ci_type == "NetworkDevice" else None,
            "Load_Balancing_Algorithm": random.choice(["Round Robin", "Least Connections", "IP Hash"]) if ci_type == "LoadBalancer" else None,
            "Region": random.choice(["US-East", "US-West", "EU-Central", "AP-Southeast"]),
            "Owner": f"User-{random.randint(10, 99)}"
        }
        data.append(item)

    df = pd.DataFrame(data)
    return df

# Generate and save the sample data
cmdb_df = generate_cmdb_data(100) #Generate more data.
cmdb_df.to_csv("ci_data.csv", index=False)
print("CMDB data generated and saved to cmdb_data.csv")
