"""
Sérialiseurs pour l'API des utilisateurs
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Organization, Role, User, UserPreference


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ['created_at']


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les utilisateurs"""
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    preferences = UserPreferenceSerializer(read_only=True)
    
    class Meta:
        model = User
        # Unique name for OpenAPI schema to avoid conflict with tickets.serializers.UserSerializer
        ref_name = 'UsersUser'
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'organization', 'organization_name', 'role', 'role_name',
            'location', 'timezone', 'language', 'is_active', 'is_verified',
            'last_login', 'last_activity', 'created_at', 'preferences'
        ]
        read_only_fields = [
            'id', 'last_login', 'last_activity', 'created_at', 'is_verified'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création d'utilisateurs"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm',
            'phone', 'organization', 'role', 'location', 'timezone', 'language'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour des utilisateurs"""
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'organization', 
            'role', 'location', 'timezone', 'language', 'is_active'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """Sérialiseur pour le changement de mot de passe"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Sérialiseur pour la connexion"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Identifiants invalides.")
            if not user.is_active:
                raise serializers.ValidationError("Compte désactivé.")
            attrs['user'] = user
        else:
            raise serializers.ValidationError("Username et password requis.")
        
        return attrs


class UserStatsSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques utilisateur"""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    verified_users = serializers.IntegerField()
    users_by_organization = serializers.DictField()
    users_by_role = serializers.DictField()
    recent_logins = serializers.IntegerField()
