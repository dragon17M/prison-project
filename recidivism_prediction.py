import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. قراءة البيانات من ملف Excel
file_path = 'C:\\sqlite\\prison_project\\recidivism_prediction\\prisoners_data.xlsx'
data = pd.read_excel(file_path)

# 2. طباعة أول 5 صفوف للتأكد
print(data.head())

# 3. تقسيم البيانات إلى المدخلات والمخرجات
X = data.drop('recidivism', axis=1)
y = data['recidivism']

# 4. تقسيم البيانات إلى تدريب واختبار
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. بناء النموذج
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 6. تدريب النموذج على بيانات التدريب
model.fit(X_train, y_train)

# 7. توقع القيم على بيانات الاختبار
y_pred = model.predict(X_test)

# 8. حساب دقة النموذج
accuracy = accuracy_score(y_test, y_pred)
print(f"دقة النموذج: {accuracy * 100:.2f}%")

# 9. عرض تقرير مفصل عن أداء النموذج
print(classification_report(y_test, y_pred))

# 10. وظيفة تخصيص برنامج تأهيلي بناءً على تقييم السجين
def recommend_program(literacy, social_skills, vocational_skills):
    if literacy < 3:
        return "برنامج محو الأمية"
    elif social_skills < 3:
        return "برنامج تحسين المهارات الاجتماعية"
    elif vocational_skills < 3:
        return "برنامج التدريب المهني"
    else:
        return "برنامج دمج متقدم"

# 11. اختبار الوظيفة
program = recommend_program(2, 4, 3)
print(f"التوصية: {program}")  # النتيجة: برنامج محو الأمية

# 12. حفظ النموذج المدرب لاستخدامه لاحقًا
joblib.dump(model, 'recidivism_model.pkl')

# 13. تحميل النموذج المحفوظ (مثال)
# model = joblib.load('recidivism_model.pkl')
# new_prisoner = [[35, 1, 0, 5, 3]]  # مثال على بيانات سجين
# prediction = model.predict(new_prisoner)
# print("عرضة للعودة" if prediction[0] == 1 else "مستعد للاندماج")
