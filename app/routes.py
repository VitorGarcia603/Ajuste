from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user
from app import app
from app.models import db, Usuario, Produto, MovimentacaoProduto
from datetime import datetime

@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Usuario.query.filter_by(email=email, senha=senha).first()
        if user:
            login_user(user)
            return redirect(url_for('lista_produtos'))
        else:
            error = 'Credenciais inválidas'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/produtos')
@login_required
def lista_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET','POST'])
@login_required
def novo_produto():
    if request.method == 'POST':
        p = Produto(
            nome=request.form['nome'],
            categoria=request.form['categoria'],
            preco_custo=float(request.form['preco_custo']),
            preco_venda_sugerido=float(request.form['preco_venda_sugerido']),
            peso=float(request.form['peso'] or 0),
            largura=float(request.form['largura'] or 0),
            altura=float(request.form['altura'] or 0),
            profundidade=float(request.form['profundidade'] or 0)
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('lista_produtos'))
    return render_template('novo_produto.html')

@app.route('/produto/<int:id>')
@login_required
def produto_detalhes(id):
    produto = Produto.query.get_or_404(id)
    return render_template('produto_detalhes.html', produto=produto)

@app.route('/produto/<int:id>/movimentar', methods=['GET','POST'])
@login_required
def nova_movimentacao(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        tipo = request.form['tipo']
        quantidade = int(request.form['quantidade'])
        descricao = request.form['descricao']
        mov = MovimentacaoProduto(tipo=tipo, quantidade=quantidade, descricao=descricao, data=datetime.utcnow(), produto_id=produto.id)
        if tipo == 'entrada':
            produto.estoque += quantidade
            produto.entradas += quantidade
        else:
            produto.estoque -= quantidade
            produto.saidas += quantidade
        produto.ultima_atualizacao = mov.data
        db.session.add(mov)
        db.session.commit()
        return redirect(url_for('produto_detalhes', id=id))
    return render_template('nova_movimentacao.html', produto=produto)

@app.route('/movimentacao/<int:id>/editar', methods=['GET','POST'])
@login_required
def editar_movimentacao(id):
    mov = MovimentacaoProduto.query.get_or_404(id)
    if request.method == 'POST':
        mov.tipo = request.form['tipo']
        mov.quantidade = int(request.form['quantidade'])
        mov.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('produto_detalhes', id=mov.produto_id))
    return render_template('editar_movimentacao.html', movimentacao=mov)

@app.route('/movimentacao/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_movimentacao(id):
    mov = MovimentacaoProduto.query.get_or_404(id)
    pid = mov.produto_id
    db.session.delete(mov)
    db.session.commit()
    return redirect(url_for('produto_detalhes', id=pid))

@app.route('/produto/<int:id>/editar', methods=['GET','POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.categoria = request.form['categoria']
        produto.preco_custo = float(request.form['preco_custo'])
        produto.preco_venda_sugerido = float(request.form['preco_venda_sugerido'])
        produto.peso = float(request.form['peso'] or 0)
        produto.largura = float(request.form['largura'] or 0)
        produto.altura = float(request.form['altura'] or 0)
        produto.profundidade = float(request.form['profundidade'] or 0)
        db.session.commit()
        return redirect(url_for('produto_detalhes', id=id))
    return render_template('editar_produto.html', produto=produto)