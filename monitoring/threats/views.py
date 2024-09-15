from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
from .models import Threat, Request, RequestThreat


# Create your views here.
THREATS = [
    {'id': 1, 'name': 'Запуск вредоносного ПО', 'short_description': 'Мониторинг запуска вредоносного ПО', 'img_url':'http://127.0.0.1:9000/static/virus.jpg', 'description':'Наши специалисты детектируют запуск вредоносного программного обеспечения в режиме 24/7, что позволяет защитить рабочие станции пользователей','count':9,'price':10000},
    {'id': 2, 'name': 'Сетевая активность', 'short_description': 'Мониторинг сетевой активности', 'img_url':'http://127.0.0.1:9000/static/network.jpg', 'description':'Наши специалисты имеют большой опыт в детектировании атак, основываясь на анализе сетевого трафика','count':16,'price':18000},
    {'id': 3, 'name': 'Эксплуатация уязвимостей', 'short_description': 'Мониторинг эксплуатации уязвимостей на рабочик станциях', 'img_url':'http://127.0.0.1:9000/static/vulnerability.jpg', 'description':'Наши специалисты имеют большой опыт в детектировании эксплуатации известных уязвимостей и атак, таких как eternal blue и kerberoasting','count':9,'price':11900},
    {'id': 4, 'name': 'Фишинговые атаки', 'short_description': 'Мониторинг проведения фишинговых атак', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg','description':'Наши системы обнаружения фишинга помогут эффективно обнаружить и предотвратить фишинговую атаку','count':12,'price':10000},
    {'id': 5, 'name': 'Атаки DoS/DDoS', 'short_description': 'Мониторинг и противодействие DoS/DDoS атакам', 'img_url':'http://127.0.0.1:9000/static/ddos.jpg','description':'Наша система AntiDDoS успешно выявляет и блокирует DDoS атаки, что позволяет оставаться доступными для клиентов','count':73,'price':11500},
    {'id': 6, 'name': 'Эксплуатация уязвимостей web-приложений', 'short_description': 'Мониторинг эксплуатации уязвимостей web-приложений', 'img_url':'http://127.0.0.1:9000/static/web.jpg','description':'Для проникновения внутрь компании хакеры зачастую используют уязвимости в web-приложений. Наши специалисты успешно детектируют и митигируют попытки эксплуатации таких уязвимостей', 'count':7,'price':13200},
]
# TODO
REQUESTS = [{'request_id':1,'threats':[{'threat_name':'Запуск вредоносного ПО','company_name':'Kaspersky', 'short_description':'Мониторинг запуска вредоносного ПО','price':'10000', 'img_url':'http://127.0.0.1:9000/static/virus.jpg'},{'threat_name':'Эксплуатация уязвимостей web-приложений','company_name':'Kaspersky', 'short_description':'Мониторинг эксплуатации уязвимостей web-приложений','price':'14000', 'img_url':'http://127.0.0.1:9000/static/web.jpg'}]}]



def get_name_by_id(threats, search_id):
    for threat in threats:
        if threat['id'] == search_id:
            return threat['name']
    return None


def threats_list(request):
    

    # проверяем наличие заявки в статусе draft
    if not Request.objects.filter(status='draft').exists():
        req = Request()
        req.save()

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
        'request_id': current_request.id if current_request else req.id
    }
    
    return render(request, 'index.html', context)



def threat_description(request, id):

    threat = Threat.objects.get(id=id)
    return render(request, 'description.html', {'threat': threat})



def threat_request(request, id):
    req_id = id
    current_request = Request.objects.get(id=id)
    threat_ids = RequestThreat.objects.filter(request=current_request).values_list('threat_id', flat=True)
    current_threats = Threat.objects.filter(id__in=threat_ids)
    
    # Передаем данные в шаблон
    context = {
        'current_threats': current_threats,
        'current_request': current_request,
        'req_id':req_id
    }
    
    return render(request, 'request.html', context)


def add_threat(request):
    if request.method == 'POST':
        threat_id = request.POST.get('threat_id')
        threat = Threat.objects.get(id=threat_id)
        req = Request.objects.get(status='draft')
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