from django import template
# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter
def addclass(field, css):
        return field.as_widget(attrs={"class": css})


@register.filter
def addlabel(field, label):
    return field.as_widget(attrs={"label": label})

# синтаксис @register... , под которой описана функция addclass() -
# это применение "декораторов", функций, обрабатывающих функции
# мы скоро про них расскажем. Не бойтесь соб@к