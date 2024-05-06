from rest_framework.decorators import api_view
from rest_framework import status
from game.models import Word, Game
from game.serializers import WordSerializer, CustomUserSerializer
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication

@api_view(['GET'])
#Gerando token para as requisições do meu app
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrf_token': csrf_token})

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
def start_new_game(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        return Response({'message': user_id})
    else:
        return Response({'message': 'Usuário não está logado'}, status=status.HTTP_401_UNAUTHORIZED)

# Create your views here.
@api_view(['GET'])
def word_list(request):
    #Verificando metodo executado, caso não seja retornar o erro 405
    if request.method == 'GET':
        words =  Word.word_list()
        if words is not None:
            serializer = WordSerializer(words, many = True)
            return Response(serializer.data)
        else:
            return Response({'message': 'Lista vazia!'}) 
    return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def word_random_game(request):
    #Verificando metodo executado, caso não seja retornar o erro 405
    if request.method == 'GET':
        word_random = Game.random_word() 
        if word_random:
            serializer = WordSerializer(word_random)
            return Response(serializer.data)
        else:
            return Response({'message': 'Acabou as palavras!'}) 
    return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

 # Importe o serializador personalizado
@api_view(['POST'])
def api_login(request):
    if request.method == 'POST':
        # Obtenha os dados de autenticação da solicitação
        email_request = request.data.get('email')
        password_request = request.data.get('password')

        print(email_request)
        print(password_request)
        # Autenticar o usuário
        user = authenticate(request, email=email_request, password=password_request)
       
        if user is not None:
            # Login bem-sucedido
            login(request, user)  # Faça login com o usuário autenticado  
            request.session['user_id'] = user.id  # Armazene o ID do usuário na sessão
            # Serializar os dados do usuário
            serializer = CustomUserSerializer(user)
            # Retornar os dados do usuário na resposta da API
            return Response(serializer.data)
        else:
            # Login falhou
            return Response({'message': 'Credenciais inválidas'}, status = status.HTTP_401_UNAUTHORIZED)
    else:
        # Método de solicitação não suportado
        return Response({'message': 'Método não suportado'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)


