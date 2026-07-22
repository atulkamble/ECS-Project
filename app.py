from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>AWS ECS Project</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f4f7fb;
                    text-align: center;
                    padding-top: 100px;
                }

                .card {
                    background: white;
                    width: 600px;
                    margin: auto;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                }

                h1 {
                    color: #ff9900;
                }

                p {
                    color: #333333;
                    font-size: 18px;
                }
            </style>
        </head>

        <body>
            <div class="card">
                <h1>Amazon ECS Project</h1>
                <p>Python Flask application deployed successfully.</p>
                <p>Platform: ECS Fargate</p>
                <p>Image Registry: Amazon ECR</p>
            </div>
        </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "ecs-flask-app",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    ), 200


@app.route("/api/info")
def application_info():
    return jsonify(
        {
            "application": "Basic ECS Flask Project",
            "platform": "Amazon ECS Fargate",
            "container": "Docker",
            "registry": "Amazon ECR",
            "version": "1.0.0",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
