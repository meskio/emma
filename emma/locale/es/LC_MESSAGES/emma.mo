��    5      �  G   l      �     �     �     �  v   �  �   B  �   �  r   _     �  .   �       @        U     m     r     w  *   �     �     �     �  �   �  	   q     {     �     �  4   �     �     �  �   �     �	  �   �	  !   �
  *   �
  :   �
       '   +  "   S  8   v  9   �     �     �       P        i     �  (   �     �     �     �     �     �     �     �  d  �     ^     q     �  �   �  �   0  �   �     z     �  3        B  @   E     �     �     �     �  -   �     �     �     	  �        �     �     �     �  9        F     M  �   O  ,   3  �   `  %     5   1  E   g  $   �  &   �  )   �  8   #  9   \     �     �     �  d   �  "   1     T  +   r     �     �     �     �     �     �     �           &   "   (                 /      %   ,       #   2         5                    	      *   
       3         .            '                        4   -   !       +          1                             )       $                   0                  %s found     error connecting by POP3     error sending email   * [[remind|23/11/2011 08:17;hackmeeting@listas.sindominio.ent;subject;text]]
    Schelude a reminder at certan date
   * find From:/hackmeeting/,Tags:asamblea
    Use for search on emails stored by emma
  * display 0
    Display an email from a search list generated
   * moderate [session_name]
    Start moderating an assembly
  * word
    While moderating request word
  * stop
    Stop moderating
   * remind 23/11/2011 08:17;hackmeeting@listas.sindominio.ent;subject;text
    Schelude a reminder at certan date
 %s has the word Assembly log from %(day)s/%(month)s/%(year)s

 Cc Connect to %(server)s:%(port)s nick:%(nick)s channel:%(channel)s Connect to jid:%(jid)s  Date From Give word to: %s Index not in range(0-%(number)d): %(args)s No help Not found any email Not valid index: %s Once a 'find' command is call use the 'display'command to output the email
with the index number give as parameter of 'display'
Ex: display 0 Present:  Request word from: %s Start moderating Stop moderating Stop moderating the assembly started with 'moderate' Subject To Use for search on emails stored by emma.
Search terms are introduced separated by ','with the form 'Field:string',
string can be a regular expression between '/'.
Ex: find From:/meskio.*/,Tags:asamblea,Body:/squat/ While moderating request word You can program reminders to be send by %s at a given date.
 It takes three or four parameters separated by ';': date;email;subject;body
The subject is optional [core]     load %(type)s %(name)s [core] Not valid config value on log_level [core] can't unsubscribe identifier, it was not subscribed [core] connect to database [core] preparing interfaces and modules [core] restore %s scheduled events [irc %(identifier)s] command received: %(cmd)s: %(args)s [xmpp %(identifier)s] command received: %(cmd)s: %(args)s args not well formed db request error. display emma is a bot for virtual assembly
==================================
Commands:
 error conecting to server: %s error conecting to xmpp: %s fetching email %(pop_user)s@%(pop_host)s find help moderate remind reminder stop word Project-Id-Version: emma 0.1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2012-03-16 16:20+0100
PO-Revision-Date: 2012-03-05 01:36+0100
Last-Translator: Ruben Pollan <meskio@sindominio.net>
Language-Team: Spanish
Language: es
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
     %s encontrados     falló al conectar por POP3     falló al enviar email   * [[recuerda|23/11/2011 08:17;hackmeeting@listas.sindominio.ent;subject;texto]]
    Programa un recordatorio para una fecha dada
   * busca From:/hackmeeting/,Tags:asamblea
    Busca en el archivo de emails de emma
  * muestra 0
    Muestra un email de la lista generada por una busqueda
   * modera [nombre_sesion]
    Inicia la moderación de una asamblea
  * palabra
    Durante una asamblea moderada pide turno de palabra
  * para
    Para la moderación
   * recuerda 23/11/2011 08:17;hackmeeting@listas.sindominio.ent;subject;texto
    Programa un recordatorio para una fecha dada
 %s tiene la palabra Log de la asamblea del %(day)s/%(month)s/%(year)s

 Cc Conectando a %(server)s:%(port)s nick:%(nick)s canal:%(channel)s Conectando a jid:%(jid)s Fecha De Doy palabra a: %s Indice fuera de rango(0-%(number)d): %(args)s No hay ayuda Email no encontrado Indice invalido: %s Una vez que el comando 'busca' a sido invocado usa el comando 'muestra' para devolver el email
dandole a 'muestra' el indice del email como parametro
Ej: muestra 0 Asistentes:  Petición de palabra de: %s Empiezo a moderar Paro de moderar Para la moderación de una asamblea iniciada con 'modera' Asunto A Busca en el archivo de email de emma.
Los patrones de busqueda se introducen separados por ',' con la forma 'Cabecera:texto',
texto puede ser una expresion regular entre '/'.
Ej: busca From:/meskio.*/,Tags:asamblea,Body:/squat/ Estando en moderación pide turno de palabra Puedes programar recordatorios enviandos por %s a una fecha dada.
 Requiere de tres o cuatro parametros separados por ';': fecha;email;asunto;cuerpo
El asunto es opcional [core]     cargando %(type)s %(name)s [core] Parametro de configuración log_level invalido [core] no se puede desubscribir el identificador, no estaba subscrito [core] conectando a la base de datos [core] preparando interfaces y modulos [core] restaurando %s eventos programados [irc %(identifier)s] comando recivido: %(cmd)s: %(args)s [xmpp %(identifier)s] comando recivido: %(cmd)s: %(args)s argumentos inválidos petición a db erronea. muestra emma es un bot para el asamblearismo virtual
============================================
Comandos:
 falló al conectar al servidor: %s falló al conectar a xmpp: %s descargando email %(pop_user)s@%(pop_host)s busca ayuda modera recuerda recordatorio para palabra 