from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

# تحميل نموذج التنبؤ
model = joblib.load('recidivism_model.pkl')

# تهيئة التطبيق
app = Flask(__name__)

# صفحة الإدخال
@app.route('/')
def index():
    return render_template('index.html')

# توقع واحتمالية العودة
@app.route('/predict', methods=['POST'])
def predict():
    # استلام البيانات من المستخدم من النموذج
    data = request.form
    age = int(data['age'])
    gender = int(data['gender'])
    crime_type = int(data['crime_type'])
    behavior_score = int(data['behavior_score'])
    mental_state = int(data['mental_state'])
    skills = int(data['skills'])

    # تجهيز البيانات للتنبؤ
    input_data = pd.DataFrame([[age, gender, crime_type, behavior_score, mental_state, skills]],
                              columns=['age', 'gender', 'crime_type', 'behavior_score', 'mental_state', 'skills'])

    # توقع النموذج
    prediction = model.predict(input_data)[0]

    # تحديد البرنامج التأهيلي بناءً على القيم
    if behavior_score < 3:
        program = "برنامج محو الأمية"
    elif mental_state < 3:
        program = "برنامج تحسين المهارات الاجتماعية"
    elif skills < 3:
        program = "برنامج التدريب المهني"
    else:
        program = "برنامج دمج متقدم"

    result = {
        "التنبؤ": "عرضة للعودة" if prediction == 1 else "مستعد للاندماج",
        "البرنامج الموصى به": program
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
