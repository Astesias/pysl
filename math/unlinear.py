import nlopt # 导入模块


# 定义代价函数
class ObjectiveFunction():
    def __init__(self):
        self.n_calls = 0 # 记录运行次数
     # 这里代价函数的思想是不满足条件的情况下把代价函数设置成最大值，因为目前我测试的是最小化代价函数，因此返回代价函数的导数
    def __call__(self, par_values, grad=None):
        x1 = par_values[0]
        x2 = par_values[1]
        x3 = par_values[2]
        obj_func = 6*x1+4*x2+3*x3
        if x1+x2+x3 > 95 or 6*x1+5*x2+2*x3 > 400 or 5*x1+2*x2 > 200 or 12*x1+10*x2+16*x3 > 1200:
            obj_func = 1
        self.n_calls += 1
        return 1/obj_func

x1 = [1,95]
x2 = [1,95]
x3 = [1,95]
objfunc_calculator = ObjectiveFunction()
opt = nlopt.opt(nlopt.LN_SBPLX, 3)
# Assign the objective function calculator
opt.set_min_objective(objfunc_calculator)
# lower bounds of parameters values
opt.set_lower_bounds([x1[0], x2[0], x3[0]])
# upper bounds of parameters values
opt.set_upper_bounds([x1[1], x2[1], x3[1]])
# the initial step size to compute numerical gradients
opt.set_initial_step([0.5,0.5,0.5])
# Maximum number of evaluations allowed
opt.set_maxeval(1000000)
# Relative tolerance for convergence
# opt.set_stopval(0.5)
opt.set_xtol_rel(1e-20)
# Start the optimization with the first guess
firstguess = [15,20,12]
x = opt.optimize(firstguess)
print("\noptimum at x1: %s, x2: %s, x3: %s,"% (x[0], x[1], x[2]))
print("function value = ",  1/(opt.last_optimum_value()))
print("result code = ", opt.last_optimize_result())
print("With %i function calls" % objfunc_calculator.n_calls)