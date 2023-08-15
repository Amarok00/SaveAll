# Модель блога\пост

``` class Post(models.Model):
    class Meta:```
        verbose_name = "Создать пост"  # Название модели отображаемое в административном интерфейсе - "Создать пост"
        verbose_name_plural = "Создать посты"  # Название модели во множественном числе - "Создать посты"

    title = models.CharField(max_length=200, help_text="Максимум 200 символов", db_index=True)
    # Поле для заголовка поста с максимальной длиной в 200 символов. 
    # Вспомогательный текст "Максимум 200 символов" будет отображаться в административном интерфейсе.
    # db_index=True создает индекс для данного поля в базе данных.

    content = RichTextField(max_length=5000, blank=True, null=True, help_text="Максимум 5000 символов")
    # Поле для содержания поста, использующее RichTextField.
    # Максимальная длина 5000 символов.
    # Поле может быть пустым (blank=True) или содержать значение null (null=True).
    # Вспомогательный текст "Максимум 5000 символов" будет отображаться в административном интерфейсе.

    data_create = models.DateTimeField(default=timezone.now)
    # Поле для хранения даты и времени создания поста по умолчанию используется текущая дата и время (timezone.now).

    data_update = models.DateTimeField(auto_now=True)
    # Поле для хранения даты и времени последнего обновления поста.
    # auto_now=True автоматически обновляет поле при сохранении объекта.

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Внешний ключ ForeignKey, используется для связи с моделью User.
    # on_delete=models.CASCADE означает, что при удалении связанного сущности User, будут удалены все связанные сущности Post.

    slug = models.SlugField(max_length=50)
    # Поле SlugField используется для создания URL-адресов, основанных на заголовке поста.
    # Максимальная длина 50 символов.

    likes = models.ManyToManyField(User, related_name="postcomment", blank=True)
    # Поле ManyToManyField, используется для отображения отношения "многие ко многим" между пользователями и постами.
    # Каждый пользователь может поставить лайк нескольким постам, и наоборот.
    # Связь модели User осуществляется через related_name.

    reply = models.ForeignKey("self", null=True, related_name="reply_ok", on_delete=models.CASCADE)
    # Внешний ключ ForeignKey, указывает на саму модель Post.
    # null=True означает, что поле может содержать значение null.
    # Относительное имя связи - "reply_ok".
    # on_delete=models.CASCADE означает, что при удалении связанного сущности Post, будут удалены все связанные сущности Post.
    
    def total_likes(self):
        return self.likes.count()
    # Метод, который возвращает общее количество лайков для поста.
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    # Метод, который возвращает абсолютную ссылку на пост.
    # reverse используется для получения URL по имени маршрута "post-detail" и передачи параметра pk текущего объекта.

    def __str__(self):
        return self.title
    # Метод, который определяет строковое представление модели.
    # Здесь возвращается заголовок поста при приведении объекта к строке.
