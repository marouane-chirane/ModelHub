import uvicorn
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def main():
    # Configuration du serveur
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() == "true"
    
    print("=" * 60)
    print("🚀 Starting ModelHub API")
    print("=" * 60)
    print(f"📡 API running at: http://{host}:{port}")
    print("📚 Available endpoints:")
    print("  🏠 API Root: /")
    print("  📊 Models: /api/v1/models")
    print("  📈 Time Series: /api/v1/time-series")
    print("  📖 API Documentation: /docs")
    print("  🔧 Interactive API: /redoc")
    print("=" * 60)
    print("🎯 API Features:")
    print("  • Model Management (CRUD)")
    print("  • Model Training")
    print("  • Time Series Analysis")
    print("  • Predictions")
    print("=" * 60)
    print("Press CTRL+C to quit")
    print("=" * 60)
    
    # Lancer le serveur
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    main() 