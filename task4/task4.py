import argparse

def string_match(comparing_string, compared_string):
    i = 0
    while i < len(compared_string):
        if compared_string[i] == '*':
            print('OK')
            break
        elif compared_string[i] == comparing_string[i]:
            if i == (len(comparing_string)-1) or i == (len(compared_string)-1):
                if len(comparing_string) == len(compared_string) and (comparing_string[-1] or compared_string[-1]):
                    print('OK')
                    break
                else:
                    i+=1
                    continue
            i+=1
            continue
        else:
            print('KO')
            break
        print('OK')

def main(comparing_string, compared_string):
    try:
        string_match(comparing_string, compared_string)
    except:
        print('Ошибка ввода!')
    
def createParser ():
    par = argparse.ArgumentParser()
    par.add_argument('first', nargs='?')
    par.add_argument('second', nargs='?')    
    return par
        
if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    main(args.first, args.second)
    

    
