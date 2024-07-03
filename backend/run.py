from app import create_app, db
from app.models import Meeting

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Meeting': Meeting}

if __name__ == '__main__':
    app.run(debug=True)
