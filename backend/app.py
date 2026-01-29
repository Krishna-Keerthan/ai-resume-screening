from app import create_app
import os

app = create_app()

@app.route('/' , methods=['GET'])
def index():
    return "Successfully Runnning the Backend"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print("\n" + "="*50)
    print("🚀 Starting Flask Development Server")
    print("="*50)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Debug Mode: {debug}")
    print(f"Port: {port}")
    print(f"URL: http://localhost:{port}")
    print("="*50 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )