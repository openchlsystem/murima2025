# apps/accounts/managers.py
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom manager for User model"""
    
    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a regular user"""
        if not username:
            raise ValueError(_('The Username field must be set'))
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('status', 'active')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(username, email, password, **extra_fields)
    
    def active(self):
        """Return only active users"""
        return self.filter(is_active=True, status='active')
    
    def agents(self):
        """Return only agents"""
        return self.filter(role='agent', is_active=True)
    
    def supervisors(self):
        """Return only supervisors"""
        return self.filter(role='supervisor', is_active=True)
    
    def managers(self):
        """Return only managers"""
        return self.filter(role='manager', is_active=True)
    
    def available_agents(self):
        """Return agents available for calls"""
        return self.filter(
            role='agent',
            is_active=True,
            is_online=True,
            agent_status__in=['available', 'busy']
        )
    
    def by_department(self, department):
        """Return users by department"""
        return self.filter(department=department, is_active=True)
    
    def online_users(self):
        """Return currently online users"""
        return self.filter(is_online=True, is_active=True)


class ActiveUserManager(models.Manager):
    """Manager that returns only active users"""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, status='active')