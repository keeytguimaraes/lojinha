from flask import Flask, render_template

# 🔹 Importando blueprints de cada módulo (entidade)
from routes.cliente_routes import cliente_bp
from routes.fornecedor_routes import fornecedor_bp
from routes.vendedor_routes import vendedor_bp
from routes.estoque_routes import estoque_bp
from routes.vendas_routes import vendas_bp

# 🔹 Criando a aplicação Flask
app = Flask(__name__)

# 🔹 Rota da página inicial
@app.route("/")
def index():

    return render_template("index.html")

#  Registrando os blueprints sem url_prefix (se não quebra o código)
app.register_blueprint(cliente_bp)
app.register_blueprint(fornecedor_bp)
app.register_blueprint(vendedor_bp)
app.register_blueprint(estoque_bp)
app.register_blueprint(vendas_bp)

# 🔹 Inicializa a aplicação
if __name__ == "__main__":
    app.run(debug=True)