# Bot Inmobiliario 2.0

Bot que busca pisos de particulares en múltiples portales y envía notificaciones a Telegram.

## Despliegue en Render

1. Sube este repositorio a GitHub
2. Conecta tu cuenta de Render con GitHub
3. Crea un nuevo "Web Service" o "Worker"
4. Configura las variables de entorno:
   - `TELEGRAM_BOT_TOKEN`: Tu token de bot de Telegram
   - `TELEGRAM_CHAT_ID`: Tu ID de chat de Telegram

## Variables de Entorno

- `TELEGRAM_BOT_TOKEN`: Token del bot de Telegram
- `TELEGRAM_CHAT_ID`: ID del chat donde enviar notificaciones

## Configuración

Edita `config.py` para ajustar:
- Zonas de búsqueda
- Fuentes activas (pisos.com, fotocasa, idealista, etc.)
- Intervalos de búsqueda
- Filtros de particulares

## Dependencias

- requests: Para peticiones HTTP
- beautifulsoup4: Para parsear HTML
- lxml: Parser XML/HTML rápido
- playwright: Para scraping de sitios dinámicos (Idealista)
