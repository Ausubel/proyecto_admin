def run():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1') for line in lines]



if __name__=='__main__':
    run()