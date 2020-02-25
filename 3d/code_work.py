#перевод числа в код грэя
def bin_to_gray(num):
	return num^(num>>1)

#обратный перевод
def gray_to_bin(num):
	bin = 0
	while num != 0:
		bin^=num
		num=num>>1
	return bin

#перевод массива чисел в код грэя
def list_from_bin_to_gray(list_num):
	new_list = []
	for i in list_num:
		new_list.append( bin_to_gray(i) )
	return new_list

#перевод массива кодов грэя в бинарный вид
def list_from_gray_to_bin(list_num):
	new_list = []
	for i in list_num:
		new_list.append( gray_to_bin(i) )
	return new_list

#перевод числа в строку бинарного кода
def bin_str_from(num):
	bin_num = str(bin(num))
	return bin_num[2:len(bin_num)]

#дополнение строки бинарного кода до нужного кол-ва разрядов
def supplement(num, size):
	return "0"*(size-len(num))+num