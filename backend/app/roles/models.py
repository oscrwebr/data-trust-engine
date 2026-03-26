from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Role(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    name = Column(String(128), nullable=False)

class SensitivityCategory(Base):
    __tablename__ = "sensitivity_category"

    sensitivity_category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)


class SensitivitySubcategory(Base):
    __tablename__ = "sensitivity_subcategory"

    sensitivity_subcategory_id = Column(Integer, primary_key=True, index=True)
    sensitivity_category_id = Column(Integer, ForeignKey("sensitivity_category.sensitivity_category_id"))
    name = Column(String(128), nullable=False)


class RolePermission(Base):
    __tablename__ = "role_permission"

    role_permission_id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.role_id"))
    threshold = Column(Integer, nullable=True)
    sensitivity_subcategory_id = Column(
        Integer,
        ForeignKey("sensitivity_subcategory.sensitivity_subcategory_id")
    )

class UserRole(Base):
    __tablename__ = "user_role" 
    user_role_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    role_id = Column(Integer, ForeignKey("role.role_id"))

class PendingUserRole(Base):
    __tablename__ = "pending_user_role" 
    pending_user_role_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("pending_users.user_id"))
    role_id = Column(Integer, ForeignKey("role.role_id"))