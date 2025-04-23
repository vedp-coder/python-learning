import string
import random
import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         long_url TEXT NOT NULL,
         short_code TEXT NOT NULL UNIQUE)
    ''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form.get('url')
        if long_url:
            # Generate unique short code
            while True:
                short_code = generate_short_code()
                conn = sqlite3.connect('urls.db')
                c = conn.cursor()
                
                # Check if code exists
                if not c.execute('SELECT 1 FROM urls WHERE short_code=?', 
                               (short_code,)).fetchone():
                    # Save new URL
                    c.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)',
                            (long_url, short_code))
                    conn.commit()
                    conn.close()
                    break
            
            short_url = request.host_url + short_code
            return f'Shortened URL: <a href="{short_url}">{short_url}</a>'
    
    return '''
        <form method="POST">
            <input type="url" name="url" placeholder="Enter URL" required>
            <button type="submit">Shorten URL</button>
        </form>
    '''

@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    result = c.execute('SELECT long_url FROM urls WHERE short_code=?', 
                      (short_code,)).fetchone()
    conn.close()
    
    if result:
        return redirect(result[0])
    return 'URL not found', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
