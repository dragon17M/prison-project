from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

# تحميل نموذج التنبؤ من الملف
model = joblib.load('C:/sqlite/prison_project/recidivism_prediction/recidivism_model.pkl')

# تهيئة التطبيق
app = Flask(__name__)

# صفحة الإدخال (واجهة المستخدم)
@app.route('/')
def index():
    return render_template('index.html')  # عرض صفحة الإدخال للمستخدم

# التنبؤ واحتمالية العودة
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # استلام البيانات من المستخدم عبر نموذج الإدخال
        age = int(request.form['age'])  # تحويل العمر إلى عدد صحيح
        gender = int(request.form['gender'])  # تحويل الجنس إلى عدد صحيح
        crime_type = int(request.form['crime_type'])  # تحويل نوع الجريمة إلى عدد صحيح
        behavior_score = int(request.form['behavior_score'])  # تحويل درجة السلوك إلى عدد صحيح
        mental_state = int(request.form['mental_state'])  # تحويل الحالة النفسية إلى عدد صحيح
        skills = int(request.form['skills'])  # تحويل المهارات إلى عدد صحيح
    except ValueError:
        # إذا كانت البيانات المدخلة غير صالحة (مثل نص بدلاً من أرقام)، سيتم إرجاع رسالة خطأ
        return jsonify({"error": "يرجى إدخال قيم صحيحة لجميع الحقول"}), 400
    
    # تجهيز البيانات على شكل DataFrame للتنبؤ باستخدام النموذج
    input_data = pd.DataFrame([[age, gender, crime_type, behavior_score, mental_state, skills]],
                              columns=['age', 'gender', 'crime_type', 'behavior_score', 'mental_state', 'skills'])

    # استخدام النموذج للتنبؤ
    prediction = model.predict(input_data)[0]  # الحصول على التنبؤ من النموذج

    # تحديد البرنامج التأهيلي بناءً على القيم المدخلة
    if behavior_score < 3:
        program = "برنامج محو الأمية"
    elif mental_state < 3:
        program = "برنامج تحسين المهارات الاجتماعية"
    elif skills < 3:
        program = "برنامج التدريب المهني"
    else:
        program = "برنامج دمج متقدم"

    # إعداد النتيجة النهائية: التنبؤ واسم البرنامج الموصى به
    result = {
        "التنبؤ": "عرضة للعودة" if prediction == 1 else "مستعد للاندماج",
        "البرنامج الموصى به": program
    }
    
    # إرسال النتيجة كـ JSON
    return jsonify(result)

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
