from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# 扩展的回收物品数据库
RECYCLING_GUIDE = {
    "plastic bottle": {
        "instruction": "Rinse and remove caps. Place in blue recycling bin.",
        "points": 5,
        "category": "Plastic",
        "tips": ["Crush bottles to save space", "Remove labels if possible"]
    },
    "paper": {
        "instruction": "Keep dry and clean. Place in blue recycling bin.",
        "points": 3,
        "category": "Paper",
        "tips": ["Flatten cardboard boxes", "Remove any plastic wrapping"]
    },
    "cardboard": {
        "instruction": "Flatten boxes. Place in blue recycling bin.",
        "points": 4,
        "category": "Paper",
        "tips": ["Break down large boxes", "Remove packing tape"]
    },
    "glass bottle": {
        "instruction": "Rinse thoroughly. Place in green glass recycling bin.",
        "points": 6,
        "category": "Glass",
        "tips": ["Remove metal caps", "Don't break glass - it's harder to recycle"]
    },
    "aluminum can": {
        "instruction": "Rinse and crush if possible. Place in blue recycling bin.",
        "points": 8,
        "category": "Metal",
        "tips": ["Crushing saves space", "Check for local redemption value"]
    },
    "electronics": {
        "instruction": "Take to designated e-waste recycling center. Do not place in regular bins.",
        "points": 15,
        "category": "E-Waste",
        "tips": ["Remove batteries if possible", "Wipe personal data from devices"]
    },
    "battery": {
        "instruction": "Take to special battery recycling drop-off location. Hazardous if disposed improperly.",
        "points": 10,
        "category": "Hazardous",
        "tips": ["Tape terminals of lithium batteries", "Store in cool, dry place until recycling"]
    },
    "plastic bag": {
        "instruction": "Take to grocery store recycling bin. Do not place in curbside recycling.",
        "points": 2,
        "category": "Plastic",
        "tips": ["Reuse when possible", "Collect multiple bags together for recycling"]
    },
    "food waste": {
        "instruction": "Compost if possible. Otherwise dispose in regular trash.",
        "points": 0,
        "category": "Organic",
        "tips": ["Start a compost bin", "Use a countertop compost collector"]
    }
}

# 用户数据模拟（在真实应用中会使用数据库）
user_data = {
    "points": 0,
    "level": 1,
    "recycled_items": [],
    "next_reward": 50
}


@app.route('/')
def index():
    return render_template('ecocycle_index.html')


@app.route('/recycle', methods=['POST'])
def recycle():
    item = request.form['item'].lower()

    if item in RECYCLING_GUIDE:
        guide = RECYCLING_GUIDE[item]
        points = guide["points"]

        # 更新用户数据
        user_data["points"] += points
        user_data["recycled_items"].append({
            "item": item,
            "points": points,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        # 检查是否升级
        if user_data["points"] >= user_data["next_reward"]:
            user_data["level"] += 1
            user_data["next_reward"] = user_data["level"] * 50

        return render_template('ecocycle_results.html',
                               item=item,
                               instruction=guide["instruction"],
                               points=points,
                               category=guide["category"],
                               tips=guide["tips"],
                               user_data=user_data)
    else:
        return render_template('ecocycle_results.html',
                               item=item,
                               instruction="We're not sure how to recycle this item. Please check with your local recycling facility.",
                               points=0,
                               category="Unknown",
                               tips=["Try searching for similar items", "Contact your local waste management"],
                               user_data=user_data)


@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    results = []

    if query:
        # 简单搜索实现
        for item, data in RECYCLING_GUIDE.items():
            if query in item:
                results.append({"item": item, "category": data["category"]})

    return jsonify(results)
