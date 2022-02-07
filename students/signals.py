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
        only_contacted.update(has_been_student=True)
        penalty_amount = instance.penalty.aggregate(Sum('penalty_in_percent')).get('penalty_in_percent__sum')
        total_payment_of_month = instance.courses.aggregate(Sum('cost_per_month')).get('cost_per_month__sum')
        if penalty_amount > 0:#if it is a penalty!
            total_payment_of_month = penalty_amount * total_payment_of_month/100 + total_payment_of_month
            instance.update(total_payment_per_month=total_payment_of_month)
        elif penalty_amount < 0:#if it is discount
            total_payment_of_month = total_payment_of_month - penalty_amount*total_payment_of_month/100
            instance.update(total_payment_per_month=total_payment_of_month)
        elif penalty_amount==0:
            instance.update(total_payment_per_month=total_payment_of_month)

@receiver(pre_delete, sender=Student)
def change_profile_when_deleted(sender, instance, **kwargs):
    only_contacted_id = instance.only_contacted.id
    only_contacted = get_object_or_404(OnlyContacted, id=only_contacted_id)
    only_contacted.update(has_been_student=False)

