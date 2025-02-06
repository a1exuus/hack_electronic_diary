from datacenter.models import Mark, Lesson, Chastisement, Commendation, Schoolkid
from random import choice, randint


def get_schoolkid_card(child_name):
    child = Schoolkid.objects.get(full_name__contains=child_name)
    return child


def create_commendation(schoolkid, subject):                                                                         
    child = get_schoolkid_card(schoolkid)
    lessons = Lesson.objects.filter(subject__title=subject)
    lesson = choice(lessons)
    Commendation.objects.create(text='Хвалю!', created=lesson.date, schoolkid=child, subject=lesson.subject, teacher=lesson.teacher)


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid.id)
    for chastisement in chastisements:
        chastisement.delete()


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=schoolkid.id, points__in=[2, 3])
    for mark in marks:
        mark.points = randint(4, 5)
        mark.save()
