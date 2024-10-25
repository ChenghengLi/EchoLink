from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.lifespan import lifespan
from core.config import engine
from core.config import Base
from routes import user, test

# Initialize the FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)


# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Create the database tables on startup
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(test.router, prefix="/test", tags=["Test"])



