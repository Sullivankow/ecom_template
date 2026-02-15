"""
Serializers pour la gestion des utilisateurs dans l’API.
Inclut le serializer d’inscription et les méthodes de validation et création.
"""
# On importe le module serializers de Django REST Framework
from rest_framework import serializers
import re
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
    
    def validate_password(self, value):
        """
        Valide la complexité du mot de passe utilisateur.
        Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule et un caractère spécial.

        Args:
            value (str): Le mot de passe à valider.

        Raises:
            serializers.ValidationError: Si le mot de passe ne respecte pas les critères de sécurité.

        Returns:
            str: Le mot de passe validé.
        """
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\\W).{8,}$', value):
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule et un caractère spécial."
            )
        return value
    
    def validate_email(self, value):
        """
        Valide le format de l'adresse e-mail et applique des règles de sécurité supplémentaires.
        L'adresse doit être valide, ne pas contenir d'espaces, ni de caractères suspects.

        Args:
            value (str): L'adresse e-mail à valider.

        Raises:
            serializers.ValidationError: Si l'adresse e-mail ne respecte pas les critères de sécurité.

        Returns:
            str: L'adresse e-mail validée.
        """
        import re
        # Regex stricte pour email : pas d'espaces, caractères spéciaux limités, format classique
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', value):
            raise serializers.ValidationError("Adresse e-mail invalide ou suspecte.")
        if ' ' in value:
            raise serializers.ValidationError("L'adresse e-mail ne doit pas contenir d'espaces.")
        # Optionnel : blacklist de domaines ou caractères
        # if value.endswith('@tempmail.com'):
        #     raise serializers.ValidationError("Les adresses temporaires ne sont pas autorisées.")
        return value

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