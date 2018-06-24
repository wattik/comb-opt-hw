package combopt.problemSolver.optimization.perturbation.candidates;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;
import combopt.problemSolver.optimization.perturbation.exceptions.OptimizerFinished;

public interface CandidateFinder {

    public Flight findCandidate(Path path) throws OptimizerFinished;

}
