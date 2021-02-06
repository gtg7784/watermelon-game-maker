from subprocess import PIPE, Popen

def deploy(email, uuid):
    p = Popen(f'cd ./tmp/{uuid}/daxigua/;vercel', stdout=PIPE, stdin=PIPE, shell=True, universal_newlines=True)
    # for out in p.stdout.readlines():
    #     print(out)
    out, err = p.communicate('Y\n\n')
    print(out)
    # p.stdin.write('Y')

if __name__ == "__main__":
    deploy("tae.gun7784@gmail.com", "5e41e684-bcda-4430-8270-c6da094a8c87")