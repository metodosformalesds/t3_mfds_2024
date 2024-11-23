from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    def get_client_ip(self, request):
        # Asegúrate de manejar valores 'None' correctamente
        if not request or not hasattr(request, 'META'):
            return "127.0.0.1"  # Dirección IP predeterminada
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', "127.0.0.1")
        return ip

    def stash_email_verification(self, request, email):
        # Asegúrate de que todas las partes de la clave sean cadenas válidas
        return super().stash_email_verification(request, str(email or ''))
