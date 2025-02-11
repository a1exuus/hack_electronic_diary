from datacenter.models import Mark, Lesson, Chastisement, Commendation, Schoolkid
from random import choice, randint
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_schoolkid_card(child_name):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name).unique()
    except ObjectDoesNotExist:
        raise('Такого ученика не существует!')
    except MultipleObjectsReturned:
        raise('Учеников с таким именем более 2-х. Попытайтесь ввести полное ФИО')
    return child


def create_commendation(schoolkid, subject):                                                                         
    child = get_schoolkid_card(schoolkid)
    try:
        lessons = Lesson.objects.filter(subject__title=subject).order_by('-date')
    except ObjectDoesNotExist:
        raise('Такого урока не существует!')
    lesson = choice(lessons)
    Commendation.objects.create(text='Хвалю!', created=lesson.date, schoolkid=child, subject=lesson.subject, teacher=lesson.teacher)


def remove_chastisements(schoolkid):
    for chastisement in Chastisement.objects.filter(schoolkid=schoolkid):
        chastisement.delete()


def fix_marks(schoolkid):
    for mark in Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]):
        mark.points = randint(4, 5)
        mark.save()
