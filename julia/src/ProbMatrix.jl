# This file contains the struct for the probability matrix

using LinearAlgebra

struct ProbMatrix{T<:Real} <: AbstractArray{T,2}
        data

        function ProbMatrix{T}(data::AbstractArray{T,2}) where T<:Real
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
                new{T}(data)
        end
end

# Outer constructors

ProbMatrix(data::Array{T,2}) where {T} = ProbMatrix{T}(data)

# Define functions

Base.size(m::ProbMatrix{T}) where T = size(m.data)
LinearAlgebra.factorize(m::ProbMatrix{T}) where T = factorize(m.data)
