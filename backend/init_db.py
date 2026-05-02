"""
Initialize database tables.
Run this script to create all tables in the database.
"""
from app.core.database import Base, engine
from app.models.user import User
from app.models.tracked_product import TrackedProduct
from app.models.price_history import PriceHistory
from app.models.notification import Notification
from app.models.platform_error import PlatformError

def init_db():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_db()
