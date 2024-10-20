from fastapi import FastAPI
from core.lifespan import lifespan
from core.config import engine
from core.config import Base
from routes import user

# Initialize the FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)

# Create the database tables on startup
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])
