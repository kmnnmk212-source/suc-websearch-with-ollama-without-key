from flask import Flask, request, jsonify
from flask_cors import CORS
from ddgs import DDGS
import logging

app = Flask(__name__)
# تفعيل CORS للسماح لصفحة HTML بالتحدث مع هذا السيرفر
CORS(app)

# إعداد التسجيل لعرض الأخطاء
logging.basicConfig(level=logging.INFO)

# --- هذا هو الجزء الذي أضفناه لحل مشكلة 404 ---
@app.route('/')
def home():
    return "Server is Ready"
# ----------------------------------------------

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    logging.info(f"🔍 Searching for: {query} ...")
    results_text = ""
    
    try:
        # البحث باستخدام DuckDuckGo
        # max_results: عدد النتائج التي سيتم جلبها
        ddgs = DDGS()
        # استخدام ddgs.text للبحث العام
        results = list(ddgs.text(query, max_results=3))
        
        if not results:
            return jsonify({"context": "لم يتم العثور على نتائج في البحث."})

        for index, result in enumerate(results):
            title = result.get('title', 'No Title')
            body = result.get('body', 'No Content')
            # تجميع النتائج في نص واحد ليتم إرساله للذكاء الاصطناعي
            results_text += f"مصدر {index+1} ({title}):\n{body}\n\n"
            
        logging.info("✅ Search completed.")
        return jsonify({"context": results_text})

    except Exception as e:
        logging.error(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # تشغيل السيرفر على المنفذ 5000
    print("🚀 Python Search Server running on http://localhost:5000")
    app.run(port=5000, debug=True)
