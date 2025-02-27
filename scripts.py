from datacenter.models import Mark, Lesson, Chastisement, Commendation, Schoolkid
from random import choice, randint
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_schoolkid_card(child_name):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except ObjectDoesNotExist:
        raise ValueError(f"Ученик с именем '{child_name}' не найден.")
    except MultipleObjectsReturned:
        raise ValueError(f"Найдено несколько учеников с именем '{child_name}', уточните запрос.")

    return child


def create_commendation(schoolkid, subject):
    if schoolkid:                                                                    
        child = get_schoolkid_card(schoolkid)
        lessons = Lesson.objects.filter(subject__title=subject).order_by('-date')
        if lessons:
            lesson = choice(lessons)
            Commendation.objects.create(text='Хвалю!', created=lesson.date, schoolkid=child, subject=lesson.subject, teacher=lesson.teacher)
        else:
            raise ValueError('Уроков по данному предсету не существует. Проверьте правильность написания названия предмета')
    else:
        raise ValueError('Ученика с данным именем не существует!')


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def fix_marks(schoolkid):
    if schoolkid:
        Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=randint(4, 5))
    else:
        raise ValueError(f'Данного ученика не существует!')
