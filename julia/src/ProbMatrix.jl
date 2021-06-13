# This file contains the struct for the probability matrix

module ProbMatrixDef

export ProbMatrix

struct ProbMatrix
    data::AbstractArray

    function ProbMatrix(data) 
	if ndims(data) != 2
		error("Probability matrix needs to be two-dimensional")
	end
	if size(data,1) != size(data,2)
		error("Probability matrix needs to be square.")
	end
	for col_num in 1:size(data,1)
		if sum(data[:,col_num]) != 1
			error("Each column of a probability matrix must sum to one.")
		end
	end
        new(data)
    end
end
"""
function ProbMatrix(A::AbstractMatrix)
    LinearAlgebra.checksquare(A)
    return symmetric_type(typeof(A))(A, char_uplo(uplo))
end
"""
Mat = [0.8 0.05 ; 0.2 0.95]

A = ProbMatrix(Mat)

end
