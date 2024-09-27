from apps import create_app

app = create_app()

@app.route("/")
def index():
    return {"msg": "Hello Flask"}
        
if __name__ == "__main__":
    app.run()
    
