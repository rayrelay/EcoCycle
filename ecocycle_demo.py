from flask import Flask, render_template, request

app = Flask(__name__)

# Mock database of recyclable items and their instructions
RECYCLING_GUIDE = {
    "plastic bottle": "Rinse and remove caps. Place in blue recycling bin.",
    "paper": "Keep dry and clean. Place in blue recycling bin.",
    "cardboard": "Flatten boxes. Place in blue recycling bin.",
    "glass": "Rinse thoroughly. Place in green glass recycling bin.",
    "aluminum can": "Rinse and crush if possible. Place in blue recycling bin.",
    "electronics": "Take to designated e-waste recycling center. Do not place in regular bins.",
    "battery": "Take to special battery recycling drop-off location. Hazardous if disposed improperly."
}


@app.route('/')
def index():
    return render_template('ecocycle_index.html')


@app.route('/recycle', methods=['POST'])
def recycle():
    item = request.form['item'].lower()

    if item in RECYCLING_GUIDE:
        instruction = RECYCLING_GUIDE[item]
        points = 10  # Simulated points earned
    else:
        instruction = "We're not sure how to recycle this item. Please check with your local recycling facility."
        points = 0

    return render_template('ecocycle_results.html',
                           item=item,
                           instruction=instruction,
                           points=points)
