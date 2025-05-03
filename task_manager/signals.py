from chat.consumer import notify_user
from notifications.models import Notification
from task_manager.models import Task
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Task)
def assign_task(sender, created, instance, **kwargs):
    if created:
        if instance.assign_to:
            Notification.objects.create(
                to_user=instance.assign_to,
                title='Assigned to task',
                descriptions=f'''Task {instance.title} has been assigned to you etc...'''
            )
            notify_user(instance.assign_to.id,
                        f'''Task {instance.title} has been assigned to you etc...''')
    else:
        if instance.assign_to:
            Notification.objects.create(
                to_user=instance.assign_to,
                title='Task Updated',
                descriptions=f'''
                Task {instance.title} has been updated
                {instance.description}'''
            )
            notify_user(instance.assign_to,
                        f'''Task {instance.title} has been assigned to you etc...''')
