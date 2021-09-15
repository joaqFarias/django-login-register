from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import User


def root(request):
    return redirect('/index')

def index(request):

    return render(request, 'login_registro.html')


def login(request):

    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "email": log_user.email,
                    #"role": log_user.role
                }

                request.session['user'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/exito")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")

        return redirect("/index")
    else:
        return redirect("/index")


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['register_first_name'] =  request.POST['first_name']
            request.session['register_last_name'] =  request.POST['last_name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email=request.POST['email'],
                password=password_encryp,
                #role=request.POST['role']
            )

            messages.success(request, "El usuario fue agregado con exito.")
            
            request.session['user'] = {
                "id" : usuario_nuevo.id,
                "name": f"{usuario_nuevo.first_name} {usuario_nuevo.last_name}",
                "email": usuario_nuevo.email
            }
            return redirect("/index")

        return redirect("/index")
    else:
        return redirect("/index")

def salir(request):
    if 'user' in request.session.keys():
        del request.session['user']
    
    return redirect("/index")

@login_required
def exito(request):
    return render(request, 'exito.html')