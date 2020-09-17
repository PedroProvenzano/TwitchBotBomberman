from twitchio.ext import commands
import pyautogui
from time import sleep
from itertools import repeat
from dotenv import load_dotenv
load_dotenv()
import os
pag = pyautogui

delayTime = 0.25

equipoUno = []
equipoDos = []
admins = ['Mrklus', 'mrklus']

# funciones rapidas
def direcciones(arg, jugador):
    if jugador == 'jugadorUno':
        if arg == 'u':
            return 'i'
        elif arg == 'd':
            return 'k'
        elif arg == 'l':
            return 'j'
        elif arg == 'r':
            return 'l'
    elif jugador == 'jugadorDos':
        if arg == 'u':
            return 'w'
        elif arg == 'd':
            return 's'
        elif arg == 'l':
            return 'a'
        elif arg == 'r':
            return 'd'    

# check
def checkAdmin(nombre):
    if not nombre in admins:
        return False
    else:
        return True

# movimiento
def movimientoRes(nombreUsuario, direccion, tiempo=1):
        # Equipo uno
    for integrante in equipoUno:
        if nombreUsuario == integrante:
            # ejecuta la accion en el equipo uno
            dirFinal = direcciones(direccion, 'jugadorUno')
            pag.keyDown(dirFinal)
            sleep(0.20*int(tiempo))
            pag.keyUp(dirFinal)
            return
        # Equipo dos
    for integrante in equipoDos:
        if nombreUsuario == integrante:
            #ejecuta la accion en el equipo dos
            dirFinal = direcciones(direccion, 'jugadorDos')
            pag.keyDown(dirFinal)
            sleep(0.20*int(tiempo))
            pag.keyUp(dirFinal)
            return    


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=os.getenv("IRC_TOKEN"), client_id=os.getenv("CLIENT_ID"), nick=os.getenv("NICK"), prefix='!',
                         initial_channels=[os.getenv("INITIAL_CHANNELS")])

    
    async def event_ready(self):
        print(f'Bot listo!')

    async def event_message(self, message):
        await self.handle_commands(message)

    # Acciones especificas

    # Comando para registrarse en un equipo EJ: !register equipoUno
    @commands.command(name='register')
    async def my_commandRegister(self, ctx, *args):

        for integrante in equipoUno:
            if(ctx.author.name == integrante):
                await ctx.send(f'Jugador {ctx.author.name} ya se encuentra registrado en el equipo uno..')
                return
        for integrante in equipoDos:
            if(ctx.author.name == integrante):
                await ctx.send(f'Jugador {ctx.author.name} ya se encuentra registrado en el equipo dos..')
                return
        

        if args[0]=='equipoUno':
            if len(equipoUno) == 3:
                await ctx.send('Equipo uno ya esta lleno')
                return
            else:
                equipoUno.append(ctx.author.name)
                await ctx.send(f'Jugador {ctx.author.name} registrado en equipo uno')

        elif args[0]=='equipoDos':
            if len(equipoDos) == 3:
                await ctx.send('Equipo dos ya esta lleno')
                return
            else:
                equipoDos.append(ctx.author.name)
                await ctx.send(f'Jugador {ctx.author.name} registrado en equipo dos')


# Comando para mostrar en chat los participantes de los grupos
    @commands.command(name='teams')
    async def my_commandTeams(self, ctx, *args):
        await ctx.send(f'El equipo uno es {equipoUno}')
        await ctx.send(f'El equipo dos es {equipoDos}')

# Comando para retirarse de un grupo !retire
    @commands.command(name='retire')
    async def my_commandRetire(self, ctx, *args):
        for integrante in equipoUno:
            if ctx.author.name == integrante:
                equipoUno.remove(ctx.author.name)
                await ctx.send(f'El usuario {ctx.author.name} se retiro del equipo uno')
                return
        for integrante in equipoDos:
            if ctx.author.name == integrante:
                equipoDos.remove(ctx.author.name)
                await ctx.send(f'El usuario {ctx.author.name} se retiro del equipo dos')
                return
        
        await ctx.send(f'El usuario {ctx.author.name} no pertenece a ningun equipo')

    # Comando de movimientos
    @commands.command(name='move')
    async def my_commandJas(self, ctx, *args):
        # Chequea que el argumento de cantidad de movimiento este definido, caso contrario pone un default 
        try:
            tiempoMove = args[1]
        except IndexError:
            tiempoMove = 1


        if int(tiempoMove) > 3:
            return
        # Movimiento
        movimientoRes(ctx.author.name, args[0], tiempoMove)

        
    # Limpiar equipos 
    @commands.command(name='restart')
    async def my_commandRestart(self, ctx):
        # Check admin
        if checkAdmin(ctx.author.name):
            equipoUno.clear()
            equipoDos.clear()
            await ctx.send(f'Equipos reiniciados!')
            return
        else:
            await ctx.send(f'Lo siento {ctx.author.name}, no sos admin')
            return

    # Poner bombas 
    @commands.command(name='bomb')
    async def my_commandBomb(self, ctx):
        # Equipo uno
        for integrante in equipoUno:
            if ctx.author.name == integrante:
                # ejecuta la accion en el equipo uno
                pag.keyDown('m')
                sleep(0.05)
                pag.keyUp('m')
                return
        # Equipo dos
        for integrante in equipoDos:
            if ctx.author.name == integrante:
                #ejecuta la accion en el equipo dos
                pag.keyDown('f')
                sleep(0.05)
                pag.keyUp('f')
                return        

#    @commands.command(name='movegroup')
#    async def my_commandMoveGroup(self, ctx, *args):
#        if checkAdmin(ctx.author.name):


    @commands.command(name='ayuda')
    async def my_commandHelp(self, ctx):
        await ctx.send('Instrucciones: !move l,r,u,d || !bomb [para poner bomba]')
        


bot = Bot()
bot.run()