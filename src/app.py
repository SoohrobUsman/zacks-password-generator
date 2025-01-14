from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
import string
import re
import os

app = Flask(__name__, 
    static_folder='../static',
    template_folder='../templates'
)
CORS(app)

# Configure app for production
app.config['PROPAGATE_EXCEPTIONS'] = True

def generate_basic_password(complexity='medium', length=12):
    # Ensure minimum length to accommodate 'Zack'
    length = max(length, 8)  # 'Zack' + at least 4 more characters
    
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    if complexity == 'easy':
        chars = lowercase + digits
    elif complexity == 'medium':
        chars = lowercase + uppercase + digits
    else:  # hard
        chars = lowercase + uppercase + digits + symbols
    
    # Generate the random part of the password
    random_length = length - 4  # Reserve 4 characters for 'Zack'
    random_part = ''.join(random.choice(chars) for _ in range(random_length))
    
    # Insert 'Zack' at a random position
    insert_pos = random.randint(0, random_length)
    password = random_part[:insert_pos] + 'Zack' + random_part[insert_pos:]
    
    return password

def generate_pattern_password(pattern):
    mapping = {
        'L': string.ascii_lowercase,
        'U': string.ascii_uppercase,
        'N': string.digits,
        'S': '!@#$%^&*()_+-=[]{}|;:,.<>?'
    }
    
    # Generate password according to pattern
    password = ''.join(random.choice(mapping.get(c, c)) for c in pattern.upper())
    
    # Add 'Zack' if not already present
    if 'Zack' not in password:
        insert_pos = random.randint(0, len(password))
        password = password[:insert_pos] + 'Zack' + password[insert_pos:]
    
    return password

def shuffle_word(word):
    # Ensure 'Zack' is in the word
    if 'Zack' not in word:
        word = word + 'Zack'
    
    chars = list(word)
    # Keep shuffling until we get a different arrangement
    original = ''.join(chars)
    while ''.join(chars) == original:
        random.shuffle(chars)
    return ''.join(chars)

def replace_chars(word):
    # Ensure 'Zack' is in the word
    if 'Zack' not in word:
        word = word + 'Zack'
    
    replacements = {
        'a': '@', 'e': '3', 'i': '1', 'o': '0', 
        's': '$', 't': '7', 'b': '8', 'g': '9'
    }
    result = ''
    # Don't replace characters in 'Zack'
    zack_index = word.lower().find('zack')
    
    for i, char in enumerate(word.lower()):
        if i >= zack_index and i < zack_index + 4:
            result += word[i]  # Keep original character
        else:
            result += replacements.get(char, char)
    
    return result

def calculate_password_strength(password):
    score = 0
    
    # Length check
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 2
    
    # Character variety
    if re.search(r'[A-Z]', password): score += 2
    if re.search(r'[a-z]', password): score += 1
    if re.search(r'\d', password): score += 2
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password): score += 3
    
    # Special conditions
    if re.search(r'[A-Z].*[A-Z]', password): score += 1  # Multiple uppercase
    if re.search(r'\d.*\d', password): score += 1  # Multiple numbers
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?].*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password): score += 2  # Multiple symbols
    
    # Return strength category
    if score <= 4: return 'weak'
    elif score <= 8: return 'medium'
    else: return 'strong'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        mode = data.get('mode', 'basic')
        
        if mode == 'basic':
            complexity = data.get('complexity', 'medium')
            length = int(data.get('length', 12))
            if length < 6 or length > 32:
                return jsonify({'error': 'Length must be between 6 and 32'}), 400
            password = generate_basic_password(complexity, length)
        elif mode == 'pattern':
            pattern = data.get('pattern', '')
            if not pattern:
                return jsonify({'error': 'Pattern is required'}), 400
            password = generate_pattern_password(pattern)
        elif mode == 'shuffle':
            word = data.get('word', '')
            if not word:
                return jsonify({'error': 'Word is required'}), 400
            password = shuffle_word(word)
        elif mode == 'replace':
            word = data.get('word', '')
            if not word:
                return jsonify({'error': 'Word is required'}), 400
            password = replace_chars(word)
        else:
            return jsonify({'error': 'Invalid mode'}), 400
            
        # Calculate password strength
        strength = calculate_password_strength(password)
        
        return jsonify({
            'password': password,
            'strength': strength
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error generating password: {str(e)}")
        return jsonify({'error': 'Error generating password'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
