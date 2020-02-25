from random import *
from math import *
import code_work as cw

class GeneticAlgorithm:
	Pc = 0.9							#вероятность скрещивания
	Pm = 0.2							#вероятность мутации
	p_size = 0							#размер популяции
	iters = 0							#кол-во итераций
	left = 0							#xmin
	right = 0							#xmax
	code_size = 0						#макс. кол-во бит под хромосому
	roulette = False					#редукция по методу рулетки
	best_pairs = False					#отбор пар среди лучших
	
	f = None
	F = None
	protocol = ""
	
	target_func_y = []
	target_func_x = []
	fitness_func_x = []
	fitness_func_y = []
	step_size = 0
	
	now_iter = 0
	
	population = []
	
	#-------------------------------------
	def __init__(self, f, F, left, right, p_size, code_size):			#установка функций и интервалов
		self.f = f
		self.F = F
		self.left = left
		self.right = right
		self.code_size = code_size
		self.change_population_size(p_size)
	#--------------------------------------------
	def change_population_size(self, new_p_size):
		self.reset()
		self.p_size = new_p_size	
		self.step_size = (fabs(self.right-self.left))/(1<<self.code_size)
		self.calculate_target_func()						#расчет целевой функции
		self.calculate_fintess_func()						#расчет функции приспособленности
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
		for i in range(0, 1<<self.code_size):
			self.target_func_x.append( self.left+self.step_size*i )
			self.target_func_y.append( self.f(self.left+self.step_size*i) )
	#--------------------------------
	def calculate_fintess_func(self):						#расчет функции приспособленности по значениями целевой
		self.fitness_func_x = self.target_func_x.copy()
		self.fitness_func_y = []
		for i in range(0, len(self.target_func_x)):
			self.fitness_func_y.append( self.F(self.left+self.step_size*i) )
	#--------------------------------------------
	def setup(self, iterations, roulette=True, best_pairs=False):#установка кол-ва итераций и размера популяции
		self.change_iterations_num(iterations)
		self.roulette = roulette
		self.best_pairs = best_pairs
	#-------------------------------
	def population_to_dots(self):
		dots = []
		for person in self.population:
			x = self.left+self.step_size*person
			value = self.f(x)
			dots.append([x, value])
		return dots
	#------------------------------------
	def add_population_in_protocol(self):					#добавление популяции в протокол
		self.protocol += "|№\t\t|x\t\t|хромосома\t\t\t|f(x)\t\t|F(x)\t\t|\n"
		for i in range(0, len(self.population)):
			person = self.population[i]
			chromo = cw.supplement( cw.bin_str_from( person ), self.code_size )
			x=self.left+self.step_size*person
			fx = self.f(x)
			Fx = self.F(x)
			self.protocol += f"|{ i+1 }\t\t|{x:.2f}\t\t|{ chromo }\t\t\t|{fx:.2f}\t\t|{Fx:.2f}\t\t|\n"
	#-----------------------------
	def generate_population(self):							#генерация начальной популяции без повторений
		if self.p_size > len(self.target_func_x):
			self.generate_population2()
			return
		self.population = []
		nums = list( range(0, len(self.target_func_x)) )
		for i in range(0, self.p_size):
			self.population.append(nums.pop( randint(0, len(nums)-1) ))
	#------------------------------
	def generate_population2(self):							#генерация начальной популяции с повторениями
		self.population = []
		for i in range(0, self.p_size):
			element = randint(0, len(self.target_func_x)-1)
			self.population.append(element)
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
			
		self.iteration()
		self.now_iter += 1
		best_idx = self.find_best(self.population)
		person = self.population[best_idx]
		best_x = self.left+self.step_size*person
		
		if step_mode or self.now_iter == 3 or self.now_iter >= self.iters:	#добавление информации популяции в протокол
			self.protocol += "НОВАЯ ИТЕРАЦИЯ\n"
			self.protocol += f"Популяция на итерации №{self.now_iter}:\n"
			self.add_population_in_protocol()
			fx = self.f(best_x)
			Fx = self.F(best_x)
			self.protocol += f"На итерации {self.now_iter} лучшая особь под номером {best_idx+1} с x={best_x:.2f} f(x)={fx:.2f} F(x)={Fx:.2f}\n"
			self.protocol += f"Средняя приспособленность популяции={self.find_average():.2f}\n"
			
		return best_x
	#-------------------
	def iteration(self):									#одна итерация алгоритма
		childs = self.crossbreeding()						#получение потомков путем скрещивания
		self.mutation(childs)								#мутация потомков
		self.population += childs							#расширение потомков
		if self.roulette:									#отбор лучших особей
			self.roulette_reduction()						
		else:
			self.tournament_reduction()
	#-----------------------
	def crossbreeding(self):								#скрещивание пар
		pairs = self.make_pairs()							#получаем пары родителей
		if len(pairs) == 0:									#если не удалось ни одного скрещивания
			return []
		childs = []
		for parents in pairs:
			p1 = parents[0]
			p2 = parents[1]
			k = randint(1, self.code_size - 1)
			mask = 0
			while k:										#расчитываем битовую маску
				mask ^= 1<<(self.code_size-k) 
				k -= 1
			c1 = (p1&mask) | (p2&~mask)						#берем левую часть от 1-го и правую от 2-го
			c2 = (p2&mask) | (p1&~mask)						#берем левую от 2-го и правую от 1-го
			childs += [c1, c2]
		return childs
	#--------------------
	def make_pairs(self):									#создание пар родителей
		pairs = []
		parents = self.population.copy()
		while len(parents) > 1:								#пока особей от 2-х и выше
			if(random() < self.Pc):							#если есть вероятность создания пары
				if self.best_pairs:							#лучшие с лучшими
					p1 = parents.pop( self.find_best(parents) )
					p2 = parents.pop( self.find_best(parents) )
				else:										#случайный отбор
					p1 = parents.pop( randint(0, len(parents) - 1) )
					p2 = parents.pop( randint(0, len(parents) - 1) )
				pairs.append([p1, p2])
		return pairs
	#--------------------------
	def mutation(self, childs):								#мутация потомков
		for i in range(0, len(childs)):
			if random() < self.Pm:							#если есть вероятность мутации
				n = randint(0, self.code_size - 1)
				childs[i] ^= 1 << (self.code_size-n-1)
	#-------------------
	def roulette_reduction(self):							#отбор популяции(метод рулетки)
		next_population = []
		while len(next_population) < self.p_size:			#пока не набрали необходимое кол-во
			Fs = self.total_fitness()						#рассчитываем суммарную приспособленность
			left = 0
			right = 0
			i = 0
			c = random()
			while True:
				value = self.population[i]
				x = self.left + self.step_size * value
				relative_F = self.F(x)/Fs
				right = left + relative_F 								#относительная приспособленность особи
				if left<=c<=right or i+1 == len(self.population):							 
					next_population.append( self.population.pop(i) )	#отбираем в след. популяцию
					break
				i += 1
				left = right
		self.population = next_population
	#------------------------------
	def tournament_reduction(self):							#отбор популяции(метод турнира)
		next_population = []
		while len(next_population) < self.p_size:
			best_idx = -1
			best_value = 0
			for i in range(0, len(self.population)):
				person = self.population[i]
				x = self.left + self.step_size * person
				F = self.F(x)
				if F > best_value:
					best_idx = i
					best_value = F
			next_population.append(self.population.pop( best_idx ))
		self.population = next_population
	#-----------------------
	def total_fitness(self):								#расчет суммарной приспособленности популяции
		sum = 0
		for person in self.population:
			x = self.left + self.step_size * person
			sum += self.F(x)
		return sum
	#-------------------
	def find_best(self, persons):						#поиск наиболее приспособленной особи
		best_idx = 0
		best_value = 0
		for i in range(0, len(persons)):
			x = self.left + self.step_size * persons[i]
			F_value = self.F(x)
			if F_value > best_value:
				best_idx = i
				best_value = F_value
		return best_idx
	#----------------------
	def find_average(self):
		sum = 0
		for person in self.population:
			x = self.left + self.step_size * person
			sum += self.F(x)
		sum /= len(self.population)
		return sum
#---GeneticAlgorithm END---