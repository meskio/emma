��    9      �  O   �      �     �     �       v   +  �   �  �   9  r   �  .   2     a  @   d     �     �     �  *   �     �     �          .  �   B  	   �     �  �   �  4   �	     �	     �	     �	  �   �	  g   �
  �   7  !   �  *   �  :   %     `  '   {  "   �  8   �  9   �     9     N  "   `     �  P   �     �     �  (        ?     D     Y     ^     g     n     w     �     �  (   �     �  d  �     2     E     e  �   �  �     �   �     N  3   �       @        F     _     e  -   h     �     �  !   �     �  �   �     �     �  �   �  9   u  (   �     �     �  �   �  t   �  �   :  %   �  5     E   A  $   �  &   �  )   �  8   �  9   6     p     �  6   �     �  d   �  "   B     e  +   �     �     �     �     �     �     �     �            3        L                 -                  *                                  5   .             )                    2      9      /       7   8         0                    !             %      1   "   4   	   (   &          3         ,       
   $          '           6   #             +           %s found     error connecting by POP3     error sending email   * [[remind|23/11/2011 08:17;hackmeeting@listas.sindominio.ent;subject;text]]
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
 Assembly log from %(day)s/%(month)s/%(year)s

 Cc Connect to %(server)s:%(port)s nick:%(nick)s channel:%(channel)s Connect to jid:%(jid)s  Date From Index not in range(0-%(number)d): %(args)s No help Not found any email Not valid command for history:  Not valid index: %s Once a 'find' command is call use the 'display'command to output the email
with the index number give as parameter of 'display'
Ex: display 0 Present:  Request word from: %s Start the moderation of an assembly.
It will assign turns to talk as people request them with 'word'.
If a session_name is given the session will be saved on the wiki. Stop moderating the assembly started with 'moderate' Store irc log on the wiki page  Subject To Use for search on emails stored by emma.
Search terms are introduced separated by ','with the form 'Field:string',
string can be a regular expression between '/'.
Ex: find From:/meskio.*/,Tags:asamblea,Body:/squat/ While moderating request word.
It can also be requestested with a /me containing the word 'word' in it. You can program reminders to be send by %s at a given date.
 It takes three or four parameters separated by ';': date;email;subject;body
The subject is optional [core]     load %(type)s %(name)s [core] Not valid config value on log_level [core] can't unsubscribe identifier, it was not subscribed [core] connect to database [core] preparing interfaces and modules [core] restore %s scheduled events [irc %(identifier)s] command received: %(cmd)s: %(args)s [xmpp %(identifier)s] command received: %(cmd)s: %(args)s args not well formed db request error. db update error: %(id)s - %(date)s display emma is a bot for virtual assembly
==================================
Commands:
 error conecting to server: %s error conecting to xmpp: %s fetching email %(pop_user)s@%(pop_host)s find gives the word to %s help moderate remind reminder starts moderating stop stops moderating time conversion error: %(id)s - %(date)s word Project-Id-Version: emma 0.2
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2012-04-01 13:55+0200
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
 Log de la asamblea del %(day)s/%(month)s/%(year)s

 Cc Conectando a %(server)s:%(port)s nick:%(nick)s canal:%(channel)s Conectando a jid:%(jid)s Fecha De Indice fuera de rango(0-%(number)d): %(args)s No hay ayuda Email no encontrado Comando no valido para hisotria:  Indice invalido: %s Una vez que el comando 'busca' a sido invocado usa el comando 'muestra' para devolver el email
dandole a 'muestra' el indice del email como parametro
Ej: muestra 0 Asistentes:  Petición de palabra de: %s Inicia la moderación de una asamblea.
Asignará turnos de palabra a la gente que los pida con el comando 'palabra'.
Si se le ha dado un nombre_sesion la sesion sera guardada en el wiki. Para la moderación de una asamblea iniciada con 'modera' Almacena el log de irc en la pagina wiki Asunto A Busca en el archivo de email de emma.
Los patrones de busqueda se introducen separados por ',' con la forma 'Cabecera:texto',
texto puede ser una expresion regular entre '/'.
Ej: busca From:/meskio.*/,Tags:asamblea,Body:/squat/ Mientras esta en moderacion pide turno de palabra.
Tambien se puede pedir con un /me con la palabra 'palabra' en el. Puedes programar recordatorios enviandos por %s a una fecha dada.
 Requiere de tres o cuatro parametros separados por ';': fecha;email;asunto;cuerpo
El asunto es opcional [core]     cargando %(type)s %(name)s [core] Parametro de configuración log_level invalido [core] no se puede desubscribir el identificador, no estaba subscrito [core] conectando a la base de datos [core] preparando interfaces y modulos [core] restaurando %s eventos programados [irc %(identifier)s] comando recivido: %(cmd)s: %(args)s [xmpp %(identifier)s] comando recivido: %(cmd)s: %(args)s argumentos inválidos petición a db erronea. fallo en la actualización de la bd: %(id)s - %(date)s muestra emma es un bot para el asamblearismo virtual
============================================
Comandos:
 falló al conectar al servidor: %s falló al conectar a xmpp: %s descargando email %(pop_user)s@%(pop_host)s busca da turno de palabra a %s ayuda modera recuerda recordatorio empieza a moderar para para de moderar fallo en la conversion de tiempo: %(id)s - %(date)s palabra 