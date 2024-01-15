from django.shortcuts import render
from datetime import date


def GetData(id):
    data = [
            
  {'title': 'Установка и настройка сетевого оборудования', 
   'adress': 'Алексеевская', 'time':'от 7 до 14 рабочих дней',
    'price': 10000,
    'summary': 'Комплексное обслуживание сетевой инфраструктуры', 
    'due_date': '12 месяцев', 
    'image': "https://2bservice.ru/upload/medialibrary/23f/23f6679a3a068c1a305d10145830e6d6.png",
    'id': 1, 
    'info': 'Наши эксперты проведут профессиональную установку и настройку сетевого оборудования, включая маршрутизаторы, коммутаторы, точки доступа и системы безопасности. Мы гарантируем стабильное и безопасное подключение к интернету.',
    'includes': [
        'Монтаж активного и пассивного сетевого оборудования;', 
        'Настройки сетей и сетевого оборудования;',
        'Администрирования сетей и сетевого оборудования;',
        'Мониторинга работы сетей и сетевых устройств;',
        'Маршрутизации трафиков;',
        'Проведению аудита и диагностики проблем в сети;',
        'Настраиванию VPN-каналов;',\
          'И т.д.']
    },
  {
    'title': 'Мониторинг инфраструктуры',
    'adress': 'Алтуфьевское шоссе, 12',
    'time': 'до 7 рабочих дней (подключение мониторинга)',
    'price': 7000,
    'summary': 'Подключение мониторинга, и его проведение на постоянной основе',
    'due_date': "На всем протяжении оказания услуги",
    'image': "https://top-fon.com/uploads/posts/2023-02/1675504503_top-fon-com-p-fon-dlya-prezentatsii-monitoring-24.jpg",
    'id': 2,
    'info': 'Мы осуществляем постоянный мониторинг серверов, чтобы предотвратить сбои и неожиданные проблемы. ВПри возникновении неполадок, наша команда будет оперативно реагировать, сообщать о неполадках и восстанавливать работоспособность серверов.',
    'includes': [
      'Подключение различных систем мониторинга на любые сервера и сервисы клиентов, в т.ч. Grafana, Zabbix и др.;',
      'Мониторинг состояния систем 24/7 нашими операторами;',
      'Подключение алертов для уведомления клиента;',
      'Молниеносная реакция на отклонения метрик и восстановление работоспособности сервисов.'
    ]
  },
  {
    'title': 'Резервное копирование',
    'price': 5000,
    'time': 'До 3 рабочих дней (внедрение резервного копирования)',
    'summary': 'Внедрение резервного копирования различных видов',
    'image': 'https://filearchive.cnews.ru/img/book/2022/06/02/backup_as_a_service.jpg',
    'due_date': "На всем протяжении оказания услуги",
    'id': 3,
    'info': 'Мы предлагаем регулярное резервное копирование данных с использованием надежных и безопасных методов. В случае потери данных или сбоя системы, мы сможем восстановить ценную информацию и предотвратить значительные потери.',
    'includes': [
      'Любые виды РК: инкрементальные, разностные и т.д;',
      'Копирование данных как на наши сервера, так и на ваши хранилища;',
      'Многогранность видов, методов и объемов резервных копий;'
    ]
  },
  {
    'title': 'Защита от кибератак',
    'price': 10000,
    'time': 'до 7 рабочих дней (Внедрение системы обнаружения кибератак (СОК))',
    'summary': 'Внедрение системы обнаружения кибератак в вашу инфраструктуру, а также постоянный мониторинг',
    'due_date': "На всем протяжении оказания услуги",
    'id': 4,
    'image': 'https://www.secuteck.ru/hubfs/SecuteckRu/Articles/Cybersecurity-Issues-and-How-to-Defend-Your-Business-against-Cyberattacks-in-2020.jpg',
    'info': 'Наша команда специалистов по безопасности поможет защитить вас от кибератак и вредоносного программного обеспечения. Мы также предлагаем установку и настройку современных систем защиты, включая брандмауэры, антивирусные программы и системы обнаружения вторжений.',
    'includes': [
      'Внедрение СОКа во всю необходимую инфраструктуру;',
      'Внедрение защищающего от кибератак ПО;'
      'Подключение вашей инфраструктуры в наш единый центр мониторинга инцидентов инфромационной безопасности;',
      'Молниеносная реакция на любой инцидент;',
      'Возможность разворачивания центра мониторинга инцидентов ИБ в вашей инфраструктуре;',
      'Подключение алертов для уведомления о всех инцидентах;'
      'И многое другое...'
    ]
  },
        ]
    if id == -1:
        return data
    return data[id - 1]

def GetServices(request):
    keyword = request.GET.get('keyword')
    a = GetData(-1)
    if not keyword:
        return render(request, 'services.html', {'data': {
        'current_date': date.today(),
        'services': a}})
    services = []
    for i in a:
        if keyword and keyword.lower() in i.get('title', '').lower():
            services.append(i)
    return render(request, 'services.html', {'data': {
        'current_date': date.today(),
        'services': services}})

def GetService(request, id):
    return render(request, 'service.html', {'data' : {
        'current_date': date.today(),
        'service': GetData(id)
    }})