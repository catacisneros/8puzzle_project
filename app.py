from flask import Flask, render_template, request, jsonify
from a_star_solver import solve_puzzle
from utils import generate_puzzle_from_image, is_solvable
import random
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the absolute path to the project directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, 
           template_folder=os.path.join(BASE_DIR, 'templates'),
           static_folder=os.path.join(BASE_DIR, 'static'))

# Configure upload folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def home():
    try:
        logger.debug("Rendering home page")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}")
        return str(e), 500

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'error': 'No selected file'}), 400
        
        if not file.content_type.startswith('image/'):
            logger.error(f"Invalid file type: {file.content_type}")
            return jsonify({'error': 'File must be an image'}), 400
        
        logger.debug("Processing image")
        result = generate_puzzle_from_image(file)
        logger.debug(f"Generated puzzle state: {result['state']}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in upload: {str(e)}")
        return jsonify({'error': 'Error processing image'}), 500

@app.route('/shuffle', methods=['POST'])
def shuffle():
    try:
        data = request.json
        if not data or 'state' not in data:
            logger.error("No state provided in request")
            return jsonify({'error': 'No state provided'}), 400
            
        current_state = data['state']
        if not isinstance(current_state, list) or len(current_state) != 9:
            logger.error(f"Invalid state format: {current_state}")
            return jsonify({'error': 'Invalid state format'}), 400
            
        # Keep the empty space (0) in its current position
        empty_pos = current_state.index(0)
        non_zero_elements = [x for x in current_state if x != 0]
        
        # Shuffle until we get a solvable state
        while True:
            random.shuffle(non_zero_elements)
            new_state = non_zero_elements[:empty_pos] + [0] + non_zero_elements[empty_pos:]
            if is_solvable(new_state):
                break
        
        logger.debug(f"Shuffled state: {new_state}")
        return jsonify({'state': new_state})
    except Exception as e:
        logger.error(f"Error in shuffle: {str(e)}")
        return jsonify({'error': 'Error shuffling puzzle'}), 500

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        if not data or 'state' not in data:
            logger.error("No state provided in request")
            return jsonify({'error': 'No state provided'}), 400
        
        initial_state = data['state']
        if not isinstance(initial_state, list) or len(initial_state) != 9:
            logger.error(f"Invalid state format: {initial_state}")
            return jsonify({'error': 'Invalid state format'}), 400
        
        logger.debug(f"Solving puzzle with state: {initial_state}")
        path = solve_puzzle(initial_state)
        logger.debug(f"Solution path length: {len(path)}")
        return jsonify({'solution': path})
    
    except Exception as e:
        logger.error(f"Error in solve: {str(e)}")
        return jsonify({'error': 'Error solving puzzle'}), 500

if __name__ == '__main__':
    app.run(debug=True)
