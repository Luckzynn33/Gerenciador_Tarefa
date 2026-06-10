from Gerenciador import database, app
from Gerenciador.models import Usuario, Tarefa

with app.app_context():
    database.create_all()