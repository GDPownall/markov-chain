# This file contains the struct for the markov chain 

using LinearAlgebra

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

struct EquationOfMotion
	eigvals
	eigvecs
	constants

	function EquationOfMotion(m::MarkovChain)
		eigvals = LinearAlgebra.eigvals(m.mat)
		eigvecs = transpose(LinearAlgebra.eigvecs(m.mat))
		#normalize
		for row_num in 1:size(eigvecs,2)
			# Find element with largest absolute value in each row
			multi = argmax(map(abs,eigvecs[row_num,:]))
			# Divide by that element
			eigvecs[row_num,:] = eigvecs[row_num,:]/eigvecs[row_num,multi]
		end
		# Calculate constants
		consts  = reshape(m.initial,(1,size(m.initial)[1]))*inv(eigvecs)
		new(eigvals,eigvecs,consts)
	end
end

function stationarystate(eq::EquationOfMotion)
	stationary_idxs = findall(x -> abs(x-1) < 0.000001, eq.eigvals)
	result = zeros(size(eq.eigvals))
	for idx in stationary_idxs
		result += eq.constants[idx]*eq.eigvecs[idx,:]
	end
	return result
end

function stateattime(eq::EquationOfMotion, t::Int)
	result = zeros(size(eq.eigvals))
	for idx in 1:length(eq.constants)
		result += eq.constants[idx]*(eq.eigvals[idx]^t)*eq.eigvecs[idx,:]
	end
	return result
end
