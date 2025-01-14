# Enhanced Password Generator

A modern web-based password generator with multiple generation modes and features.

## Features

- Multiple password generation modes:
  - Basic password with customizable complexity
  - Pattern-based generation
  - Word shuffling
  - Character replacement
- Password strength meter
- Dark mode support
- Copy to clipboard functionality
- Responsive design

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Navigate to the project directory
2. Run the Flask application:
```bash
python src/app.py
```
3. Open your browser and visit `http://localhost:5000`

## Usage

1. Select a generation mode from the dropdown
2. Configure the options based on the selected mode:
   - Basic: Choose complexity and length
   - Pattern: Enter a pattern using L (lowercase), U (uppercase), N (number), S (symbol)
   - Shuffle: Enter a word to shuffle
   - Replace: Enter a word for character replacement
3. Click "Generate Password"
4. Use the copy button to copy the generated password

## Security Notes

- Passwords are generated server-side for enhanced security
- No passwords are stored or logged
- Uses cryptographically secure random number generation
- CORS enabled for API access

## Technologies Used

- Backend: Flask (Python)
- Frontend: HTML5, CSS3, JavaScript
- Styling: Tailwind CSS
- Icons: Unicode emojis
