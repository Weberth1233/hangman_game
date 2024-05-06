from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email = None, name = None, password= None, **extra_fields):
        if not email:
            raise ValueError('O campo de e-mail é obrigatório')
        if not password:
            raise ValueError('O campo de senha é obrigatório')
        # Normalizando o email
        email_normalized = self.normalize_email(email)
        # Criando um novo usuário
        user = self.model(email=email_normalized, name=name, **extra_fields)
        # Criptografando senha
        user.set_password(password)
        # Salvando o usuário no banco de dados
        user.save()
        return user
    
class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    username = None

    objects = UserManager()
    #Campo deve ser usado para autenticar usuários durante o processo de login.
    USERNAME_FIELD = 'email'
    #Campos que serão obrigatórios ao criar um novo usuário
    REQUIRED_FIELDS =['name']

    def __str__(self) -> str:
        return self.name
    
    def get_user_by_id(id=None):
        try:
            if not id:
                ValueError('É necessário passar um id')
                return None
            
            user = CustomUser.objects.get(pk=id)
            if user:
                return user
            else:
                return None
        except Exception:
            return None
        
# Create your models here.
from django.utils import timezone 
import random
words_used = []

class Word(models.Model):
    word = models.CharField(max_length = 100)
    
    def __str__(self) -> str:
        return self.word
    
    def word_list():
        words = Word.objects.all()
        return words if words.count() > 0 else None

    def create_word(word = None):
        my_word = Word(word = word).save()
        return my_word
    
class Hint(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    hint = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return f'Palavra = {self.word.word} Dicas = {self.hint}'

class Game(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    victory = models.BooleanField(default=False)
    number_attempts = models.IntegerField(default=0)  
    difficulty = models.CharField(max_length=50, default="Easy")  
    score = models.IntegerField(default=0)  
    hints_used = models.IntegerField(default=0)  

    def __str__(self) -> str:
        return f"Palavra: {self.word}, Vitoria: {self.victory}, numero tentativas: {self.number_attempts}"    

    @staticmethod
    def random_word():
        global words_used
        #Pegando as palavras que não foram utilzadas ainda
        words_not_used = Word.objects.exclude(word__in=words_used)
        #Verificando se ainda a palavras novas
        if not words_not_used:
            return None
        #Escolgendo uma palavra aleatoria não usada
        word_random = random.choice(words_not_used)
        #Adicionando na lista de palavras novas
        words_used.append(word_random.word)
        return word_random
    

class Attempt(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    letter = models.CharField(max_length = 1)

    def __str__(self) -> str:
        return f"Jogo: {self.game}, letra: {self.letter}"

