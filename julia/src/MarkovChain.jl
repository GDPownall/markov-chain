# This file contains the struct for the markov chain 

struct MarkovChain
    mat::ProbMatrix
    initial::Array{Real,1}

    function MarkovChain(mat,initial)
	if sum(initial) != 1
		error("Sum of initial probabilities must be one.")
	end
	new(mat,initial)
    end

end
