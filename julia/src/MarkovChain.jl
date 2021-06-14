# This file contains the struct for the markov chain 

include("ProbMatrix.jl")

module MarkovChainDef

using ..ProbMatrixDef

export MarkovChain 

struct MarkovChain
    mat::ProbMatrix
    initial::AbstractArray

    function MarkovChain(mat,initial)
	if sum(initial) != 1
		error("Sum of initial probabilities must be one.")
	end
	new(mat,initial)
    end

end

Mat = [0.8 0.05 ; 0.2 0.95]

A = ProbMatrix(Mat)

init = [1 0]

x = MarkovChain(A,init)

end
