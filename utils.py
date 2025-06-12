from PIL import Image
import numpy as np
import io
import base64

def is_solvable(puzzle):
    # Count inversions
    inversions = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:
                inversions += 1
    return inversions % 2 == 0

def generate_puzzle_from_image(file):
    try:
        # Read the image from the file object
        img = Image.open(io.BytesIO(file.read()))
        
        # Convert to RGB if image is in a different mode
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to 3x3 grid
        img = img.resize((300, 300))
        
        # Convert the entire image to base64 for background
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        background_img = base64.b64encode(buffered.getvalue()).decode()
        
        # Split into 3x3 grid
        h, w = img.size
        cell_h, cell_w = h // 3, w // 3
        
        # Store image segments and calculate puzzle state
        segments = []
        puzzle = []
        
        # Create 8 pieces (excluding the empty space)
        for i in range(3):
            for j in range(3):
                # Skip the top-left position (will be empty)
                if i == 0 and j == 0:
                    segments.append('')  # Empty segment for the empty space
                    puzzle.append(0)  # 0 represents empty space
                    continue
                
                # Crop the segment
                left = j * cell_w
                upper = i * cell_h
                right = left + cell_w
                lower = upper + cell_h
                segment = img.crop((left, upper, right, lower))
                
                # Convert segment to base64
                buffered = io.BytesIO()
                segment.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                segments.append(img_str)
                
                # Calculate position for puzzle state (1-8)
                puzzle.append(i * 3 + j)
        
        # Shuffle the puzzle while ensuring it's solvable
        while True:
            np.random.shuffle(puzzle)
            if is_solvable(puzzle):
                break
        
        return {
            'state': puzzle,
            'segments': segments,
            'background': background_img
        }
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        # Return a default puzzle if there's an error
        return {
            'state': list(range(9)),
            'segments': [''] * 9,
            'background': ''
        }
