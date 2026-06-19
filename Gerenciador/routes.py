from flask import render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from Gerenciador import app, database, bcrypt
from Gerenciador.forms import FormLogin, FormCriarConta
from Gerenciador.models import Usuario


@app.route('/', methods=['GET', 'POST'])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for('perfil', id_usuario=usuario.id))
        else:
            flash('E-mail ou senha incorretos.', 'danger')
    return render_template('homepage.html', form=formLogin)


@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha_criptografada = bcrypt.generate_password_hash(formcriarconta.senha.data).decode('utf-8')

        usuario = Usuario(
            nome=formcriarconta.username.data,
            email=formcriarconta.email.data,
            senha=senha_criptografada,
            cargo=formcriarconta.cargo.data
        )

        database.session.add(usuario)
        database.session.commit()

        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('criarconta.html', form=formcriarconta)





@app.route('/perfil/<id_usuario>')
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get(int(id_usuario))
    if int(id_usuario) == (current_user.id):
        return render_template('perfil.html', usuario=current_user)
    else:
        usuario = Usuario.query.get(int(id))
        return render_template('perfil.html', usuario=usuario)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

