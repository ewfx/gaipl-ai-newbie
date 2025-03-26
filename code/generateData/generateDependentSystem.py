import json

def generate_dependency_graph_test_data(applications):
    """
    Generates test data for application dependency graphs.

    Args:
        applications (list): A list of application names.

    Returns:
        dict: A dictionary representing the dependency graph.
    """

    dependency_graph = {}

    for app in applications:
        dependency_graph[app] = []

    # Add some random dependencies
    dependency_graph["web-service-1"] = ["web-service-2", "web-service-3"]
    dependency_graph["web-service-2"] = ["web-service-4"]
    dependency_graph["web-service-3"] = ["web-service-4"]

    return dependency_graph

# Example Usage
applications = ["web-service-1", "web-service-2", "web-service-3", "web-service-4"]
dependency_data = generate_dependency_graph_test_data(applications)


def save_to_file(dependency_data, filename):
    """Saves log data to a file (JSON lines format)."""
    with open(filename, 'w') as f:
        for log in dependency_data:
            f.write(json.dumps(log) + '\n')


save_to_file(dependency_data, '../data/dependency_graph.json')

