from django.shortcuts import render
from django.http import HttpResponse
from twilio.rest import Client
# Create your views here.

def webhook(request):
    if request.method == 'POST':
        data = request.POST

	signal_info = data.get('signal_info')

	account_sid = 'ACd583b9d8d4b1f740c2f72c3455c412be'
	auth_token = 'TU_TOKEN_DE_AUTENTICACION'
	client = Client(account_sid, auth_token)

	mensaje = client.messages.create(
	    body=f"Se recibió una señal: {signal_info}",
	    from='Twilio number',
	    to='662459847'
	)

		return HttpResponse('OK')

    return HttpResponse('Método no permitido', status=405)
