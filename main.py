# Made and developed by gneval9 Software
# 08-08-2026
# Versión: 0.0.0-dev

import time
import sys
import threading
import curses
from curses import wrapper


segundos_por_tick = 2 		# Default (2)
ticks_total = 0

debug = False

dinero = 500
impuestos = 5
poblacion = 1
recursos = 0
hambre = 0
alimentos = 150
fabricas = 1
casas = 1
multi_fabricas = 0.5
multi_casas = 2
capacidad = casas * multi_casas
humor = 100



#---PRECIOS---#

prec_fabrica = [200, 170]
prec_casa = [170, 100]

prec_alimento = [2]
prec_recurso = [8]

#------------#



def clamp(val, min_val, max_val):
	if min_val <= val <= max_val:
		return(val)

	elif val < min_val:
		return(min_val)
	
	elif val > max_val:
		return(max_val)





	
	
def main(stdscr):
	global segundos_por_tick, ticks_total
	
	comando = ""

	ventana_info = curses.newwin(30, 30, 0, 0)
	ventana_cmd = curses.newwin(3, curses.COLS, curses.LINES -4, 0)

	ventana_cmd.nodelay(True)
	ventana_cmd.keypad(True)
	curses.curs_set(0)



	stdscr.clear()
	stdscr.addstr(2, 50,"""
	                                                                                                                                    
	            ...                                                                       .                
		   xH88"`~                                                                      @88>              
		 :8888                            .u    .                            .u    .     %8P               
		:8888>                   .u     .d88B :@8c        .         u      .d88B :@8c     .          u     
		X8888                 ud8888.  ="8888f8888r  .udR88N     us888u.  ="8888f8888r  .@88u     us888u.  
		88888               :888'8888.   4888>'88"  <888'888k .@88 "8888"   4888>'88"  ''888E` .@88 "8888" 
		88888              d888 '88%"   4888> '    9888 'Y"  9888  9888    4888> '      888E  9888  9888  
		88888              8888.+"      4888>      9888      9888  9888    4888>        888E  9888  9888  
		`8888L           ! 8888L       .d888L .+   9888      9888  9888   .d888L .+     888E  9888  9888  
		 `8888          /  '8888c. .+  ^"8888*"    ?8888u../ 9888  9888   ^"8888*"      888&  9888  9888  
		   "888.      :"    "88888%       "Y"       "8888P'  "888*""888"     "Y"        R888" "888*""888" 
		     `""***~"`        "YP'                    "P'     ^Y"   ^Y'                  ""    ^Y"   ^Y'  
                                                                                                  




			                                         
                                  .                       .,-.  .-.    .- .                
                                  |-.. .  .-..-..-,. ..-. |`-;  `-..-.-|--|-. . ..-. .-..-,
                                  `-''-|  `-|' '`'- ` `-`-'-'   `-'`-' '  '- ` ` `-`-'  `'-
                                     `-'  `-'                                              
                                                           08-2026



					""")

	stdscr.refresh()
	time.sleep(2)
	
	stdscr.clear()
	stdscr.refresh()

	


	def mostrar_informacion():
		ventana_info.erase()

		ventana_info.addstr(1,1,f"Dinero: {int(dinero)}€")
		ventana_info.addstr(2,1,f"Impuestos: {impuestos}%")
	
		ventana_info.addstr(4,1,f"Población: {int(poblacion)} / {capacidad}")
		ventana_info.addstr(5,1,f"Casas: {casas}")
		ventana_info.addstr(6,1,f"Fábricas: {fabricas}")

		ventana_info.addstr(8,1,f"Recursos: {int(recursos)}R")
		ventana_info.addstr(9,1,f"Alimentos: {int(alimentos)}")
	
		ventana_info.addstr(11,1,f"Hambre: {hambre}%")
		ventana_info.addstr(12,1,f"Humor: {int(humor)}%")
	

		if debug == True:
			ventana_info.addstr(18,1,f"Segundos por tick: {segundos_por_tick}")
			ventana_info.addstr(19,1,f"Ticks totales: {ticks_total}")	
	
		ventana_info.refresh()





	#--- COMANDOS ---#

	def mostrar_comando(output, vanish=True, delay=1.5):
		ventana_cmd.erase()

		ventana_cmd.addstr(0,1, "COMANDO >>  " )
		ventana_cmd.addstr(1,len("COMANDO >>  "), output)
		
		ventana_cmd.refresh()
		
		if vanish == True:
			time.sleep(delay)
			ventana_cmd.erase()
			ventana_cmd.refresh()

		else:
			ventana_cmd.refresh()
			




	def entrada_comandos():
		nonlocal comando

		tecla = ventana_cmd.getch()

		if tecla != -1:
			if 32 <= tecla <= 126:
				comando += chr(tecla)

			elif tecla in (8, 127, curses.KEY_BACKSPACE):
				ventana_cmd.erase()
				comando = comando[:-1]

			elif tecla in (10, 13):
				ventana_cmd.erase()
				ejecutar_comando(comando.split())
				comando = ""


		
		ventana_cmd.addstr(0,1, "COMANDO >>  " + comando + "_")
		ventana_cmd.refresh()





	def ejecutar_comando(comando):
		global debug, dinero, poblacion, recursos, hambre, alimentos, fabricas, multi_fabricas, humor, capacidad, casas, impuestos, segundos_por_tick

		if comando:
			nombre = comando[0]
			argumentos = comando[1:]

		else:
			nombre = 0



		if nombre == "help":
			output = """help, debug, buy [fabrica/casa/alimentos/recursos] [num], sell [fabrica/casa/alimentos/recursos] [num], 
						            tax [%], ticks [s/t]"""
			mostrar_comando(output, False)



		elif nombre == "ticks":
			segundos_por_tick = float(argumentos[0])


		elif nombre == "debug":
			if debug == False:
				output = "Modo debug activado"

			elif debug == True:
				output = "Modo debug desactivado"
	
			debug = not debug
			mostrar_comando(output)





		elif nombre == "tax":
			if 0 <= int(argumentos[0]) <= 100:
				impuestos = int(argumentos[0])
			
			else:
				mostrar_comando("Valor inválido")





		elif nombre == "buy":
			if len(argumentos) < 2:
				return


			if argumentos[0] == "fabrica":
				cantidad = int(argumentos[1])
				prec_total_dinero = prec_fabrica[0] * cantidad
				prec_total_recursos = prec_fabrica[1] * cantidad

				output = f"¿Comprar {cantidad} fábricas por {prec_total_dinero}€ y {prec_total_recursos}R? (y o n)"
				mostrar_comando(output, False)

				while True:
					tecla = ventana_cmd.getch()

					if tecla == ord("y"):
						if prec_total_dinero < dinero and prec_total_recursos < recursos:
							dinero -= prec_total_dinero
							recursos -= prec_total_recursos
							fabricas += cantidad

							ventana_cmd.erase()
							break

						else:
							mostrar_comando("No puedes comprar esto")
							break

					elif tecla == ord("n"):
						ventana_cmd.erase()
						break





			if argumentos[0] == "casa":
				cantidad = int(argumentos[1])
				prec_total_dinero = prec_casa[0] * cantidad
				prec_total_recursos = prec_casa[1] * cantidad

				output = f"¿Comprar {cantidad} casas por {prec_total_dinero}€ y {prec_total_recursos}R? (y o n)"
				mostrar_comando(output, False)

				while True:
					tecla = ventana_cmd.getch()

					if tecla == ord("y"):
						if prec_total_dinero < dinero and prec_total_recursos < recursos:
							dinero -= prec_total_dinero
							recursos -= prec_total_recursos
							casas += cantidad

							ventana_cmd.erase()
							break

						else:
							mostrar_comando("No puedes comprar esto")
							break

					elif tecla == ord("n"):
						ventana_cmd.erase()
						break






			if argumentos[0] == "alimentos":
				cantidad = int(argumentos[1])
				prec_total_dinero = prec_alimento[0] * cantidad

				output = f"¿Comprar {cantidad} alimentos por {prec_total_dinero}€? (y o n)"
				mostrar_comando(output, False)

				while True:
					tecla = ventana_cmd.getch()

					if tecla == ord("y"):
						if prec_total_dinero < dinero:
							dinero -= prec_total_dinero
							alimentos += cantidad

							ventana_cmd.erase()
							break

						else:
							mostrar_comando("No puedes comprar esto")
							break

					elif tecla == ord("n"):
						ventana_cmd.erase()
						break


			if argumentos[0] == "recursos":
				cantidad = int(argumentos[1])
				prec_total_dinero = prec_recurso[0] * cantidad


				output = f"¿Comprar {cantidad} recursos por {prec_total_dinero}€? (y o n)"
				mostrar_comando(output, False)

				while True:
					tecla = ventana_cmd.getch()

					if tecla == ord("y"):
						if prec_total_dinero < dinero:
							dinero -= prec_total_dinero
							recursos += cantidad

							ventana_cmd.erase()
							break

						else:
							mostrar_comando("No puedes comprar esto")
							break

					elif tecla == ord("n"):
						ventana_cmd.erase()
						break


		elif nombre =="sell":
			if len(argumentos) < 2:
				return

		
			if argumentos[0] == "fabrica":
				cantidad = int(argumentos[1])
				prec_total_dinero = prec_fabrica[0] * cantidad / 2
				prec_total_recursos = prec_fabrica[1] * cantidad / 2

				output = f"¿Vender {cantidad} fábricas por {prec_total_dinero}€ y {prec_total_recursos}R? (y o n)"
				mostrar_comando(output, False)

				while True:
					tecla = ventana_cmd.getch()

					if tecla == ord("y"):
						if fabricas >= cantidad:
							dinero += prec_total_dinero
							recursos += prec_total_recursos
							fabricas -= cantidad

							ventana_cmd.erase()
							break

						else:
							mostrar_comando("No dispones de suficientes fábricas para vender")
							break

					elif tecla == ord("n"):
						ventana_cmd.erase()
						break





			if argumentos[0] == "casa":
				cantidad = int(argumentos[1])
				prec_total_dinero = prec_casa[0] * cantidad / 2
				prec_total_recursos = prec_casa[1] * cantidad / 2

				output = f"¿Vender {cantidad} casas por {prec_total_dinero}€ y {prec_total_recursos}R? (y o n)"
				mostrar_comando(output, False)

				while True:
					tecla = ventana_cmd.getch()

					if tecla == ord("y"):
						if casas >= cantidad and (casas - cantidad) * 2 >= poblacion:
							dinero += prec_total_dinero
							recursos += prec_total_recursos
							casas -= cantidad

							ventana_cmd.erase()
							break

						else:
							mostrar_comando("No dispones de suficientes casas para vender")
							break

					elif tecla == ord("n"):
						ventana_cmd.erase()
						break






			if argumentos[0] == "alimentos":
				cantidad = int(argumentos[1])
				prec_total_dinero = prec_alimento[0] * cantidad / 2
				prec_total_recursos = prec_alimento[1] * cantidad / 2

				output = f"¿Vender {cantidad} alimentos por {prec_total_dinero}€ y {prec_total_recursos}R? (y o n)"
				mostrar_comando(output, False)

				while True:
					tecla = ventana_cmd.getch()

					if tecla == ord("y"):
						if alimentos >= cantidad:
							dinero += prec_total_dinero
							recursos += prec_total_recursos
							alimentos -= cantidad

							ventana_cmd.erase()
							break

						else:
							mostrar_comando("No dispones de suficientes alimentos para vender")
							break

					elif tecla == ord("n"):
						ventana_cmd.erase()
						break



			if argumentos[0] == "recursos":
				cantidad = int(argumentos[1])
				prec_total_dinero = prec_recurso[0] * cantidad / 2

				output = f"¿Vender {cantidad} recursos por {prec_total_dinero}€? (y o n)"
				mostrar_comando(output, False)

				while True:
					tecla = ventana_cmd.getch()

					if tecla == ord("y"):
						if recursos >= cantidad:
							dinero += prec_total_dinero
							recursos -= cantidad

							ventana_cmd.erase()
							break

						else:
							mostrar_comando("No dispones de suficientes recursos para vender")
							break

					elif tecla == ord("n"):
						ventana_cmd.erase()
						break


		elif nombre == "exit":
			ventana_cmd.clear()
			ventana_cmd.refresh()
			sys.exit()




		elif not comando:
			return

		else:
			mostrar_comando("Comando inválido")

	#----------------#




	#---LOGICA---#

	def logica():
		global dinero, poblacion, recursos, hambre, alimentos, fabricas, multi_fabricas, humor, capacidad, casas, impuestos


		# alimentos

		alimentos -= poblacion / 2

		if alimentos <= 0:
			alimentos = 0



		# hambre
	
		if alimentos <= poblacion + (poblacion // 5):
			hambre += 2
			hambre = clamp(hambre, 0, 100)

		else:
			hambre -= 15
			hambre = clamp(hambre, 0, 100)


		poblacion -= hambre // 25
		poblacion = clamp(poblacion, 0, capacidad)



		# fabricas

		produccion = (fabricas * multi_fabricas) * poblacion
		produccion *= (100 - hambre) / 100
		produccion *= humor / 100

		recursos += produccion
		dinero += produccion / 4



		# casas y capacidad

		capacidad = casas * 2



		# nacimientos

		if ticks_total != 0 and ticks_total % 10 == 0:
			if alimentos / 100 < capacidad:
				poblacion += alimentos / 100
				poblacion = round(poblacion)
				poblacion = clamp(poblacion, 0, capacidad)



		# impuestos

		if ticks_total != 0 and ticks_total % 5 == 0:
			dinero += produccion * impuestos / 100



		# humor

		humor = 100
		humor -= hambre
		humor -= impuestos * 2
		humor += min(alimentos / 10, 20)
		humor += min(dinero / 100, 20)
		humor += min(recursos / 25, 20)

		humor = clamp(humor, 0, 100)




		# Pantalla GAME OVER

		if poblacion == 0:
			poblacion = 0
			ventana_info.refresh()
			mostrar_comando("HAS PERDIDO      Pulsa ENTER para continuar...", False)
			
			while True:
				tecla = ventana_cmd.getch()

				if tecla in (10, 13, curses.KEY_ENTER):
					ventana_cmd.clear()
					ventana_cmd.refresh()
					sys.exit()







	#--- MAIN LOOP ---#

	last_tick = time.monotonic()

	while True:

		# logica cada 2s
		now = time.monotonic()
		if now - last_tick >= segundos_por_tick:
			logica()
			ticks_total += 1
			last_tick = now


		time.sleep(0.01)


		mostrar_informacion()
		entrada_comandos()

	#-----------------#


wrapper(main)




