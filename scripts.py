from datacenter.models import Mark, Lesson, Chastisement, Commendation, Schoolkid
from random import choice, randint
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_schoolkid_card(child_name):
    try: child = Schoolkid.objects.filter(full_name__contains=child_name).distinct().first()
    except ObjectDoesNotExist: raise ObjectDoesNotExist
    except MultipleObjectsReturned: raise MultipleObjectsReturned
    return child


def create_commendation(schoolkid, subject):                                                                         
    child = get_schoolkid_card(schoolkid)
    lessons = Lesson.objects.filter(subject__title=subject).order_by('-date')
    if lessons:
        lesson = choice(lessons)
        Commendation.objects.create(text='Хвалю!', created=lesson.date, schoolkid=child, subject=lesson.subject, teacher=lesson.teacher)
    else:
        raise()


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=randint(4, 5))