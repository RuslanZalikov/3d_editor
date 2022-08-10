def f(*args):
    args = list(args)
    args.append(args[0])
    print(args)
f(1, 2, 3)
