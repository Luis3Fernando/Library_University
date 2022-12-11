from distutils import archive_util
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import random
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import View
# Create your views here.
#no olvides hacer codigo para el login y eliminar salas inecesarias

def Home(request, username_id, code):
    usuario = Usuario.objects.get(id=username_id)
    sala = Canal.objects.get(canal_code=code)
    messages = Mensaje.objects.filter(ms_canal=sala)

    integrantes = []

    for i in Membership.objects.all():
        if (i.canal == sala) and (i.usuario!=usuario):
            integrantes.append(i.usuario)

    data = {
        'usuario': usuario,
        'sala': sala,
        'messages': messages,
        'miembros': integrantes
    }
    return render(request, "Home.html", data)

def Login(request):
    return render(request, "form_login.html")

def Registrarse(request):
    return render(request, "form_register.html")

def sala1(request, id_user):
    data = {
        "id_user" : id_user,
    }
    return render(request, "canal_main.html", data)

def sala2(request):
    identificador = request.POST["id_user"]
    identificador = int(identificador)
    code= ""
    code_value = []
    valores = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    
    for i in range(6):
        num = random.randint(0, 34) 
        code_value.append(num)

    for i in code_value:
        for j in range(34):
            if i == j:
                code = code + valores[j]
                break

    code = code.upper()

    sala = Canal.objects.create(canal_code=code)
    sala.save()

    data = {
        'identificador': identificador,
        'codigo': code
    }

    return render(request, "canal_create.html", data)

def subir(request, username_id, code):
    data = {
        'username_id': username_id,
        'code': code
    }
    return render(request, "subir_archivo.html", data)

def Mis_Archivos(request, username_id, code):
    user = Usuario.objects.get(id=username_id)
    archivos = Archivo.objects.filter(usuario=user)
    data = {
        'username_id': username_id,
        'code': code,
        'archivos':archivos,
        'content_type':'text/plain'
    }
    return render(request, "mostrar_archivos.html", data)

def Mostrar_Archivos(request, username_id, code):
    sala = Canal.objects.get(canal_code=code)
    archivos = Archivo.objects.filter(canal=sala)
    data = {
        'username_id': username_id,
        'code': code,
        'archivos':archivos,
        'content_type':'text/plain'
    }
    return render(request, "mostrar_archivos.html", data)

def Resultado_Busquedas(request):
    if request.POST["palabra"]:
        palabra = request.POST["palabra"]
        username_id = request.POST["username_id"]
        code = request.POST["code"]
        sala = Canal.objects.get(canal_code=code)
        arc = Archivo.objects.filter(canal=sala)

        archivos = []
        palabra = palabra.lower()
        for i in arc:
            if palabra in i.titulo.lower():
                archivos.append(i)

        data = {
            'username_id': username_id,
            'code': code,
            'archivos':archivos,
            'content_type':'text/plain'
        }
        return render(request, "mostrar_archivos.html", data)

    else:
        return HttpResponse("No introdujiste nada, regresa y vuelve a intentarlo")

def Archivo_personal(request, id_post, username_id):
    post = Archivo.objects.get(id=id_post)
    comments = Comentarios.objects.filter(cm_archivo = post)
    user = Usuario.objects.get(id=username_id)
    
    if user.user_name in post.lista:
        pass

    else:
        post.lista.append(user.user_name)
        post.vistas += 1
        post.save()

    data = {
        'comentarios': comments,
        'post': post,
        'usuario_main': username_id
    }
    return render(request, "archivo.html", data)

