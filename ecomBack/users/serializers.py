"""
Serializers pour la gestion des utilisateurs dans l’API.
Inclut le serializer d’inscription et les méthodes de validation et création.
"""
# On importe le module serializers de Django REST Framework
from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouvel utilisateur.
    Permet de créer un compte utilisateur via l'API.
    """

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        """
        Valide que les deux mots de passe saisis par l'utilisateur sont identiques.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur après validation des données.
        """
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Méthode de validation globale pour vérifier que les deux mots de passe correspondent
def validate(self, attrs):
    """
    Valide que les deux mots de passe saisis par l'utilisateur sont identiques.

    Args:
        attrs (dict): Les données à valider.

    Raises:
        serializers.ValidationError: Si les mots de passe ne correspondent pas.

    Returns:
        dict: Les données validées.
    """
    
    if attrs['password'] != attrs['password2']:
        raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
    # Sinon, on retourne les données validées
    return attrs

# Méthode pour créer un nouvel utilisateur après validation
def create(self, validated_data):
    """
    Crée un nouvel utilisateur après validation des données.

    Args:
        validated_data (dict): Les données validées pour la création de l'utilisateur.

    Returns:
        User: L'utilisateur nouvellement créé.
    """
    validated_data.pop('password2')
    # On crée l'utilisateur avec les données validées (username, email, password)
    user = get_user_model().objects.create_user(**validated_data)
    # On retourne l'utilisateur créé
    return user