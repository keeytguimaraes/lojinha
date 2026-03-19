from flask import Flask

from routes.clientes_routes import cliente_bp
from routes.fornecedor_routes import fornecedor_bp
from routes.vendedor_routes import vendedor_bp
from routes.estoque_routes import estoque_bp
from routes.vendas_routes import vendas_bp

app = Flask(__name__)

app.register_blueprint(cliente_bp)
app.register_blueprint(fornecedor_bp)
app.register_blueprint(vendedor_bp)
app.register_blueprint(estoque_bp)
app.register_blueprint(vendas_bp)

if __name__ == "__main__":
    app.run(debug=True)