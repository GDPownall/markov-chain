module MarkovChainModule

export
	ProbMatrix,
	MarkovChain,
	EquationOfMotion,
	stationarystate

include("ProbMatrix.jl")
include("MarkovChain.jl")

end
