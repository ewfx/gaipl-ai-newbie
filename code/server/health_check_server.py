from flask import Flask, request

app = Flask(__name__)

df = {
    'web-server-1': 'yes',
    'web-server-2': 'no',
    'web-server-3': 'yes',
    'web-server-4': 'no',
    'web-server-5': 'yes',
    'web-server-6': 'no',
    'web-server-7': 'yes',
    'web-server-8': 'yes',
    'web-server-9': 'no',
    'web-server-10': 'yes'
}
@app.route("/health", methods=["GET"])
def execute_health():
    appName = request.args.get('appName')
    if(df.get(appName) is not None and df[appName]=='yes'):
        return appName + "is up and running"
    return appName+ "is down"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',
            port=8080)  # Make the server accessible from any IP on the network, and allow debugging.

