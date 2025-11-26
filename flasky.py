from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conexao():
    return sqlite3.connect("banco.db")

def criar_tabela():
    con = conexao()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pessoa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL
        )
    """)
    con.commit()
    con.close()

criar_tabela()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]

        con = conexao()
        cur = con.cursor()
        cur.execute("INSERT INTO pessoa (nome, idade) VALUES (?, ?)", (nome, idade))
        con.commit()
        con.close()

        return redirect("/lista")

    return render_template("form.html")

@app.route("/lista")
def lista():
    con = conexao()
    cur = con.cursor()
    cur.execute("SELECT * FROM pessoa")
    dados = cur.fetchall()
    con.close()

    return render_template("lista.html", dados=dados)


if __name__ == "__main__":
    app.run(debug=True)
