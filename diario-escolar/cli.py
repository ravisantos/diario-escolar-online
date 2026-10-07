import click
from flask.cli import with_appcontext


from services.usuarios import criar_usuario



@click.command('criar-admin')
@click.option('--nome', prompt='Nome')
@click.option('--email', prompt='E-mail')
@click.password_option('--senha', prompt='Senha')
@with_appcontext
def criar_admin(nome, email, senha):
    """Cria o primeiro usuário administrador."""
    try:
        usuario = criar_usuario(nome, email, senha, 'admin')
    except ValueError as erro:
        raise click.ClickException(str(erro))
    click.echo(f'Administrador criado: {usuario.email}')