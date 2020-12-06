import requests
import sys
import platform
from bs4 import BeautifulSoup
from datetime import datetime

global logins_list

class Login():
    def __init__(self, login : str, link : str, checked : str, number : int):
        self.login = login
        self.link = link
        self.checked = checked
        self.number = number
        self.date = self.date_to_date(checked)
    
    def date_to_date(self, string_date):
        string_date = string_date.split(' ')
        string_time = string_date[3].split(':')
        string_date = string_date[2].split('-')

        year = int(string_date[0])
        month = int(string_date[1])
        day = int(string_date[2])
        hour = int(string_time[0])
        minute = int(string_time[1])
        second = int(string_time[2])

        return(datetime(year, month, day, hour, minute, second))

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    if iteration == total: 
        print('\r%s |%s| %s%% %s' % (prefix, bar, ("{0:." + str(decimals) + "f}").format(100 * (total / float(total))), suffix), end = printEnd)

def load_from_web(trials):
    def get_logins():
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        url = 'http://freelogin.ru/'
        data = requests.get(url, headers = headers)
        soup = BeautifulSoup(data.text, features = "html.parser")

        links_list = []
        text_list = []

        for link in soup.find_all('a', {'class': 'item bg1'}):
            links_list.append(link.get('href'))

        for link in soup.find_all('span', {'class': 'cmted'}):
            text_list.append(link.get('data-title'))

        total_list = []
        count = 0

        for item in links_list:      
            total_list.append(Login(item.split('=')[2], item, text_list[count], 0))
            count += 1

        return(total_list)

    def supreme_get_logins(trials):
        logins_list = []

        i = 0
        while i != trials:
            try:
                log_lst = get_logins()
                for item in log_lst:
                    logins_list.append(item)
                printProgressBar(i, trials, prefix = 'Processing: ', suffix = 'Complete', decimals = 1, length = (size()[0] - 33), fill = '█', printEnd = "\r")

                i += 1

            except:
                None

        printProgressBar(100, 100, prefix = 'Processing: ', suffix = 'Complete', decimals = 1, length = (size()[0] - 33), fill = '█', printEnd = "")

        dct_sorted = {}
        for item in logins_list:
            dct_sorted[item.login] = item

        dct_sorted_2 = sorted(dct_sorted.keys())

        return_list = []
        for item in dct_sorted_2:
            return_list.append(dct_sorted[item])

        return(return_list)
    
    return(supreme_get_logins(trials))

def size():
    def get_terminal_size():
        current_os = platform.system()
        tuple_xy = None

        if current_os == 'Windows':
            tuple_xy = _get_terminal_size_windows()

            if tuple_xy is None:
                tuple_xy = _get_terminal_size_tput()

        if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
            tuple_xy = _get_terminal_size_linux()

        if tuple_xy is None:
            tuple_xy = (80, 25)
        return tuple_xy


    def _get_terminal_size_windows():

        try:
            from ctypes import windll, create_string_buffer
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            if res:
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom,
                 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex, sizey
        except:
            pass


    def _get_terminal_size_tput():

        try:
            cols = int(subprocess.check_call(shlex.split('tput cols')))
            rows = int(subprocess.check_call(shlex.split('tput lines')))
            return (cols, rows)
        except:
            pass


    def _get_terminal_size_linux():

        def ioctl_GWINSZ(fd):
            try:
                import fcntl
                import termios
                cr = struct.unpack('hh',
                                   fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
                return cr

            except:
                pass

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)

            except:
                pass

        if not cr:
            try:
                cr = (os.environ['LINES'], os.environ['COLUMNS'])

            except:
                return None

        return int(cr[1]), int(cr[0])

    def det_size():
        if __name__ == "__main__":
            sizex, sizey = get_terminal_size()

            return [sizex, sizey]
    return det_size()

