from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.roles.models import (
    Role,
    RolePermission,
    SensitivityCategory,
    SensitivitySubcategory,
)

def seed_sensitivity_data():
    db: Session = SessionLocal()

    # -------------------------
    # Clear existing data
    # -------------------------
    db.query(RolePermission).delete(synchronize_session=False)
    db.query(Role).delete(synchronize_session=False)
    db.query(SensitivitySubcategory).delete(synchronize_session=False)
    db.query(SensitivityCategory).delete(synchronize_session=False)
    db.commit()

    # -------------------------
    # Create Categories
    # -------------------------
    pii = SensitivityCategory(name="PII")
    financial = SensitivityCategory(name="Financial")
    legal = SensitivityCategory(name="Legal")
    db.add_all([pii, financial, legal])
    db.commit()

    db.refresh(pii)
    db.refresh(financial)
    db.refresh(legal)

    # -------------------------
    # PII Subcategories
    # -------------------------
    pii_subs = [
        "Names",
        "Phone numbers",
        "Emails",
        "Passwords",
        "Addresses",
        "Postcodes",
        "Number plates",
        "IP address",
        "MAC address"
    ]
    pii_subcategory_objs = []
    for name in pii_subs:
        sub = SensitivitySubcategory(
            name=name,
            sensitivity_category_id=pii.sensitivity_category_id
        )
        db.add(sub)
        pii_subcategory_objs.append(sub)

    # -------------------------
    # Financial Subcategories
    # -------------------------
    financial_subs = [
        "IBANs",
        "VAT numbers",
        "Payment transactions"
    ]
    financial_subcategory_objs = []
    for name in financial_subs:
        sub = SensitivitySubcategory(
            name=name,
            sensitivity_category_id=financial.sensitivity_category_id
        )
        db.add(sub)
        financial_subcategory_objs.append(sub)

    # -------------------------
    # Legal Subcategories
    # -------------------------
    legal_subs = [
        "Contracts",
        "Court Records",
        "NDAs",
        "Legal Claims",
        "Compliance Documents"
    ]
    legal_subcategory_objs = []
    for name in legal_subs:
        sub = SensitivitySubcategory(
            name=name,
            sensitivity_category_id=legal.sensitivity_category_id
        )
        db.add(sub)
        legal_subcategory_objs.append(sub)

    db.commit()

    # -------------------------
    # Create Default Roles
    # -------------------------
    default_roles = [
        ("PII Role", pii_subcategory_objs),
        ("Financial Role", financial_subcategory_objs),
        ("Legal Role", legal_subcategory_objs),
    ]

    for role_name, subcategory_list in default_roles:
        role = Role(name=role_name)
        db.add(role)
        db.commit()
        db.refresh(role)

        # Assign default threshold 50 for each subcategory
        for sub in subcategory_list:
            perm = RolePermission(
                role_id=role.role_id,
                sensitivity_subcategory_id=sub.sensitivity_subcategory_id,
                threshold=50
            )
            db.add(perm)

    db.commit()
    db.close()

    print("All existing data cleared and sensitivity data seeded successfully.")

if __name__ == "__main__":
    seed_sensitivity_data()
