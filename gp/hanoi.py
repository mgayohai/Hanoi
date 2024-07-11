import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file

    add_propositions(disks, domain_file, n_, pegs)
    add_actions(disks, domain_file, n_, pegs)

    domain_file.close()


def add_propositions(disks, domain_file, n_, pegs):
    """
    Add the propositions of a 'Towers of Hanoi' game to the domain file
    :param disks: A list of disk names
    :param domain_file: The domain file
    :param n_: The number of disks
    :param pegs: A list of the disks names
    """
    domain_file.write("Propositions:\n")
    for peg in pegs:
        domain_file.write(f"empty_{peg} ")
        for disk in disks:
            domain_file.write(f"{disk}_on_{peg} ")
    for disk in disks:
        domain_file.write(f"{disk}_top ")
    for i in range(n_):
        for j in range(i + 1, n_):
            domain_file.write(f"{disks[i]}_on_{disks[j]} ")
    domain_file.write("\n")


def add_actions(disks, domain_file, n_, pegs):
    """
    Add actions of a 'Towers of Hanoi' game to the domain file
    :param disks: A list of disk names
    :param domain_file: The domain file
    :param n_: The number of disks
    :param pegs: A list of the disks names
    """
    domain_file.write("Actions:\n")
    move_between_pegs(disks, domain_file, pegs)
    move_from_peg_to_disk(disks, domain_file, n_, pegs)
    move_from_disk_to_peg(disks, domain_file, n_, pegs)
    move_from_disk_to_disk(disks, domain_file, n_)


def move_from_disk_to_disk(disks, domain_file, n_):
    """
    Adds to the domain file, the action of moving a disk from one disk to another.
    :param disks: A list of disk names
    :param domain_file: The domain file
    :param n_: The number of disks
    """
    for i in range(n_):
        for j in range(i + 1, n_):
            for k in range(i + 1, n_):
                if j != k:
                    domain_file.write(f"Name: Move_{disks[i]}_from_{disks[j]}_to_{disks[k]} \n")
                    domain_file.write(f"pre: {disks[i]}_top {disks[i]}_on_{disks[j]} {disks[k]}_top \n")
                    domain_file.write(f"add: {disks[i]}_on_{disks[k]} {disks[j]}_top\n")
                    domain_file.write(f"delete: {disks[k]}_top {disks[i]}_on_{disks[j]}\n")


def move_from_disk_to_peg(disks, domain_file, n_, pegs):
    """
    Adds to the domain file, the action of moving a disk from a disk to an empty peg.
    :param disks: A list of disk names
    :param domain_file: The domain file
    :param n_: The number of disks
    :param pegs: A list of the disks names
    """
    for i in range(n_):
        for j in range(i + 1, n_):
            for peg in pegs:
                domain_file.write(f"Name: Move_{disks[i]}_from_{disks[j]}_to_{peg} \n")
                domain_file.write(f"pre: {disks[i]}_top {disks[i]}_on_{disks[j]} empty_{peg} \n")
                domain_file.write(f"add: {disks[i]}_on_{peg} {disks[j]}_top\n")
                domain_file.write(f"delete: empty_{peg} {disks[i]}_on_{disks[j]}\n")


def move_from_peg_to_disk(disks, domain_file, n_, pegs):
    """
    Adds to the domain file, the action of moving a disk from an empty peg to a disk.
    :param disks: A list of disk names
    :param domain_file: The domain file
    :param n_: The number of disks
    :param pegs: A list of the disks names
    """
    for i in range(n_):
        for j in range(i + 1, n_):
            for peg in pegs:
                domain_file.write(f"Name: Move_{disks[i]}_from_{peg}_to_{disks[j]} \n")
                domain_file.write(f"pre: {disks[i]}_top {disks[i]}_on_{peg} {disks[j]}_top \n")
                domain_file.write(f"add: {disks[i]}_on_{disks[j]} empty_{peg}\n")
                domain_file.write(f"delete: {disks[j]}_top {disks[i]}_on_{peg}\n")


def move_between_pegs(disks, domain_file, pegs):
    """
    Adds to the domain file, the action of moving a disk from an empty peg to another empty peg.
    :param disks: A list of disk names
    :param domain_file: The domain file
    :param pegs: A list of the disks names
    """

    for disk in disks:
        for peg_src in pegs:
            for peg_dest in pegs:
                if peg_src != peg_dest:
                    domain_file.write(f"Name: Move_{disk}_from_{peg_src}_to_{peg_dest} \n")
                    domain_file.write(f"pre: {disk}_top {disk}_on_{peg_src} empty_{peg_dest} \n")
                    domain_file.write(f"add: {disk}_on_{peg_dest} empty_{peg_src} \n")
                    domain_file.write(f"delete: {disk}_on_{peg_src} empty_{peg_dest} \n")


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file

    problem_file.write("Initial state: ")

    # Set the smallest disk on top
    problem_file.write(f"{disks[0]}_top ")

    # Set all pegs that as empty (except the tower)
    for j in range(1, m_):
        problem_file.write(f"empty_{pegs[j]} ")

    # Set all disk on top of the one another (scaling)
    for i in range(n_ - 1):
        problem_file.write(f"{disks[i]}_on_{disks[i + 1]} ")
    problem_file.write(f"{disks[n_ - 1]}_on_{pegs[0]} \n")

    problem_file.write("Goal state: ")
    for p in range(m_ - 1):
        problem_file.write(f"empty_{pegs[p]} ")

    # Set all disk on top of the one another (scaling)
    for i in range(n_ - 1):
        problem_file.write(f"{disks[i]}_on_{disks[i + 1]} ")
    problem_file.write(f"{disks[n_ - 1]}_on_{pegs[m_ - 1]} ")

    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
