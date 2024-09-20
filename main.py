from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/card1')
def card1():
    return render_template('card1.html')

@app.route('/card2')
def card2():
    return render_template('card2.html')

@app.route('/card3')
def card3():
    return render_template('card3.html')

if __name__ == '__main__':
    app.run(debug=True)
#dc3545