import argparse

# ввод функции
def convert_base(num, to_base, from_base=10):
    if to_base.isdigit():
# преобразование исходного в десятичное        
        if isinstance(num, str):   
            n = int(num, base = from_base)
        else:
            n = int(num)
# преобразование в базовую систему
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n < len(to_base):
            return alphabet[n]
        else:
            return convert_base(n // len(to_base), to_base, from_base) + alphabet[n % len(to_base)]
    else:
        print(num, end = ' ' )
        return to_base

def main(int_nb, string_base):
    try:
        print(convert_base(int_nb, string_base))
    except:
        print('Должно быть натуральное число!')
    
def createParser ():
    par = argparse.ArgumentParser()
    par.add_argument('num', nargs='?')
    par.add_argument('base', nargs='?')    
    return par
       
if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    num = ''
    base = ''
    main(args.num, args.base)


    