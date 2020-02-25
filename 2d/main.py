from genetic_algorithm import GeneticAlgorithm
from interface import *
from math import *

#интервал функции
# left = -1
# right = 1
left = -6
right = 6
#настройки алгоритма
p_size = 100					#размер популяции
code_size = 20						#длина кода
#--------
def f(x, y):						#целевая функция
	return 0.1*x+0.2*y-4*cos(x)+4*cos(0.9*y)+5
#-------------
def F(x, y):						#функция приспособленности
	return 0.1*x+0.2*y-4*cos(x)+4*cos(0.9*y)+5

ga = GeneticAlgorithm(f, F, left, right, p_size, code_size)

screen = Interface("1000x600")
elements = {}			

#----------
def main():
	ga.setup(iterations=20, best_pairs=False)
	draw_interface()
	screen.start()
#--------------------	
def draw_interface():
	#графики
	elements["target_function"] = screen.add_graphic(4, 3, 600, 0)
	elements["fitness_function"] = screen.add_graphic(4, 3, 600, 300)
	draw_graphic()
	#метки
	screen.add_label("Левая граница="+str(left), 10, 10)
	screen.add_label("Правая граница="+str(right), 10, 30)
	screen.add_label("Размер популяции=", 10, 50)
	screen.add_label("Кол-во итераций=", 10, 70)
	screen.add_label("ПРОТОКОЛ:", 10, 170)
	#текстовые поля
	elements["population_num"] = screen.add_textbox(8, 1, str(ga.p_size), 120, 50)
	elements["iterations"] = screen.add_textbox(8, 1, str(ga.iters), 120, 70)
	elements["protocol"] = screen.add_textbox(95, 28, "", 10, 200)
	#кнопки
	screen.add_button("Полный проход", 100, 100, run)
	screen.add_button("Полный проход пошагово", 190, 100, run_with_interval)
	screen.add_button("Одна итерация", 10, 100, step)
	screen.add_button("Сброс", 350, 100, reset)
#------------------	
def draw_graphic(best = None):
	screen.draw_graphic(elements["target_function"], "Целевая фунцкция", "x", "y", "f(x)", ga.target_func_x, ga.target_func_y, ga.target_func_z)
	screen.draw_graphic(elements["fitness_function"], "Функция приспособленности", "x", "y", "F(x)", ga.fitness_func_x, ga.fitness_func_y, ga.fitness_func_z)
	screen.draw_dots(elements["target_function"], ga.population_to_dots())
	if not best is None:
		screen.draw_dots(elements["target_function"], best)
#---------
def run():
	screen.clear_textbox(elements["protocol"])
	ga.change_iterations_num(int(screen.get_text_from_textbox(elements["iterations"])))
	ga.change_population_size(int(screen.get_text_from_textbox(elements["population_num"])))
	best = ga.run()
	screen.update_textbox(elements["protocol"], ga.protocol)
	draw_graphic(best)
#-----------------------
def run_with_interval():
	screen.clear_textbox(elements["protocol"])
	ga.change_iterations_num(int(screen.get_text_from_textbox(elements["iterations"])))
	ga.change_population_size(int(screen.get_text_from_textbox(elements["population_num"])))
	ga.reset()
	for i in range(0, ga.iters):
		best = ga.step(step_mode=True)
		screen.update_textbox(elements["protocol"], ga.protocol)
		if best is None:
			break
		if i%5 == 0:
			draw_graphic(best)	
	draw_graphic(best)	
#----------
def step():
	ga.change_iterations_num(int(screen.get_text_from_textbox(elements["iterations"])))
	ga.change_population_size(int(screen.get_text_from_textbox(elements["population_num"])))
	best = ga.step(step_mode = True)
	if not best is None:
		screen.update_textbox(elements["protocol"], ga.protocol)
		draw_graphic(best)
	else:
		screen.update_textbox(elements["protocol"], "Больше нет итераций, нажмите Сброс")
#-----------
def reset():
	ga.reset()
	screen.clear_textbox(elements["protocol"])
	screen.draw_graphic(elements["target_function"], "Целевая фунцкция", "x", "y", "f(x)", ga.target_func_x, ga.target_func_y, ga.target_func_z)
	screen.draw_graphic(elements["fitness_function"], "Функция приспособленности", "x", "y", "F(x)", ga.fitness_func_x, ga.fitness_func_y, ga.fitness_func_z)

main()