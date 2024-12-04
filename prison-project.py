from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import os

# تحميل نموذج التنبؤ باستخدام المسار من المتغير البيئي
model_path = os.getenv('MODEL_PATH', 'C:/sqlite/prison_project/recidivism_prediction/recidivism_model.pkl')
model = joblib.load(model_path)

# تهيئة التطبيق
app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# دالة التنبؤ وإرجاع النتيجة
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # استلام ومعالجة البيانات المدخلة من المستخدم
        inputs = {
            "age": int(request.form.get('age', 0)),
            "gender": int(request.form.get('gender', 0)),
            "crime_type": int(request.form.get('crime_type', 0)),
            "behavior_score": int(request.form.get('behavior_score', 0)),
            "mental_state": int(request.form.get('mental_state', 0)),
            "skills": int(request.form.get('skills', 0))
        }
    except ValueError:
        return jsonify({"error": "يرجى إدخال قيم صحيحة لجميع الحقول"}), 400

    # تجهيز البيانات للتنبؤ
    input_data = pd.DataFrame([list(inputs.values())],
                              columns=list(inputs.keys()))

    # تنبؤ باستخدام النموذج
    prediction = model.predict(input_data)[0]

    # تحديد البرنامج التأهيلي بناءً على المدخلات
    program = (
        "برنامج محو الأمية" if inputs["behavior_score"] < 3 else
        "برنامج تحسين المهارات الاجتماعية" if inputs["mental_state"] < 3 else
        "برنامج التدريب المهني" if inputs["skills"] < 3 else
        "برنامج دمج متقدم"
    )

    # إعداد النتيجة النهائية
    result = {
        "التنبؤ": "عرضة للعودة" if prediction == 1 else "مستعد للاندماج",
        "البرنامج الموصى به": program
    }

    return jsonify(result)

# تشغيل التطبيق
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
