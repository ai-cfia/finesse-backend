from flask_restx import Namespace, Resource

monitor_namespace = Namespace("monitor", description="Monitoring operations")


@monitor_namespace.route("")
class Health(Resource):
    def get(self):
        return "ok", 200
