import hmac
import hashlib
import uuid
import time
import os
from flask import Blueprint, jsonify

upload_bp = Blueprint('upload', __name__)

# Credentials from environment variables
IMAGEKIT_PRIVATE_KEY = os.getenv('IMAGEKIT_PRIVATE_KEY')
IMAGEKIT_PUBLIC_KEY = os.getenv('IMAGEKIT_PUBLIC_KEY')
IMAGEKIT_URL_ENDPOINT = os.getenv('IMAGEKIT_URL_ENDPOINT')

@upload_bp.route('/config', methods=['GET'])
def get_config():
    """Return public configuration for frontend SDK"""
    return jsonify({
        "publicKey": IMAGEKIT_PUBLIC_KEY,
        "urlEndpoint": IMAGEKIT_URL_ENDPOINT
    })

@upload_bp.route('/auth', methods=['GET'])
def get_auth_params():
    try:
        token = str(uuid.uuid4())
        expire = str(int(time.time()) + 1800) # 30 mins expiry
        
        # Create signature: HMAC-SHA1(private_key, token + expire)
        # Note: ImageKit expects the input data to be token + expire
        data = f"{token}{expire}"
        
        signature = hmac.new(
            IMAGEKIT_PRIVATE_KEY.encode(),
            data.encode(),
            hashlib.sha1
        ).hexdigest()
        
        return jsonify({
            "token": token,
            "expire": expire,
            "signature": signature
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@upload_bp.route('/local', methods=['POST'])
def upload_local():
    """Handle local file upload"""
    try:
        from flask import request, current_app
        from werkzeug.utils import secure_filename
        import os

        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400
            
        if file:
            filename = secure_filename(file.filename)
            # Generate unique filename to avoid overwrites
            unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
            
            # Determine path to frontend assets
            # backend/app/api -> backend/app -> backend -> root
            # Target: frontend/assets/images/cities
            
            # Assuming typical structure where backend and frontend are siblings
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            assets_dir = os.path.join(base_dir, 'frontend', 'assets', 'images', 'cities')
            
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)
                
            file.save(os.path.join(assets_dir, unique_filename))
            
            return jsonify({
                'success': True,
                'filename': unique_filename,
                'url': unique_filename # For local, we just store the filename relative to assets path
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
