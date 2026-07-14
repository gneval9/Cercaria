# Made and developed by gneval9 Software
# 08-08-2026 / 14-08-2026
version =  "1.1.2"

import time
import sys
import threading
import curses
from curses import wrapper
import ast


segundos_por_tick = 2 		# Default (2)
ticks_total = 0

debug = False
mode = "comm"		# comm, map

curs_x = 28
curs_y = 28 // 2

num_mapa = 0
map_pos = 0


fabricas = [[668]]
casas = [[553]]

num_fabricas = len(fabricas)
num_casas = len(casas)


dinero = 5000
impuestos = 5
poblacion = 1
recursos = 10000
hambre = 0
alimentos = 150
multi_fabricas = 0.5
multi_casas = 2
capacidad = num_casas * multi_casas
humor = 100

produccion = 0





#---PRECIOS---#
precios = {

"prec_fabrica": [300 * num_fabricas // 2, 170 * num_fabricas // 2],
"prec_casa": [170 * num_casas // 2, 100 * num_casas // 2],

"prec_alimentos": [2, 0],
"prec_recursos": [8, 0]

}
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
	

	with open("mapas_cercaria") as f:
		mapa = ast.literal_eval(f.read())

	ventana_info = curses.newwin(30, 30, 0, 0)
	ventana_cmd = curses.newwin(1, curses.COLS, curses.LINES -4, 0)
	ventana_cmdout = curses.newwin(2, curses.COLS, curses.LINES -3, len("COMANDO >>  "))
	ventana_mapa = curses.newwin(28, 57, 0, 60)

	ventana_cmd.nodelay(True)
	ventana_cmd.keypad(True)
	curses.curs_set(0)


	curses.start_color()



	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


	stdscr.clear()
	stdscr.addstr(2, 50,f"""
	                                                                                                                                    
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
                                                      | V{version} | 14-08-2026 |



					""")

	stdscr.refresh()
	time.sleep(2)
	
	stdscr.clear()
	stdscr.refresh()


	def mostrar_informacion():
	
		ventana_info.erase()

		ventana_info.addstr(1,1,f"Dinero: {int(dinero):,}€")
		ventana_info.addstr(2,1,f"Impuestos: {impuestos}%")
	
		ventana_info.addstr(4,1,f"Población: {int(poblacion):,} / {capacidad:,}")
		ventana_info.addstr(5,1,f"Casas: {num_casas:,}")

		ventana_info.addstr(7,1,f"Fábricas: {num_fabricas:,}")
		ventana_info.addstr(8,1,f"Producción: {round(produccion,3):,}R y {round(produccion / 3, 3):,}€")

		ventana_info.addstr(10,1,f"Recursos: {int(recursos):,}R")
		ventana_info.addstr(11,1,f"Alimentos: {int(alimentos):,}")
	
		ventana_info.addstr(13,1,f"Hambre: {hambre}%")
		ventana_info.addstr(14,1,f"Humor: {int(humor)}%")
	




		if debug == True:
			ventana_info.addstr(18,1,f"Segundos por tick: {segundos_por_tick}")
			ventana_info.addstr(19,1,f"Ticks totales: {ticks_total}")	
			ventana_info.addstr(20,1,f"Mode: {mode}")
			ventana_info.addstr(21,1,f"Map_pos: {map_pos}")
	
		ventana_info.refresh()




	#--- MAPA ---#

	
	def controlar_mapa(tecla):
		global curs_x, curs_y, mode, map_pos

		map_pos = ((curs_y * 28) + (curs_x // 2)) - 28


		if tecla == curses.KEY_UP and curs_y > 1:
			curs_y -= 1
			curses.flushinp()

		elif tecla == curses.KEY_DOWN and curs_y < 27:
			curs_y += 1
			curses.flushinp()

		elif tecla == curses.KEY_LEFT and curs_x > 1:
			curs_x -= 2
			curses.flushinp()

		elif tecla == curses.KEY_RIGHT and curs_x < 53:
			curs_x += 2
			curses.flushinp()


		if mode == "map":
			ventana_mapa.addstr(curs_y, curs_x, "X", curses.color_pair(1))


		ventana_mapa.refresh()
		




	def mostrar_mapa(num_mapa):
		global map_pos
		ventana_mapa.erase()

		x = 0
		y = 1


		for n in range(len(mapa[num_mapa])):
			if n !=0 and n % 28 ==0:
				y += 1
				x = 0


			if mapa[num_mapa][n] == 0:
				ventana_mapa.addstr(y, x, "-·", curses.color_pair(3))

			elif mapa[num_mapa][n] == 1:
				ventana_mapa.addstr(y, x, "#·", curses.color_pair(2))			

			elif mapa[num_mapa][n] == 2:
				ventana_mapa.addstr(y, x, "+·", curses.color_pair(4) | curses.A_DIM)

			x += 2


		for i in range(len(fabricas)):
			y = fabricas[i][0] // 28 + 1
			x = (fabricas[i][0] % 28) * 2 
			
			ventana_mapa.addstr(y, x, "M·", curses.color_pair(5))

		for i in range(len(casas)):
			y = casas[i][0] // 28 + 1
			x = (casas[i][0] % 28) * 2 
			
			ventana_mapa.addstr(y, x, "A·", curses.color_pair(6))

		for n in range(1, 28):
			ventana_mapa.addstr(n, 55, " ")

		ventana_mapa.refresh()
			







	#--- COMANDOS ---#


	def comprar_item(argumentos):
		global dinero, recursos, alimentos

		if argumentos[0] in ("fabrica", "casa"):
			return

		item = argumentos[0]
	
		item_prec = "prec_" + item


		cantidad = int(argumentos[1])
		prec_total_dinero = precios[item_prec][0] * cantidad
		prec_total_recursos = precios[item_prec][1] * cantidad


		output = f"¿Comprar {cantidad:,} {item} por {prec_total_dinero:,}€ y {prec_total_recursos:,}R? (y o n)"
		mostrar_comando(output, False)

		while True:
			tecla = ventana_cmd.getch()

			if tecla == ord("y"):
				if prec_total_dinero < dinero and prec_total_recursos < recursos:
					dinero -= prec_total_dinero
					recursos -= prec_total_recursos

					globals()[item] += cantidad

					ventana_cmd.erase()
					ventana_cmdout.erase()
					ventana_cmdout.refresh()
					break

				else:
					mostrar_comando("No puedes comprar esto")
					break

			elif tecla == ord("n"):
				ventana_cmd.erase()
				ventana_cmdout.erase()
				ventana_cmdout.refresh()
				break

		time.sleep(0.01)













	def vender_item(argumentos):
		global dinero, recursos, alimentos

		item = argumentos[0]
		
		item_prec = "prec_" + item


		cantidad = int(argumentos[1])
		prec_total_dinero = (precios[item_prec][0] * cantidad) / 2
		try:
			prec_total_recursos = (precios[item_prec][1] * cantidad) / 2

		except:
			prec_total_recursos = 0


		output = f"¿Vender {cantidad:,} {item} por {prec_total_dinero:,}€ y {prec_total_recursos:,}R? (y o n)"
		mostrar_comando(output, False)

		while True:
			tecla = ventana_cmd.getch()

			if tecla == ord("y"):
				if globals()[item] > cantidad:
					dinero += prec_total_dinero
					recursos += prec_total_recursos

					globals()[item] -= cantidad

					ventana_cmd.erase()
					ventana_cmdout.erase()
					ventana_cmdout.refresh()
					break

				else:
					mostrar_comando("No dispones de suficientes objetos para vender")
					break

			elif tecla == ord("n"):
				ventana_cmd.erase()
				ventana_cmdout.erase()
				ventana_cmdout.refresh()
				break





	def construir(argumentos):
		global mode, curs_x, curs_y, fabricas, dinero, recursos, num_fabricas, num_casas, capacidad

		item = argumentos[0]
		item_prec = "prec_" + item

		prec_total_dinero = precios[item_prec][0]
		try:
			prec_total_recursos = precios[item_prec][1]

		except:
			prec_total_recursos = 0



		mode = "map"
		while True:
			mostrar_comando(f"Construir {item} por {prec_total_dinero:,}€ y {prec_total_recursos:,}R", False)
			mostrar_comando("Pulsa [ESC] para dejar de construir", False, 0, (1,0))
			tecla = ventana_cmd.getch()

			if tecla in (10, 13):  # ENTER
				if prec_total_dinero < dinero and prec_total_recursos < recursos:
						
					if mapa[num_mapa][map_pos] == 0 or mapa[num_mapa][map_pos] == 2:
						ventana_cmdout.erase()
						mostrar_comando("No puedes construir aquí")

					elif any(casa[0] == map_pos for casa in casas) or any(fabrica[0] == map_pos for fabrica in fabricas):
						ventana_cmdout.erase()
						mostrar_comando("No puedes construir aquí")

					else:
						dinero -= prec_total_dinero
						recursos -= prec_total_recursos

						capacidad = num_casas * multi_casas

						globals()[item + "s"].append([map_pos])
						globals()["num_" + item + "s"] = len(globals()[item + "s"])



				else:
					curses.flushinp()
					ventana_cmdout.erase()
					mostrar_comando("No puedes comprar esto")
					time.sleep(1)
					curses.flushinp()
			
		


			elif tecla == 27:  # ESC
				curs_x = 28
				curs_y = 28 // 2		
				
				mode = "comm"
				ventana_cmdout.erase()
				ventana_cmdout.refresh()
				break


			else:
				mostrar_mapa(num_mapa)
				controlar_mapa(tecla)
				mostrar_informacion()
				time.sleep(0.05)
				


	def destruir(argumentos):
		global mode, curs_x, curs_y, fabricas, dinero, recursos, num_fabricas, num_casas, capacidad

		item = argumentos[0]
		item_prec = "prec_" + item

		prec_total_dinero = precios[item_prec][0] // 2
		try:
			prec_total_recursos = precios[item_prec][1] // 2

		except:
			prec_total_recursos = 0

		mode = "map"
		while True:
			mostrar_comando(f"Destruir {item} por {prec_total_dinero:,}€ y {prec_total_recursos:,}R", False)
			mostrar_comando("Pulsa [ESC] para dejar de destruir", False, 0, (1,0))
			tecla = ventana_cmd.getch()

			if tecla in (10, 13):  # ENTER
				if item == "casa":
					casa = next((c for c in casas if c[0] == map_pos), None)

					if casa == None:
						pass

					elif poblacion > (num_casas -1)  *  multi_casas: 
								ventana_cmdout.erase()
								mostrar_comando("No puedes dejar a tus ciudadanos sin techo.")

					else:
						casas.remove(casa)


					num_casas = len(casas)
					capacidad = num_casas * multi_casas

				else:
					curses.flushinp()
					ventana_cmdout.erase()
					time.sleep(1)
					curses.flushinp()



				if item == "fabrica":
					fabrica = next((f for f in fabricas if f[0] == map_pos), None)

					if fabrica == None:
						pass

					elif num_fabricas <= 1:
						ventana_cmdout.erase()
						mostrar_comando("No puedes quedarte sin fábricas")

					else:
						fabricas.remove(fabrica)


					num_fabricas = len(fabricas)



				else:
					curses.flushinp()
					ventana_cmdout.erase()
					time.sleep(1)
					curses.flushinp()
			
		


			elif tecla == 27:  # ESC
				curs_x = 28
				curs_y = 28 // 2		
				
				mode = "comm"
				ventana_cmdout.erase()
				ventana_cmdout.refresh()
				break


			else:
				mostrar_mapa(num_mapa)
				controlar_mapa(tecla)
				mostrar_informacion()
				time.sleep(0.05)




	def mostrar_comando(output, vanish=True, delay=1.5, pos=(0,0)):
		ventana_cmd.erase()
		ventana_cmd.addstr(0,1, "COMANDO >>  ")
		ventana_cmdout.addstr(pos[0],pos[1], output)
		
		ventana_cmdout.refresh()
		
		if vanish == True:
			time.sleep(delay)
			ventana_cmdout.erase()
			ventana_cmdout.refresh()

		else:
			ventana_cmdout.refresh()
			






	def entrada_comandos():
		nonlocal comando
		global mode

		tecla = ventana_cmd.getch()
		
		if mode == "comm":
			if tecla != -1:
				if 32 <= tecla <= 126:
					comando += chr(tecla)

				elif tecla in (8, 127, curses.KEY_BACKSPACE):
					ventana_cmd.erase()
					comando = comando[:-1]

				elif tecla in (10, 13):
					ventana_cmd.erase()
					ventana_cmdout.erase()
					ejecutar_comando(comando.split())
					comando = ""

		elif mode == "map":
			controlar_mapa(tecla)



		
		ventana_cmd.addstr(0,1, "COMANDO >>  " + comando + "_")
		ventana_cmd.refresh()






	def ejecutar_comando(comando):
		global debug, dinero, poblacion, recursos, hambre, alimentos, num_fabricas, multi_fabricas, humor, capacidad, num_casas, impuestos, segundos_por_tick, mode

		if comando:
			nombre = comando[0]
			argumentos = comando[1:]

		else:
			nombre = 0



		if nombre == "help":
			output = f"""help, build [fabrica, casa], destroy [fabrica, casa], buy [alimentos/recursos] [num], tax [%], ticks [s/t], debug,  \nsell [alimentos/recursos] [num], exit"""
			mostrar_comando(output, False)



		elif nombre == "ticks":
			if len(argumentos) < 1:
				return

			segundos_por_tick = float(argumentos[0])


		elif nombre == "debug":
			if debug == False:
				output = "Modo debug activado"

			elif debug == True:
				output = "Modo debug desactivado"
	
			debug = not debug
			mostrar_comando(output)




		elif nombre == "tax":

			if len(argumentos) < 1:
				return

			if 0 <= int(argumentos[0]) <= 100:
				impuestos = int(argumentos[0])
			
			else:
				mostrar_comando("Valor inválido")





		elif nombre == "map":
			mode = "map"




		elif nombre == "buy":
			if len(argumentos) < 2:
				return

			comprar_item(argumentos)
			



		elif nombre == "sell":
			if len(argumentos) < 2:
				return

			vender_item(argumentos)




		elif nombre == "build":
			if len(argumentos) < 1:
				return

			construir(argumentos)

		elif nombre == "destroy":
			if len(argumentos) < 1:
				return

			destruir(argumentos)

		elif nombre == "exit":
			ventana_cmd.clear()
			ventana_cmdout.erase()

			ventana_cmd.refresh()
			ventana_cmdout.refresh()

			sys.exit()




		elif not comando:
			return

		else:
			mostrar_comando("Comando inválido")


	#----------------#




	#---LOGICA---#

	def logica():
		global dinero, poblacion, recursos, hambre, alimentos, num_fabricas, multi_fabricas, humor, capacidad, casas, impuestos, produccion


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

		produccion = (num_fabricas * multi_fabricas) * poblacion
		produccion *= (100 - hambre) / 100
		produccion *= humor / 100

		recursos += produccion
		dinero += produccion / 3

		num_fabricas = len(fabricas)



		# casas y capacidad

		capacidad = num_casas * multi_casas



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
					ventana_cmdout.erase()

					ventana_cmd.refresh()
					ventana_cmdout.refresh()
					sys.exit()

				time.sleep(0.01)





	#--- MAIN LOOP ---#

	last_tick = time.monotonic()
	logica()
	mostrar_comando("Escribe 'help' para ver todos los comandos", False)

	while True:

		# logica cada 2s
		now = time.monotonic()
		if now - last_tick >= segundos_por_tick:
			logica()
			ticks_total += 1
			last_tick = now


		time.sleep(0.01)


		mostrar_informacion()
		mostrar_mapa(num_mapa)
		entrada_comandos()

	#-----------------#


wrapper(main)