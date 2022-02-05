from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import OnlyContacted, Student

@receiver(post_save, sender=Student)
def change_profile(sender, instance, created, **kwargs):
    if created:
        only_contacted_id = instance.only_contacted.id
        only_contacted = get_object_or_404(OnlyContacted, id=only_contacted_id)
        only_contacted.update(has_been_student=True)



@receiver(pre_delete, sender=Student)
def change_profile_when_deleted(sender, instance, **kwargs):
    only_contacted_id = instance.only_contacted.id
    only_contacted = get_object_or_404(OnlyContacted, id=only_contacted_id)
    only_contacted.update(has_been_student=False)

