import os
import logging
from flask import Flask, request, jsonify
import docker
from common_python import (
    configure_logging,
    require_api_key,
    create_health_blueprint,
    log_request_info,
)

app = Flask("pg-isready-web")
configure_logging(app)
health_bp = create_health_blueprint()
app.register_blueprint(health_bp)
app.before_request(log_request_info)

POSTGRES_CONTAINER = os.getenv("POSTGRES_CONTAINER", "postgres")
DOCKER_HOST = os.getenv("DOCKER_HOST", "unix://var/run/docker.sock")

docker_client: docker.DockerClient


@app.route("/pg_isready/<db_name>", methods=["GET"])
@require_api_key
def check_pg_isready(db_name):
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username parameter is required"}), 400

    command = ["pg_isready", "-U", username, "-d", db_name]

    container = docker_client.containers.get(POSTGRES_CONTAINER)

    try:
        exec_result = container.exec_run(command, stdout=True, stderr=True)
        exit_code = exec_result.exit_code
        output = exec_result.output.decode("utf-8") if exec_result.output else ""
        status = "ready" if exit_code == 0 else "not ready"

        response = {
            "database": db_name,
            "username": username,
            "container": POSTGRES_CONTAINER,
            "status": status,
            "output": output.strip(),
        }
        app.logger.info(f"pg_isready check: {response}")
        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Error running pg_isready: {e}")
        return jsonify({"error": str(e)}), 500


def main():
    global docker_client

    try:
        docker_client = docker.DockerClient(base_url=DOCKER_HOST)
    except docker.errors.DockerException:
        error_msg = f"Docker host '{DOCKER_HOST}' not found"
        app.logger.error(error_msg)
        exit(1)

    try:
        docker_client.containers.get(POSTGRES_CONTAINER)
    except docker.errors.NotFound:
        error_msg = f"Container '{POSTGRES_CONTAINER}' not found"
        app.logger.error(error_msg)
        exit(1)


if __name__ == "__main__":
    main()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
