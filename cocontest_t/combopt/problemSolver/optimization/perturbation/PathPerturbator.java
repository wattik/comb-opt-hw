package combopt.problemSolver.optimization.perturbation;

import combopt.problemSolver.entity.Path;
import combopt.problemSolver.optimization.perturbation.exceptions.PerturbationNotPossible;

public interface PathPerturbator {
    public Perturbation proposePerturbation(Path path) throws PerturbationNotPossible;
}
