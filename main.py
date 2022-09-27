import json
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen


class CardPopCadastro(MDCard):

    def __init__(self, mensagem, **kwargs):
        super().__init__(**kwargs)
        self.ids.mensagem.text = mensagem

    def fechar(self):
        self.parent.remove_widget(self)


class CardSenha(MDCard):

    def fechar(self):
        self.parent.remove_widget(self)


class Principal(MDScreen):
    def login(self):
        self.parent.current = 'login'


class Login(MDScreen):

    def on_leave(self, *args):
        self.ids.usuario.text = ''
        self.ids.senha.text = ''

    def abrir_card(self):
        self.add_widget(CardSenha())

    def abrir_PopUpCadastro(self, mensagem):
        self.add_widget(CardPopCadastro(mensagem))


class Registrar(MDScreen):

    def on_leave(self, *args):
        self.ids.user.text = ''
        self.ids.senha.text = ''
        self.ids.confirmacao_senha.text = ''

    def abrir_PopUpCadastro(self, mensagem):
        self.add_widget(CardPopCadastro(mensagem))

    def login(self):

        self.parent.current = 'login'


class Program(MDApp):
    usuarios = {}
    path = ''
    usuario_vazio = False
    senha_vazio = False

    def on_pre_enter(self):
        self.path = MDApp.get_running_app().user_data_dir+'/'

    def logar(self, usuario, senha):
        usuario = usuario.strip()
        senha = senha.strip()
        if usuario not in self.usuarios:
            self.get_running_app().root.ids.gerenciador.get_screen('login').abrir_PopUpCadastro('Usuário não cadastrado')
        elif senha == self.usuarios[usuario]:
            self.get_running_app().root.ids.gerenciador.current = 'principal'
        else:
            self.get_running_app().root.ids.gerenciador.get_screen('login').abrir_PopUpCadastro(
                    'Senha incorreta!!!')

    def registrar(self, usuario, senha, confirmacao_senha):
        usuario = usuario.strip()
        senha = senha.strip()
        if usuario == '':
            self.get_running_app().root.ids.gerenciador.get_screen('registrar').abrir_PopUpCadastro('O campo usuário não pode ser vazio!!!')

        else:
            if usuario in self.usuarios:
                self.get_running_app().root.ids.gerenciador.get_screen('registrar').abrir_PopUpCadastro('Usuario já cadastrado!!!')
            else:
                if senha.strip() == '':
                    self.get_running_app().root.ids.gerenciador.get_screen('registrar').abrir_PopUpCadastro(
                        'O campo senha não pode estar vazio!!!')
                elif len(senha.strip()) <= 5:
                    self.get_running_app().root.ids.gerenciador.get_screen('registrar').abrir_PopUpCadastro(
                        'A senha deve conter de 6 a 15 caracteres')
                elif senha == confirmacao_senha:
                    self.usuarios[usuario] = senha
                    self.saveData()
                    self.get_running_app().root.ids.gerenciador.current = 'login'

                else:
                    self.get_running_app().root.ids.gerenciador.get_screen('registrar').abrir_PopUpCadastro(
                        'As Senhas estão diferentes')

    def loadData(self):
        try:
            with open(self.path+'data.json', 'r') as data:
                self.usuarios = json.load(data)
        except FileNotFoundError:
            pass

    def saveData(self):

        with open(self.path+'data.json', 'w') as data:
            json.dump(self.usuarios, data)

    def redefinir_senha(self, usuario, senha, confirmacao_senha,card):
        usuario = usuario.strip()
        senha = senha.strip()

        if usuario in self.usuarios:

            if senha == '':
                self.get_running_app().root.ids.gerenciador.get_screen('login').abrir_PopUpCadastro(
                    'A senha não pode estar vazia!!!')
            elif len(senha.strip()) <= 5:
                self.get_running_app().root.ids.gerenciador.get_screen('login').abrir_PopUpCadastro(
                    'A senha deve conter de 6 a 15 caractere!!!')
            elif senha == confirmacao_senha:
                self.usuarios[usuario] = senha
                self.saveData()
                card.fechar()

            else:
                self.get_running_app().root.ids.gerenciador.get_screen('login').abrir_PopUpCadastro(
                    'As senhas não são identicas!!!')
        else:
            self.get_running_app().root.ids.gerenciador.get_screen('login').abrir_PopUpCadastro(
                'Usuario não cadastrado!!!')

    def dark_light(self):
        if self.theme_cls.theme_style == 'Dark':
            self.theme_cls.theme_style = 'Light'
        else:
            self.theme_cls.theme_style = 'Dark'

    def build(self):
        self.loadData()
        self.theme_cls.primary_palette = 'Orange'
        return Builder.load_file('main.kv')


if __name__ == '__main__':
    Program().run()
