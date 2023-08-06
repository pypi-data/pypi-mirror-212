from django.dispatch import Signal

from audit_trails.models import Notification


class Notify:

    def info(self, actor_object_type, actor_object_id, recipients, **kwargs):
        Notification.objects.bulk_create([
            Notification(actor_object_type=actor_object_type, actor_object_id=actor_object_id, recipient=recipient, level='info', **kwargs)
            for recipient in recipients
        ])

    def success(self, actor_object_type, actor_object_id, recipients, **kwargs):
        Notification.objects.bulk_create([
            Notification(actor_object_type=actor_object_type, actor_object_id=actor_object_id, recipient=recipient, level='success', **kwargs)
            for recipient in recipients
        ])

    def warning(self, actor_object_type, actor_object_id, recipients, **kwargs):
        Notification.objects.bulk_create([
            Notification(actor_object_type=actor_object_type, actor_object_id=actor_object_id, recipient=recipient, level='warning', **kwargs)
            for recipient in recipients
        ])

    def error(self, actor_object_type, actor_object_id, recipients, **kwargs):
        Notification.objects.bulk_create([
            Notification(actor_object_type=actor_object_type, actor_object_id=actor_object_id, recipient=recipient, level='error', **kwargs)
            for recipient in recipients
        ])


notify = Notify()
