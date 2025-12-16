
import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mylablink_python.settings")
django.setup()

from api.models import TestType

def populate_test_types():
    test_types = [
        {"name": "تحليل دم شامل (CBC)", "description": "Complete Blood Count"},
        {"name": "تحليل سكر تراكمي (HbA1c)", "description": "Hemoglobin A1c - Diabetes Monitoring"},
        {"name": "وظائف كلى (Kidney Function)", "description": "Creatinine, Urea, etc."},
        {"name": "وظائف كبد (Liver Function)", "description": "ALT, AST, Bilirubin, etc."},
        {"name": "فيتامين د (Vitamin D)", "description": "25-Hydroxy Vitamin D"},
        {"name": "تحليل بول (Urine Analysis)", "description": "General Urine Examination"},
        {"name": "تحليل براز (Stool Analysis)", "description": "General Stool Examination"},
        {"name": "دهون ثلاثية وكوليسترول (Lipid Profile)", "description": "Cholesterol, Triglycerides, HDL, LDL"},
        {"name": "وظائف الغدة الدرقية (Thyroid Profile)", "description": "TSH, T3, T4"},
        {"name": "مخزون الحديد (Iron Profile)", "description": "Serum Iron, Ferritin, TIBC"},
        {"name": "فيتامين ب12 (Vitamin B12)", "description": "Vitamin B12 Level"},
        {"name": "تحليل حمل (Pregnancy Test)", "description": "Beta HCG (Blood/Urine)"},
        {"name": "جرثومة معدة (H. Pylori)", "description": "Helicobacter Pylori Antigen/Antibody"},
        {"name": "بروتين تفاعلي (CRP)", "description": "C-Reactive Protein - Inflammation Marker"},
        {"name": "سرعة تجلط (PT/INR)", "description": "Prothrombin Time / INR"},
        {"name": "فصيلة الدم (Blood Group)", "description": "ABO Grouping & Rh Factor"},
        {"name": "معامل روماتويد (Rheumatoid Factor)", "description": "RF Test"},
        {"name": "تحليل نقرس (Uric Acid)", "description": "Serum Uric Acid"},
        {"name": "فحص كالسيوم (Calcium)", "description": "Total & Ionized Calcium"},
        {"name": "فحص مغنيسيوم (Magnesium)", "description": "Serum Magnesium"},
        {"name": "أخرى (Other)", "description": "Other specialized tests"}
    ]

    print("Populating Test Types...")
    for test in test_types:
        obj, created = TestType.objects.get_or_create(
            name=test["name"],
            defaults={"description": test["description"]}
        )
        if created:
            print(f"Created: {test['name']}")
        else:
            print(f"Already exists: {test['name']}")

    print("Done!")

if __name__ == "__main__":
    populate_test_types()