def Chekview1(request):
    if request.POST['nombre'] and request.POST['contra']:
        user = request.POST['nombre']
        contra = request.POST['contra']

        try:
            usuario_login = Usuario.objects.get(user_name=user, user_password=contra)
        except ObjectDoesNotExist:
            usuario_login = None

        if usuario_login == None:
            return HttpResponse("Tus datos no son validos, regresa y vuelve a intentarlo")

        else:
            print(f"Usuario {user} inició sesión: {datetime.now}")
            bandera = False
            
            for i in Membership.objects.all():
                if i.usuario == usuario_login:
                    afiliacion = i
                    bandera = True
                    break
            


            if bandera==False:
                return redirect("sala1/"+str(usuario_login.id))

            else:
                canal = afiliacion.canal
                return redirect('home/'+str(usuario_login.id)+'/'+canal.canal_code+'/')
            

    else:
        return HttpResponse("Digite los datos pedidos porfavor")

def Chekview2(request):
    if request.POST["nombre"] and request.POST["contraseña"]:
        
        user = request.POST["nombre"]
        password = request.POST["contraseña"]

        try: 
            imagen = request.FILES["image"]

        except:
            imagen = "images/defecto.jpg"

        obj = Usuario.objects.create(user_name=user,user_password=password ,user_image=imagen)
        obj.save()
        return redirect('sala1/'+str(obj.id))

    else:
        return HttpResponse("No se puede Procesar la solicitud")

def Checkview3(request):
    if request.POST['code'] and request.POST['id_user']: 
        username_id = request.POST['id_user']
        usuario = Usuario.objects.get(id=username_id)
        code = request.POST['code'] 

        try:
            sala = Canal.objects.get(canal_code=code)

        except ObjectDoesNotExist:
            sala = None

        if sala == None:
            return HttpResponse("El codigo ingresado no existe")

        else:
            Membership.objects.create(usuario=usuario, canal=sala) 
            return redirect('home/'+str(username_id)+'/'+code+'/')

    else:
        return HttpResponse("Porfavor llene el campo requerido")

def Checkview4(request):
    if request.POST:
        username_id = request.POST['username_id']
        code = request.POST['code']

        usuario_arc = Usuario.objects.get(id=username_id)
        canal_arc = Canal.objects.get(canal_code=code)
        
        try:
            pdf_arc = request.FILES["pdf"]

        except:
            pdf_arc = "pdfs/Proyecto.pdf"

        titulo_arc = request.POST['titulo']
        descripcion_arc = request.POST['descripcion']
        tipo_arc = request.POST['tipo']
        categoria_arc = request.POST['categoria']

        arc = Archivo.objects.create(archivo=pdf_arc, titulo=titulo_arc, descripcion=descripcion_arc, categoria=categoria_arc, tipo=tipo_arc, usuario=usuario_arc, canal=canal_arc)
        arc.save()

        return redirect('home/'+str(username_id)+'/'+code+'/archivos/')
    else:
        return HttpResponse("Por favor digite los datos solicitados")



def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    canalid = Canal.objects.get(canal_code=room_id)
    new_message = Mensaje.objects.create(ms_text=message, ms_user=username, ms_canal=canalid)
    print(f"Nuevo mensaje en sala: {canalid.canal_code}")
    print(f"Fecha: {new_message.tiempo}")
    new_message.save()
    return HttpResponse('Message sent successfully')

def send2(request):
    print("llegue")
    message = request.POST['message']
    user_id = request.POST['username']
    post_id = request.POST['post_id']
    user = Usuario.objects.get(id=user_id)
    archivo = Archivo.objects.get(id=post_id)
    
    new_comentario = Comentarios.objects.create(cm_texto=message, cm_archivo = archivo, cm_user=user.user_name)
    archivo.comments += 1
    archivo.save()
    new_comentario.save()
    print(f"Nuevo comentario en el archivo: {archivo.titulo}")
    print(f"Fecha: {new_comentario.tiempo}")
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Canal.objects.get(codigo=room)

    messages = Mensaje.objects.filter(canal=room_details)
    return JsonResponse({"messages":list(messages.values())})

class DescargarArchivoView(View):
    def post(self, request, *args, **kwargs):
        post = Archivo.objects.get(id=request.POST['id_post'])
        response = HttpResponse(post.archivo, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s"' % post.archivo
        return response