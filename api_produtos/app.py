from flask import Flask, request, render_template
from datetime import date
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

#######################################################
# 1. Cadastrar produtos
@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    mensagem = ''
    if request.method == 'POST':
        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        datacriacao = date.today()

        if descricao and precocompra and precovenda:
            registro = (descricao, precocompra, precovenda, datacriacao)
            try:
                conn = sqlite3.connect('database/db-produtos.db')
                sql = '''INSERT INTO produtos(descricao, precocompra, precovenda, datacriacao)
                         VALUES (?, ?, ?, ?)'''
                cur = conn.cursor()
                cur.execute(sql, registro)
                conn.commit()
                mensagem = 'Produto cadastrado com sucesso!'
            except Error as e:
                mensagem = f'Erro ao cadastrar: {e}'
            finally:
                conn.close()
    return render_template('cadastrar.html', mensagem=mensagem)

#######################################################
# 2. Listar produtos
@app.route('/produtos/listar', methods=['GET'])
def listar():
    try:
        conn = sqlite3.connect('database/db-produtos.db')
        sql = 'SELECT * FROM produtos'
        cur = conn.cursor()
        cur.execute(sql)
        registros = cur.fetchall()
        return render_template('listar.html', regs=registros)
    except Error as e:
        print(e)
    finally:
        conn.close()

#######################################################
# 3. Alterar produto
@app.route('/produtos/alterar/<int:idproduto>', methods=['GET', 'POST'])
def alterar(idproduto):
    conn = sqlite3.connect('database/db-produtos.db')
    cur = conn.cursor()
    if request.method == 'POST':
        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        sql = '''UPDATE produtos 
                 SET descricao=?, precocompra=?, precovenda=?
                 WHERE idproduto=?'''
        cur.execute(sql, (descricao, precocompra, precovenda, idproduto))
        conn.commit()
        conn.close()
        return render_template('mensagem.html', mensagem='Produto alterado com sucesso!')
    else:
        cur.execute('SELECT * FROM produtos WHERE idproduto=?', (idproduto,))
        produto = cur.fetchone()
        conn.close()
        return render_template('alterar.html', produto=produto)

#######################################################
# 4. Excluir produto
@app.route('/produtos/excluir/<int:idproduto>')
def excluir(idproduto):
    try:
        conn = sqlite3.connect('database/db-produtos.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM produtos WHERE idproduto=?', (idproduto,))
        conn.commit()
        mensagem = 'Produto excluído com sucesso!'
    except Error as e:
        mensagem = f'Erro ao excluir: {e}'
    finally:
        conn.close()
    return render_template('mensagem.html', mensagem=mensagem)

#######################################################
# Página de erro 404
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

#######################################################
# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
