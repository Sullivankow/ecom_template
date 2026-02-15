# =========================
# SERVICES UTILISATEUR
# =========================

# ----- INSCRIPTION -----
# RegisterView : Vue d'inscription (POST /users/register/)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserUpdateSerializer, RegisterSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView



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

	@swagger_auto_schema(operation_summary="Inscription d'un nouvel utilisateur",tags=["Utilisateur"])
	def post(self, request, *args, **kwargs):
     
		"""
		Crée un nouvel utilisateur à partir des données envoyées en POST.
		"""
		return super().post(request, *args, **kwargs)


# ----- CONNEXION -----
# (À ajouter) LoginView : Vue de connexion (POST /api/token/ ou /login/)



from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

class LoginView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary="Connexion utilisateur (JWT)",
        operation_description="Obtenir un token d'accès et de rafraîchissement via login/mot de passe.",
        tags=["Utilisateur"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)








# ----- Modification PATCH -----
# (À ajouter) UserUpdateSerializer : Serializer pour la modification des informations utilisateur (PATCH /users/me/)
class UserSelfUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        request_body=UserUpdateSerializer,
        operation_summary="Modification du profil utilisateur",
        operation_description="Permet à l'utilisateur authentifié de modifier ses informations (PATCH).",
        tags=["Utilisateur"]
    )
    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        security=[{'Bearer': []}],
        request_body=UserUpdateSerializer,
        operation_summary="Remplacement complet du profil utilisateur",
        operation_description="Permet à l'utilisateur authentifié de remplacer toutes ses informations (PUT).",
        tags=["Utilisateur"]
    )
    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data)  # partial=False par défaut
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
    security=[{'Bearer': []}],
    operation_summary="Suppression du compte utilisateur",
    operation_description="Permet à l'utilisateur authentifié de supprimer définitivement son compte (DELETE).",
    tags=["Utilisateur"]
)
    def delete(self, request):
     user = request.user
     user.delete()
     return Response({"detail": "Compte supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
    
 
     

