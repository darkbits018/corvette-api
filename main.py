from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

# Import your API routers
from routes import auth, users, roles, discover, templates, indices

app = FastAPI(title="SC-SIEM-Corvette API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for initial testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers in the main application
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(discover.router, prefix="/api/v1/discover", tags=["Discover"])
app.include_router(templates.router, prefix="/api/v1", tags=["Templates"])
app.include_router(indices.router, prefix="/api/v1/indices", tags=["Indices"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# --- FINAL DIAGNOSTIC: Print all registered routes --- #
print("\n--- Final Registered Application Routes ---")
for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")
print("-----------------------------------------\n")
