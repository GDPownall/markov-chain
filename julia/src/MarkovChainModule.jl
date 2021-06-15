module MarkovChainModule

export
	ProbMatrix,
	MarkovChain,
	EquationOfMotion,
	stationarystate,
	stateattime

include("ProbMatrix.jl")
include("MarkovChain.jl")

end
