from flask import Blueprint, render_template, request, redirect
from models.adm.adm_insert import inserir_adm
from models.adm.adm_select import listar_adms, buscar_adm_por_id
from models.adm.adm_update import atualizar_adm
from models.adm.adm_delete import deletar_adm

adm_bp = Blueprint("adm", __name__)

# 🔹 LISTAR
@adm_bp.route("/adms")
def listar():
    adms = listar_adms()
    return render_template("adm/listar_adm.html", adms=adms)


# 🔹 CADASTRAR
@adm_bp.route("/adms/novo", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        data_nascimento = request.form["data_nascimento"]

        inserir_adm(nome, cpf, email, data_nascimento)
        return redirect("/adms")

    return render_template("adm/cadastro_adm.html")


# 🔹 EDITAR
@adm_bp.route("/adms/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        data_nascimento = request.form["data_nascimento"]

        atualizar_adm(id, nome, cpf, email, data_nascimento)
        return redirect("/adms")

    adm = buscar_adm_por_id(id)
    return render_template("adm/editar_adm.html", adm=adm)


# 🔹 DELETAR
@adm_bp.route("/adms/deletar/<int:id>")
def deletar(id):
    deletar_adm(id)
    return redirect("/adms")