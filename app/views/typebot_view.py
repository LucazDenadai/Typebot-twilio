from flask import jsonify

class TypebotView:
    @staticmethod
    def render_response(message):
        return jsonify({"response": message})