def choose(logins_list : list, show_check : bool):
        
        if logins_list == 'Empty':
            print('No logins were found with given parameters!')
            return 0
        count = 1
     
        for item in logins_list:
            item.number = count
            count += 1

        lst = [len(item.login) for item in logins_list]
        space2 = max(lst)

        print('\n  List of all logins loaded: \n')

        count = 1

        if show_check == True:
            for item in logins_list:
                space = len(str(len(logins_list))) - len(str(count))
                spacecurr = space2 - len(item.login) + 3
                print(str(item.number) + '. ' + ' ' * space + item.login + ' ' * spacecurr + item.checked)
                count += 1

        else:
            for item in logins_list:
                space = len(str(len(logins_list))) - len(str(count))
                print(str(item.number) + '. ' + ' ' * space + item.login)
                count += 1

        print('\n')

def sorting(lst, mode, submode = 'empty', submode2 = 'empty'):
    if mode == 'date':
        temp_dct = {}
        final_lst = []
        
        for item in lst:
            temp_dct[item.login] = item.date
        temp_dct = {k: v for k, v in sorted(temp_dct.items(), key=lambda item: item[1])}
        
        for key in temp_dct:
            for item in lst:
                if item.login == key:
                    final_lst.append(item)
        
        if submode == 'newfirst':
            return([final_lst[len(final_lst) - i - 1] for i in range(len(final_lst))])
        elif submode == 'oldfirst':
            return(final_lst)
        else:
            None

    elif mode == 'lenght':
        if submode == 'strict':
            temp_lst = []
            for item in lst:
                if len(item.login) == submode2:
                    temp_lst.append(item)
            if temp_lst == []:
                return('Empty')
            else:
                return(temp_lst)
        elif submode == 'sort':
            if submode2 == 'lowtohigh':
                temp_lst = []
                lenght = 1
                while lenght != 20:
                    for item in lst:
                        if len(item.login) == lenght:
                            temp_lst.append(item)
                    lenght += 1
                return(temp_lst)
            elif submode2 == 'hightolow':
                temp_lst = []
                lenght = 20
                while lenght != 1:
                    for item in lst:
                        if len(item.login) == lenght:
                            temp_lst.append(item)
                    lenght -= 1
                return(temp_lst)
            else:
                None
        elif submode == 'pick':
            temp_lst = []
            for item in lst:
                if submode2 in item.login:
                    temp_lst.append(item)
            if temp_lst == []:
                return('Empty')
            else:
                return(temp_lst)
        else:
            None

def menu(logins_list):
    show_check = True
    while True:
        inp = input('Enter logins number to get registration link: ')

        if inp == '':

            if input('Press enter again to exit: ') == '':
                return 0

            else:
                None
        
        elif inp[0] == 'l':
            for item in logins_list:
                item.number = 'NA'
            if inp[1] == 'p':
                choose(sorting(logins_list, 'lenght', 'pick', inp.split('-')[1]), show_check)
            
            elif inp[1] == 's':
                if inp[2] == 'l':
                    choose(sorting(logins_list, 'lenght', 'sort', 'hightolow'), show_check)
                elif inp[2] == 'h':
                    choose(sorting(logins_list, 'lenght', 'sort', 'lowtohigh'), show_check)
                else:
                    None
            
            elif inp[1] == 'l':
                choose(sorting(logins_list, 'lenght', 'strict', int(inp.split('-')[1])), show_check)
            
            else:
                None
                
        elif inp[0] == 'd':
            for item in logins_list:
                item.number = 'NA'
            if inp[1] == 'n':
                choose(sorting(logins_list, 'date', 'newfirst'), show_check)
            elif inp[1] == 'o':
                choose(sorting(logins_list, 'date', 'oldfirst'), show_check)
            else:
                None
        elif inp[0] == 'r':
            for item in logins_list:
                item.number = 'NA'
            choose(logins_list, show_check)
                       
        else:
            try:
                inp = int(inp)
                for item in logins_list:
                    if item.number == inp:
                        print('\n' + item.link + '\n')
            except:
                print('\nIncorrect number!\n')

def start():
    if len(sys.argv) == 1:
        tr = input('Enter number of trials (each trial gets 20 logins): ')
    else:
        tr = sys.argv[1]
    
    try:
        tr = int(tr)
    except:
        print('Inccorect number of trials, exiting...')
        input('Press enter to exit: ')
        sys.exit()
    
    logins_list = load_from_web(tr)
    choose(logins_list, True)
    exit = 1
    while exit != 0:
        try:
            exit = menu(logins_list)
        except:
            None

start()
