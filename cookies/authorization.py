from functools import wraps
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q, QuerySet
from django.http import HttpResponseForbidden
from django.utils.decorators import available_attrs

from guardian.shortcuts import (get_perms, remove_perm, assign_perm,
                                get_objects_for_user)
from guardian.utils import get_user_obj_perms_model

from collections import defaultdict
from itertools import chain

logger = settings.LOGGER


AUTHORIZATIONS = [
    ('change_resource', 'Change resource'),
    ('view_resource', 'View resource'),
    ('delete_resource', 'Delete resource'),
    ('change_authorizations', 'Change authorizations'),
    ('view_authorizations', 'View authorizations'),
]

COLLECTION_AUTHORIZATIONS = [
    ('change_collection', 'Change collection'),
    ('view_resource', 'View collection'),
    ('delete_collection', 'Delete collection'),
    ('change_authorizations', 'Change authorizations'),
    ('view_authorizations', 'View authorizations'),
]


def is_owner(user, obj):
    """
    Evaluates whether or not ``user`` is the owner of ``obj``. At the moment
    this just means that the user is the creator of the object, but we may
    switch to something more explicit later on.

    Parameters
    ----------
    user : :class:`django.contrib.auth.models.User`
    obj : Instance of :class:`django.models.Model` subclass.

    Returns
    -------
    bool
    """
    return getattr(obj, 'created_by', None) == user or user.is_superuser


def check_authorization(auth, user, obj):
    """
    Check whether ``user`` is authorized to perform ``auth`` on ``obj``.
    """
    if auth == 'is_owner':
        return is_owner(user, obj)
    if auth == 'view_resource' and getattr(obj, 'public', False):
        return True
    return user.is_superuser or is_owner(user, obj) or user.has_perm(auth, obj)


def update_authorizations(auths, user, obj, by_user=None, propagate=True):
    """
    obj can be a queryset
    """

    if type(obj) is QuerySet:
        for auth in auths:
            assign_perm(auth, user, obj)
        return
    else:
        for auth in set(get_perms(user, obj)) - set(auths):
            remove_perm(auth, user, obj)
        for auth in set(auths) - set(get_perms(user, obj)):
            assign_perm(auth, user, obj)

    if not propagate:
        return

    if type(obj).__name__ == 'Collection':
        resource_auths = [auth.replace('collection', 'resource') for auth in auths]
        resources = obj.resources.all()
        if by_user:
            resources = apply_filter(by_user, 'change_authorizations', resources)
        update_authorizations(resource_auths, user, resources, by_user=by_user)
    elif type(obj).__name__ == 'Resource':
        relation_auths = [auth.replace('resource', 'relation') for auth in auths]
        relations_from = obj.relations_from.all()
        relations_to = obj.relations_to.all()
        if by_user:
            relations_from = apply_filter(by_user, 'change_authorizations', relations_from)
            relations_to = apply_filter(by_user, 'change_authorizations', relations_to)

        update_authorizations(relation_auths, user, relations_from, by_user=by_user)
        update_authorizations(relation_auths, user, relations_to, by_user=by_user)
    elif type(obj).__name__ == 'Relation':
        entity_auths = [auth.replace('relation', 'conceptentity')
                        if auth != 'view_relation' else 'view_entity'
                        for auth in auths]
        for field in ['source', 'target']:
            related_obj = getattr(obj, field)
            if type(related_obj).__name__ == 'ConceptEntity':
                if by_user and not by_user.has_perm('change_authorizations', related_obj):
                    continue
                update_authorizations(entity_auths, user, related_obj, by_user=by_user)




def list_authorizations(obj, user=None):
    """
    List authorizations for ``obj``.
    """
    if user is None:    # All authorizations for all users.
        _auths = defaultdict(list)
        _users = {obj.created_by.id: obj.created_by}
        _auths[obj.created_by.id].append('owns')


        for user in User.objects.all():
            _auths[user.id] += get_perms(user, obj)
            _users[user.id] = user

        return [(_users[user], auths) for user, auths in _auths.items() if auths]

    # Authorizations for a specific user.
    return get_perms(user, obj)


def authorization_required(perm, fn=None, login_url=None, raise_exception=False):
    """
    Decorator for views. Checks ``perm`` on an object ``fn`` for the requesting
    :class:`.User`\.
    """
    def decorator(view_func):

        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            obj = fn(request, *args, **kwargs) if callable(fn) else fn
            if not check_authorization(perm, request.user, obj):
                if raise_exception:
                    msg = '%s on %s not authorized for %s' % \
                          (perm, obj.__unicode__(), request.user.username)
                    raise PermissionDenied(msg)
                # TODO: make this pretty and informative.
                return HttpResponseForbidden('Nope.')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def apply_filter(user, auth, queryset):
    """
    Limit ``queryset`` to those objects for which ``user`` has ``permission``.

    Parameters
    ----------
    user : :class:`django.contrib.auth.models.User`
    permission : str
    queryset : :class:`django.db.models.QuerySet`

    Returns
    -------
    :class:`django.db.models.QuerySet`

    """

    if user.is_superuser:
        return queryset
    if type(queryset) is list:
        return [obj for obj in queryset if check_authorization(auth, user, obj)]
    if auth == 'is_owner':
        return queryset.filter(created_by_id=user.id)
    return get_objects_for_user(user, auth, queryset)
