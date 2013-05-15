from models import RecordPermission


def user_permissions(user, model):
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
    if 'view' in kwargs:
        perms.canView = bool(kwargs['view'])
    if 'update' in kwargs:
        perms.canUpdate = bool(kwargs['update'])
    if 'delete' in kwargs:
        perms.canDelete = bool(kwargs['delete'])

    perms.save()
