from django.db.models.signals import post_save, pre_delete
from django.db.models import Sum
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import OnlyContacted, Student

@receiver(post_save, sender=Student)
def change_profile(sender, instance, created, **kwargs):
    if created:
        only_contacted_id = instance.only_contacted.id
        only_contacted = get_object_or_404(OnlyContacted, id=only_contacted_id)
        only_contacted.has_been_student=True
        only_contacted.save(update_fields=['has_been_student'])
# penalty_amount = instance.annotate(Sum('penalty__penalty_in_percent'))['penalty__penalty_in_percent__sum'] - this is not correct code
        #because we use annotate and aggreagate for queryset. Example: Teacher.objects.all().aggregate(Sum(experience))
        #the code written below returns dict like {''experience__sum':23}. To get value of dict we write code like this:
        #Teacher.objects.all().aggregate(Sum('experience')).get('experience__sum')
        penalty_amount = 0
        for obj in instance.penalty.all():
            penalty_amount += obj.penalty_in_percent
        total_payment_of_month = 0
        for obj in instance.penalty.all():
            total_payment_of_month += obj.cost_per_month
        if penalty_amount > 0:
            total_payment_of_month = penalty_amount * total_payment_of_month/100 + total_payment_of_month
            instance.total_payment_per_month=total_payment_of_month
            instance.save(update_fields=['total_payment_per_month'])
        elif penalty_amount < 0:#if it is discount
            total_payment_of_month = total_payment_of_month - penalty_amount*total_payment_of_month/100
            instance.total_payment_per_month=total_payment_of_month
            instance.save(update_fields=['total_payment_per_month'])
        elif penalty_amount==0:
            instance.total_payment_per_month=total_payment_of_month
            instance.save(update_fields=['total_payment_per_month'])

@receiver(pre_delete, sender=Student)
def change_profile_when_deleted(sender, instance, **kwargs):
    only_contacted_id = instance.only_contacted.id
    only_contacted = get_object_or_404(OnlyContacted, id=only_contacted_id)
    only_contacted.has_been_student = False
    only_contacted.save(update_fields=['has_been_student'])

