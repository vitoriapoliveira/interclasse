from logging import exception
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_jogador, tabela_jogos
from database import Jogador, Time,db_session, Partida

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos()
    partidas = tabela_jogos.select_todos()
    return render_template(
        "dashboard.html",
        total_jogadores=len(jogadores),
        total_times=len(times),
        total_partidas=len(partidas),
    )


@app.route("/jogadores")
def listar_jogadores(jogadores):
    jogadores=tabela_jogador.select_todos()
    return render_template("jogadores.html", jogadores=jogadores)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
        #Quando clicar no botão cadastrar
    if request.method == "POST":


        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None
        #2- verificar se foi digitado
        if not nome:
            flash("preencha o nome", "error")
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash("preencha a turma", "error")
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash("preencha o responsavel", "error")
            return redirect(url_for("novo_jogador"))
        if not time_id:
            flash("preencha o time_id", "error")
            #3- salvar no banco
        tabela_jogador.salvar(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))

    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos()

    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/times")
def listar_times():
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)

@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":
        #1-pegar os valores no form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        #2-verificar se foi digitado

        if not nome:
            flash("preencha o nome", "error")
            return redirect(url_for("novo_time"))
        if not turma:
            flash("preencha a turma", "error")
            return redirect(url_for("novo_time"))
        if not responsavel:
            flash("preencha o responsavel", "error")
            return redirect(url_for("novo_time"))
        #3- salvar no banco
        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

        times = tabela_time.select_todos()
        return render_template("times.html", times=times)




@app.route("/partidas")
def listar_partidas():
    partidas = tabela_jogos.select_todos()
    return render_template("partidas.html", partidas=partidas)
    # Buscar todos os times no banco


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        local = request.form.get("local", "").strip()
        if not time_casa_id:
            flash("preencha o time_casa_id", "error")
            return redirect(url_for("nova_partida"))
        if not time_visitante_id:
            flash("preencha o time_visitante_id", "error")
            return redirect(url_for("nova_partida"))
        if not gols_casa:
            flash("preencha o gols_casa", "error")
            return redirect(url_for("nova_partida"))
        if not gols_visitante:
            flash("preencha o gols_visitante", "error")
            return redirect(url_for("nova_partida"))
        if not data_partida:
            flash("preencha o data_partida", "error")
            return redirect(url_for("nova_partida"))
        tabela_jogos.salvar(time_casa_id = int(time_casa_id), time_visitante_id = int(time_visitante_id), gols_casa = int(gols_casa), gols_visitante=int(gols_visitante), data_partida=data_partida)
    times = tabela_time.select_todos()
    partidas =  tabela_jogos.select_todos()
    return render_template("partidas.html", partidas=partidas,times=times)

if __name__ == "__main__":
    app.run(debug=True)
