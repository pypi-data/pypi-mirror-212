from ik_solvers import PyIKSolver

if __name__ == '__main__':
    ik_solver = PyIKSolver.load("forward_dynamics","ur10e.urdf","base_link","ft_sensor",[-3.14,-3.14,-3.14,-3.14,-3.14,-3.14], [3.14,3.14,3.14,3.14,3.14,3.14])
    ik_solver.setStartState([0,0,0,0,0,0],[0,0,0,0,0,0])
    


