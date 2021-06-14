
include("src/MarkovChainModule.jl")

using ..MarkovChainModule

Mat = [0.8 0.05 ; 0.2 0.95]

println(Mat)


A = ProbMatrix(Mat)

println(inv(A))

init = [1 0]

x = MarkovChain(A,init)
