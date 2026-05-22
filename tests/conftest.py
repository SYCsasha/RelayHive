"""Test configuration and fixtures."""

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.db.base import Base, get_db
from app.main import app


# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def engine():
    """Create test database engine for each test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """Create test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    # Clean up
    app.dependency_overrides.clear()
    session.close()


@pytest.fixture
def client(db_session):
    """Create test client."""
    from fastapi.testclient import TestClient
    return TestClient(app)
