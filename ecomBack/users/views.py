# Importation des classes génériques de DRF pour créer des vues basées sur les classes.
from rest_framework import generics
# Importation du serializer d'inscription utilisateur.
from .serializers import RegisterSerializer
# Importation de la fonction pour récupérer le modèle utilisateur personnalisé.
from django.contrib.auth import get_user_model
# Importation du décorateur pour personnaliser la doc Swagger
from drf_yasg.utils import swagger_auto_schema


class RegisterView(generics.CreateAPIView):
	"""
	Vue d'API pour l'inscription d'un nouvel utilisateur.
	Hérite de CreateAPIView pour fournir automatiquement la méthode POST.
    
	Attributs :
		queryset : Définit l'ensemble des objets utilisateurs (CustomUser) sur lesquels la vue va opérer.
		serializer_class : Définit le serializer utilisé pour valider et créer l'utilisateur.
	"""
	queryset = get_user_model().objects.all()
	serializer_class = RegisterSerializer

	@swagger_auto_schema(operation_summary="Inscription d'un nouvel utilisateur")
	def post(self, request, *args, **kwargs):
		"""
		Crée un nouvel utilisateur à partir des données envoyées en POST.
		"""
		return super().post(request, *args, **kwargs)
