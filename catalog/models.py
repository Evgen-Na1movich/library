import uuid

from django.db import models
from django.urls import reverse  # используется для генерации URL-адресов

# путем инверсии шаблонов URL-адресов
# Create your models here.
""""
Жанр представляет из себя ManyToManyField, так что книга может иметь 
несколько жанров, а жанр может иметь много книг. 
Автор объявляется через ForeignKey, поэтому в каждой книге будет только 
один автор, но у автора может быть много книг
"""


class Genre(models.Model):
    # класс, определяющий модель, наследующейся от класса Model
    name = models.CharField(max_length=100, help_text="Введите жанр книги")

    def __str__(self):
        """
        Строка для представления объекта Model (на сайте Admin и т.д.)

        """
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


class Book(models.Model):
    """
    Модель, представляющая книгу (но не конкретный экземпляр книги).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    # null=True, которое позволяет базе данных хранить значение Null , если автор не выбран,
    # on_delete = models.SET_NULL установит значение автора в Null, если связанная с автором запись будет удалена
    # Внешний ключ используется потому, что у книги может быть только один автор, а у авторов может быть несколько книг

    summary = models.TextField(max_length=1000, help_text='Введите краткое описание книги')
    # isbn = models.CharField('ISBN', max_length=13,
    #                         help_text='13 Character '
    #                                   '<a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для этой книги")

    # ManyToManyField используется потому, что жанр может содержать много книг.
    # Книги могут относиться ко многим жанрам.

    def display_genre(self):
        """
    Создает строку для жанра. Это необходимо для отображения жанра в Admin.        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    """"
    BookInstance представляет собой определённую копию книги, которую кто-то может брать взаймы,
    и включает информацию о том, доступна ли копия или в какой день она ожидается,
    «отпечаток» или сведения о версии, а также уникальный идентификатор книги в библиотеке
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор для данной книги во всей библиотеке")
    # UUIDField используется для поля id, чтобы установить его как primary_key для этой модели.
    # Этот тип поля выделяет глобальное уникальное значение для каждого экземпляра
    # (по одному для каждой книги, которую вы можете найти в библиотеке)

    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Обслуживание'),
        ('o', 'Во временном пользовании'),
        ('a', 'Доступно'),
        ('r', 'Зарезервировано'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Забронировать наличие')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)


