from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
from .models import Threat, Request, RequestThreat
from django.contrib.auth.models import User


def threats_list(request):
    # проверяем наличие заявки в статусе draft
    if not Request.objects.filter(status='draft').exists():
        threat_count = 0
        current_request = 0
    else:
        requests = Request.objects.filter(status='draft')
        current_request = requests.first()
        threat_count = current_request.request_threats.count()

    
    threat_name = request.GET.get('threat_name', '').strip().lower()
    if threat_name:
        threats = Threat.objects.filter(threat_name__icontains=threat_name)
    else:
        threats = Threat.objects.all()

    
    
    # Передаем данные в шаблон
    context = {
        'threats': threats,
        'input_value': threat_name,
        'current_count': threat_count,
        'request_id': current_request.id if current_request else 0
    }
    
    return render(request, 'index.html', context)



def threat_description(request, id):
    threat = Threat.objects.get(id=id)
    return render(request, 'description.html', {'threat': threat})



def threat_request(request, id):
    if id == 0:
        return render(request, 'request.html', {'current_request':None})
    
    if Request.objects.filter(id=id).exclude(status='draft').exists():
        return render(request, 'request.html', {'current_request':None})
    
    if not Request.objects.filter(id=id).exists():
        return render(request, 'request.html', {'current_request':None})
    
    req_id = id
    current_request = Request.objects.get(id=id)
    threat_ids = RequestThreat.objects.filter(request=current_request).values_list('threat_id', flat=True)
     # Получаем все угрозы и их комментарии
    request_threats = RequestThreat.objects.filter(request=current_request)
    current_threats = Threat.objects.filter(id__in=request_threats.values_list('threat_id', flat=True))

    # Добавляем комментарии к объектам Threat
    for threat in current_threats:
        threat.comment = request_threats.get(threat=threat).comment  # Получаем комментарий для угрозы

    
    # Передаем данные в шаблон
    context = {
        'current_threats': current_threats,
        'current_request': current_request,
        'req_id':req_id
    }
    
    return render(request, 'request.html', context)


def add_threat(request):
    if request.method == 'POST':



        if not Request.objects.filter(status='draft').exists():
            req = Request()
            req.user_id = 1
            req.save()
        else:
            req = Request.objects.get(status='draft')

        threat_id = request.POST.get('threat_id')
        threat = Threat.objects.get(id=threat_id)
        if RequestThreat.objects.filter(request=req, threat=threat).exists():
            return redirect('/')
        request_threat = RequestThreat(request=req, threat=threat)
        request_threat.save()
        return redirect('/')
    else:
        return redirect('/')
    

def del_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        with connection.cursor() as cursor:
            cursor.execute("UPDATE requests SET status = %s WHERE id = %s", ['deleted', request_id])
        return redirect('/')
    else:
        return redirect('/')