
include("src/MarkovChainModule.jl")

using ..MarkovChainModule
using LinearAlgebra

Mat = [0.8 0.05 ; 0.2 0.95]

#println(Mat)


A = ProbMatrix(Mat)

#println(inv(A))
#println(eigvals(A))
#println(eigvecs(A))

init = [1,0]

x = MarkovChain(A,init)

eq = EquationOfMotion(x)
println(stationarystate(eq))
