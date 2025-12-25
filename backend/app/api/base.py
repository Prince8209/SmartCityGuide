from flask.views import MethodView
from flask import jsonify

class BaseAPI(MethodView):
    """
    Abstract Base Class for all API endpoints.
    Encapsulates common response logic and enforces OOP structure.
    """
    
    def send_response(self, data, status=200):
        """
        Standardized success response.
        Abstraction: Hides the details of JSON formatting.
        """
        response = {'success': True}
        if data:
            response.update(data)
        return jsonify(response), status

    def send_error(self, message, status=400):
        """
        Standardized error response.
        Abstraction: Hides exception handling details.
        """
        return jsonify({'success': False, 'error': message}), status
