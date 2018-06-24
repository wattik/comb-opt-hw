package combopt.problemSolver.optimization.perturbation.candidates;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;
import combopt.problemSolver.optimization.perturbation.exceptions.OptimizerFinished;
import combopt.problemSolver.structures.CostAscendingRepository;

import java.util.Iterator;

public class CostAscendingFinder implements CandidateFinder {

    private Iterator<Flight> costAscendingIterator;
    private String origin;

    public CostAscendingFinder(CostAscendingRepository costAscendingRepository, String origin) {
        this.costAscendingIterator = costAscendingRepository.iterator();
        this.origin = origin;
    }

    @Override
    public Flight findCandidate(Path path) throws OptimizerFinished {
        while (costAscendingIterator.hasNext()) {
            Flight candidate = costAscendingIterator.next();
            Flight currentFlight = path.getFlight(candidate.getDay());

            if (
                    (currentFlight == null) || (
                            candidate.getOriginCode() == currentFlight.getOriginCode()
                                    && candidate != currentFlight
                                    && !currentFlight.getDestination().equals(origin)
                    )
                            && !candidate.getDestination().equals(origin)) {
                return candidate;
            }

        }

        throw new OptimizerFinished("No more candidate flights.");
    }
}
