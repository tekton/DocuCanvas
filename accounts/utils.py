from accounts.forms import PermissionForm
from models import RecordPermission


def user_permissions(user, model):
    if user.is_superuser:
        return (True, True, True)

    perms = RecordPermission.objects.get_for_model_user(model, user)
    return (perms.canView, perms.canUpdate, perms.canDelete)


def user_can_view(user, model):
    return user_permissions(user, model)[0]


def user_can_update(user, model):
    return user_permissions(user, model)[1]


def user_can_delete(user, model):
    return user_permissions(user, model)[2]


def set_permissions(user, model, **kwargs):
    perms = RecordPermission.objects.get_for_model_user(model, user)
    updated = perms.pk is None

    if 'view' in kwargs and perms.canView ^ bool(kwargs['view']):
        updated = True
        perms.canView = bool(kwargs['view'])
    if 'update' in kwargs and perms.canUpdate ^ bool(kwargs['update']):
        updated = True
        perms.canUpdate = bool(kwargs['update'])
    if 'delete' in kwargs and perms.canDelete ^ bool(kwargs['delete']):
        updated = True
        perms.canDelete = bool(kwargs['delete'])

    if not perms.canView and not perms.canUpdate and not perms.canDelete:
        if perms.pk is not None:
            perms.delete()
    elif updated:
        perms.save()


def set_permissions_for_model(model, view_users=[], update_users=[], delete_users=[]):
    perms = RecordPermission.objects.get_for_model(model)
    userPerms = {}
    for perm in perms:
        userPerms[perm.user] = perm

    for user in set(list(view_users) + list(update_users) + list(delete_users)) - set(userPerms.keys()):
        userPerms[user] = RecordPermission()
        userPerms[user].record = model
        userPerms[user].user = user

    for user in userPerms:
        userPerms[user].canView = user in view_users
        userPerms[user].canUpdate = user in update_users
        userPerms[user].canDelete = user in delete_users

        if not userPerms[user].canView and not userPerms[user].canUpdate and not userPerms[user].canDelete:
            userPerms[user].delete()
        else:
            userPerms[user].save()


def get_permission_form_for_model(model):
    q = RecordPermission.objects.get_for_model(model).select_related("user")
    users = {"view_users": [], "update_users": [], "delete_users": []}
    for perm in q:
        if perm.canView:
            users['view_users'].append(perm.user)
        if perm.canUpdate:
            users['update_users'].append(perm.user)
        if perm.canDelete:
            users['delete_users'].append(perm.user)

    return PermissionForm(users)
