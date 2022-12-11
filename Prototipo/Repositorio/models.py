from django.db import models

# Create your models here.

class ModelBase(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    tiempo = models.DateTimeField(auto_now_add=True)
    actualizar = models.DateTimeField(auto_now=True)

    class Meta:
	    abstract = True

class Usuario(ModelBase):
    user_name = models.CharField(max_length=30)
    user_password = models.CharField(max_length=100)
    user_image = models.ImageField(upload_to="images/", null=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Canal(ModelBase):
    canal_users = models.ManyToManyField(Usuario, blank=True, through="Membership")
    canal_code = models.CharField(max_length=6, editable=False, default="000aaa")
    canal_name = models.CharField(max_length=100, default="Grupo de Amigos", editable=True)

    def __str__(self):
        return self.canal_code
    
    class Meta:
        verbose_name = "Canales"
        verbose_name_plural = "Canales"

class Archivo(ModelBase):
    archivo = models.FileField(upload_to="pdfs/" ,null=False, blank=True )
    titulo = models.CharField(max_length=150, editable=True)
    descripcion = models.CharField(max_length=1000000, editable=True)
    categoria = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    canal = models.ForeignKey(Canal, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    vistas = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    lista = list()

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"

class Comentarios(ModelBase):
    cm_texto = models.CharField(max_length=1000000)
    cm_archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
    cm_user = models.CharField(max_length=1000000, default='desconocido')

    def __str__(self):
        return self.cm_texto

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

class Mensaje(ModelBase):
    ms_text = models.CharField(max_length=1000000)
    ms_user = models.CharField(max_length=1000000)
    ms_canal = models.ForeignKey(Canal, on_delete=models.CASCADE)

    def __str__(self):
        return self.ms_text

    class Meta:
        verbose_name = "Mensajes"
        verbose_name_plural = "Mensajes"


class Membership(ModelBase):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    canal = models.ForeignKey(Canal, on_delete=models.CASCADE)

