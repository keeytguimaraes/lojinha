from flask import Flask, render_template, redirect, url_for, session
import os
from routes.auth_routes import auth_bp

# 🔹 Importando blueprints de cada módulo (entidade)
from routes.cliente_routes import cliente_bp
from routes.fornecedor_routes import fornecedor_bp
from routes.vendedor_routes import vendedor_bp
from routes.estoque_routes import estoque_bp
from routes.vendas_routes import vendas_bp
from routes.adm_routes import adm_bp

# 🔹 Criando a aplicação Flask
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()  # Chave segura para sessões (random 24 bytes hex)

# 🔹 Rota da página inicial
@app.route("/")
def index():
    # Se não estiver logado, manda para login
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    # Logado → renderiza home
    return render_template("index.html")

#  Registrando os blueprints sem url_prefix (se não quebra o código)
app.register_blueprint(cliente_bp)
app.register_blueprint(fornecedor_bp)
app.register_blueprint(vendedor_bp)
app.register_blueprint(estoque_bp)
app.register_blueprint(vendas_bp)
app.register_blueprint(adm_bp)
app.register_blueprint(auth_bp)

# 🔹 Inicializa a aplicação
if __name__ == "__main__":
    app.run(debug=True)