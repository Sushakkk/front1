from django.shortcuts import render
import datetime

# Create your views here.
THREATS = [
    {'id': 1, 'name': 'Запуск вредоносного ПО', 'short_description': 'Мониторинг запуска вредоносного ПО', 'img_url':'http://127.0.0.1:9000/static/virus.jpg', 'description':'Наши специалисты детектируют запуск вредоносного программного обеспечения в режиме 24/7, что позволяет защитить рабочие станции пользователей','count':9,'price':10000},
    {'id': 2, 'name': 'Сетевая активность', 'short_description': 'Мониторинг сетевой активности', 'img_url':'http://127.0.0.1:9000/static/network.jpg', 'description':'Наши специалисты имеют большой опыт в детектировании атак, основываясь на анализе сетевого трафика','count':16,'price':18000},
    {'id': 3, 'name': 'Эксплуатация уязвимостей', 'short_description': 'Мониторинг эксплуатации уязвимостей на рабочик станциях', 'img_url':'http://127.0.0.1:9000/static/vulnerability.jpg', 'description':'Наши специалисты имеют большой опыт в детектировании эксплуатации известных уязвимостей и атак, таких как eternal blue и kerberoasting','count':9,'price':11900},
    {'id': 4, 'name': 'Фишинговые атаки', 'short_description': 'Мониторинг проведения фишинговых атак', 'img_url':'http://127.0.0.1:9000/static/phishing.jpg','description':'Наши системы обнаружения фишинга помогут эффективно обнаружить и предотвратить фишинговую атаку','count':12,'price':10000},
    {'id': 5, 'name': 'Атаки DoS/DDoS', 'short_description': 'Мониторинг и противодействие DoS/DDoS атакам', 'img_url':'http://127.0.0.1:9000/static/ddos.jpg','description':'Наша система AntiDDoS успешно выявляет и блокирует DDoS атаки, что позволяет оставаться доступными для клиентов','count':73,'price':11500},
    {'id': 6, 'name': 'Эксплуатация уязвимостей web-приложений', 'short_description': 'Мониторинг эксплуатации уязвимостей web-приложений', 'img_url':'http://127.0.0.1:9000/static/web.jpg','description':'Для проникновения внутрь компании хакеры зачастую используют уязвимости в web-приложений. Наши специалисты успешно детектируют и митигируют попытки эксплуатации таких уязвимостей', 'count':7,'price':13200},
]

REQUESTS = [{'request_id':1,'threats':[{'threat_name':'Запуск вредоносного ПО','company_name':'Kaspersky', 'short_description':'Мониторинг запуска вредоносного ПО','price':'10000', 'img_url':'http://127.0.0.1:9000/static/virus.jpg'},{'threat_name':'Эксплуатация уязвимостей web-приложений','company_name':'Kaspersky', 'short_description':'Мониторинг эксплуатации уязвимостей web-приложений','price':'14000', 'img_url':'http://127.0.0.1:9000/static/web.jpg'}]}]


def threats_list(request):

    for req in REQUESTS:
        threat_count = len(req['threats'])

    threats = []
    if 'threat_name' in request.GET:
        for threat in THREATS:
            if request.GET['threat_name'].lower() in threat["name"].lower():
                threats.append(threat)
        return render(request, 'index.html', {'threats': threats, 'input_value':request.GET['threat_name'],'current_count':threat_count,'request_id':REQUESTS[0]['request_id']})
    return render(request, 'index.html', {'threats': THREATS, 'current_count':threat_count,'request_id':REQUESTS[0]['request_id']})


def threat_description(request, id):
    for threat in THREATS:
        if threat["id"] == id:
            data = threat
    return render(request, 'description.html', {'threat': data})


def threat_request(request, id):
    current_request = REQUESTS[0]
    return render(request, 'request.html', {'current_threats':current_request})