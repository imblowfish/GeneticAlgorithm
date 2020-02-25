from random import *
from math import *
import code_work as cw

class GeneticAlgorithm:
	Pc = 0.9							#вероятность скрещивания
	Pm = 0.15							#вероятность мутации
	p_size = 0							#размер популяции
	iters = 0							#кол-во итераций
	left = 0							#xmin
	right = 0							#xmax
	code_size = 0						#макс. кол-во бит под хромосому
	best_pairs = False					#отбор пар среди лучших
	
	f = None
	F = None
	protocol = ""
	
	target_func_y = []
	target_func_x = []
	target_func_z = []
	fitness_func_x = []
	fitness_func_y = []
	fitness_func_z = []
	step_size = 0
	
	now_iter = 0
	
	population_x = []
	population_y = []
	
	#-------------------------------------
	def __init__(self, f, F, left, right, p_size, code_size):			#установка функций и интервалов
		self.f = f
		self.F = F
		self.left = left
		self.right = right
		self.code_size = code_size
		self.change_population_size(p_size)
		interval_nums = int(sqrt(1<<self.code_size))
		self.step_size = (fabs(self.right-self.left))/(1<<code_size)
		self.calculate_target_func()						#расчет целевой функции
		self.calculate_fintess_func()						#расчет функции приспособленности
	#--------------------------------------------
	def change_population_size(self, new_p_size):
		if(self.p_size == new_p_size):
			return
		self.reset()
		self.p_size = new_p_size	
	#--------------------------------------------------
	def change_iterations_num(self, new_iteration_num):
		self.iters = new_iteration_num
	#---------------
	def reset(self):
		self.population = []
		self.now_iter = 0
	#-------------------------------
	def calculate_target_func(self):						#расчет значений целевой функции в интервале
		self.target_func_x = []
		self.target_func_y = []
		self.target_func_z = []
		interval_nums = int(sqrt(1<<self.code_size))
		step = (fabs(self.right-self.left))/(interval_nums)
		for i in range(0, interval_nums):
			x = self.left+step*i
			for j in range(0, interval_nums):
				y = self.left+step*j
				self.target_func_x.append(x)
				self.target_func_y.append(y)
				self.target_func_z.append(self.f(x, y))
	#--------------------------------
	def calculate_fintess_func(self):						#расчет функции приспособленности по значениями целевой
		self.fitness_func_x = []
		self.fitness_func_y = []
		interval_nums = int(sqrt(1<<self.code_size))
		step = (fabs(self.right-self.left))/(interval_nums)
		for i in range(0, len(self.target_func_x)):
			x = self.target_func_x[i]
			y = self.target_func_y[i]
			self.fitness_func_x.append( x )
			self.fitness_func_y.append( y )
			self.fitness_func_z.append( self.F(x, y))
	#--------------------------------------------
	def setup(self, iterations, best_pairs=False):#установка кол-ва итераций и размера популяции
		self.change_iterations_num(iterations)
		self.best_pairs = best_pairs
	#-------------------------------
	def population_to_dots(self):	
		dots = []
		for i in range(0, len(self.population_x)):
			x = self.left + self.step_size*self.population_x[i]
			y = self.left + self.step_size*self.population_y[i]
			z = self.f(x, y)
			dots.append([x, y, z])
		return dots
	#------------------------------------
	def add_population_in_protocol(self):					#добавление популяции в протокол
		self.protocol += "|№\t|x\t|y\t|хромосома x\t\t\t|хромосома y\t\t\t|f(x,y)\t|F(x,y)\t|\n"
		for i in range(0, len(self.population_x)):
			x = self.left + self.step_size*self.population_x[i]
			y = self.left + self.step_size*self.population_y[i]
			chromo_x = cw.supplement( cw.bin_str_from( self.population_x[i] ), self.code_size )
			chromo_y = cw.supplement( cw.bin_str_from( self.population_y[i] ), self.code_size )
			fx = self.f(x, y)
			Fx = self.F(x, y)
			self.protocol += f"|{ i+1 }\t|{x:.2f}\t|{y:.2f}\t|{ chromo_x }\t\t\t|{ chromo_y }\t\t\t|{fx:.2f}\t|{Fx:.2f}\t|\n"
	#-----------------------------
	def generate_population(self):							#генерация начальной популяции без повторений
		if self.p_size > len(self.target_func_x):
			self.generate_population2()
			return
		self.population_x = []
		self.population_y = []
		nums_x = list( range(0, 1<<self.code_size ))
		nums_y = nums_x.copy()
		for i in range(0, self.p_size):
			n = randint(0, 1<<self.code_size-1)
			self.population_x.append(nums_x.pop( n ))
			n = randint(0, 1<<self.code_size-1)
			self.population_y.append(nums_y.pop( n ))
	#------------------------------
	def generate_population2(self):							#генерация начальной популяции с повторениями
		self.population_x = []
		self.population_y = []
		for i in range(0, self.p_size):
			element = randint(0, 1<<self.code_size-1)
			self.population_x.append(element)
			element = randint(0, 1<<self.code_size-1)
			self.population_y.append(element)
	#-------------
	def run(self):											#запуск алгоритма с полным проходом
		self.reset()
		best = None
		for i in range(0, self.iters):
			best = self.step()
		return best
	#--------------
	def step(self, step_mode = False):						#один шаг алгоритма с возвратом лучшей особи
		if len(self.population) == 0:
			self.generate_population()
			self.protocol = f"Нулевая популяция:\n"
			self.add_population_in_protocol()
			self.protocol += f"Среднее значение между особями={self.find_average():.2f}\n"

		if self.now_iter >= self.iters:
			self.protocol += "Конец алгоритма\n"
			return
			
		self.now_iter += 1
		best_idx = self.iteration()
		best_x = self.left+self.step_size*self.population_x[best_idx]
		best_y = self.left+self.step_size*self.population_y[best_idx]
		fx = self.f(best_x, best_y)
		if step_mode or self.now_iter == 3 or self.now_iter >= self.iters:	#добавление информации популяции в протокол
			self.protocol += "НОВАЯ ИТЕРАЦИЯ\n"
			self.protocol += f"Популяция на итерации №{self.now_iter}:\n"
			self.add_population_in_protocol()
			fx = self.f(best_x, best_y)
			Fx = self.F(best_x, best_y)
			self.protocol += f"На итерации {self.now_iter} лучшая особь с x={best_x:.2f} y={best_y:.2f} f(x,y)={fx:.2f} F(x,y)={Fx:.2f}\n"
			self.protocol += f"Средняя приспособленность популяции={self.find_average():.2f}\n"
			
		return [[best_x, best_y, fx]]
	#-------------------
	def iteration(self):									#одна итерация алгоритма
		[childs_x, childs_y] = self.crossbreeding()						#получение потомков путем скрещивания
		self.mutation(childs_x, childs_y)					#мутация потомков
		self.population_x += childs_x							#расширение потомков
		self.population_y += childs_y							#расширение потомков
		return self.tournament_reduction()
	#-----------------------
	def crossbreeding(self):								#скрещивание пар
		[pairs_x, pairs_y] = self.make_pairs()				#получаем пары родителей
		if len(pairs_x) == 0:								#если не удалось ни одного скрещивания
			return []
		childs_x = []
		childs_y = []
		for i in range(0, len(pairs_x)):
			p1 = pairs_x[i][0]
			p2 = pairs_x[i][1]
			k = randint(1, self.code_size - 1)
			mask = 0
			while k:												#расчитываем битовую маску
				mask ^= 1<<(self.code_size-k) 
				k -= 1
			c1 = (p1&mask) | (p2&~mask)						#берем левую часть от 1-го и правую от 2-го
			c2 = (p2&mask) | (p1&~mask)						#берем левую от 2-го и правую от 1-го
			childs_x += [c1, c2]
			
			p1 = pairs_y[i][0]
			p2 = pairs_y[i][1]
			k = randint(1, self.code_size - 1)
			mask = 0
			while k:										#расчитываем битовую маску
				mask ^= 1<<(self.code_size-k) 
				k -= 1
			c1 = (p1&mask) | (p2&~mask)						#берем левую часть от 1-го и правую от 2-го
			c2 = (p2&mask) | (p1&~mask)						#берем левую от 2-го и правую от 1-го
			childs_y += [c1, c2]
		return [childs_x, childs_y]
	#--------------------
	def make_pairs(self):									#создание пар родителей
		pairs_x = []
		pairs_y = []
		parents_x = self.population_x.copy()
		parents_y = self.population_y.copy()
		while len(parents_x) > 1:							#пока особей от 2-х и выше
			if(random() < self.Pc):							#если есть вероятность создания пары
				n = randint(0, len(parents_x) - 1)
				p1 = parents_x.pop( n )
				n = randint(0, len(parents_x) - 1)
				p2 = parents_x.pop( n )
				pairs_x.append([p1, p2])
		while len(pairs_y) < len(pairs_x):
			if(random() < self.Pc):
				n = randint(0, len(parents_y) - 1)
				p1 = parents_y.pop( n )
				n = randint(0, len(parents_y) - 1)
				p2 = parents_y.pop( n )
				pairs_y.append([p1, p2])
		return [pairs_x, pairs_y]
	#--------------------------
	def mutation(self, childs_x, childs_y):								#мутация потомков
		for i in range(0, len(childs_x)):
			if random() < self.Pm:							#если есть вероятность мутации
				n = randint(0, self.code_size - 1)
				childs_x[i] ^= 1 << (self.code_size-n-1)
				n = randint(0, self.code_size - 1)
				childs_y[i] ^= 1 << (self.code_size-n-1)
	#------------------------------
	def tournament_reduction(self):							#отбор популяции(метод турнира)
		next_population_x = []
		next_population_y = []
		best_of_the_best_idx = 0
		best_of_the_best_value = 0
		while len(next_population_x) < self.p_size:
			best_idx = 0
			best_value = 0
			for i in range(0, len(self.population_x)):
				x = self.left+self.step_size*self.population_x[i]
				y = self.left+self.step_size*self.population_y[i]
				F = self.F(x, y)
				if F > best_value:
					best_idx = i
					best_value = F
			next_population_x.append(self.population_x.pop( best_idx ))
			next_population_y.append(self.population_y.pop( best_idx ))
			
			if best_value > best_of_the_best_value:
				best_of_the_best_idx = len(next_population_x)-1
				best_of_the_best_value = best_value
		self.population_x = next_population_x
		self.population_y = next_population_y
		return best_of_the_best_idx
	#----------------------
	def find_average(self):
		sum = 0
		nums = int(sqrt(1<<self.code_size))
		for i in range(0, len(self.population_x)):
			x = self.left+self.step_size*self.population_x[i]
			y = self.left+self.step_size*self.population_y[i]
			sum += self.F(x, y)
		sum /= len(self.population_x)
		return sum
#---GeneticAlgorithm END---