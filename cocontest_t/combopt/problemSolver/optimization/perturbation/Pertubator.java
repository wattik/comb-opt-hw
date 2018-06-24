package combopt.problemSolver.optimization.perturbation;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;
import combopt.problemSolver.entity.PathManager;

public class Pertubator {

    public static void perturbate(Perturbation perturbation, Path path) {
        boolean wasComplete = path.isComplete();
        if (!wasComplete) {
            throw new RuntimeException("Cycle is corrupted.");
        }

        for (Flight flight : perturbation.getDeletions()) {
            path.removeByDay(flight.getDay());
        }

        for (Flight flight : perturbation.getAdditions()) {
            if (PathManager.isFlightInsertableToPath(path, flight)) {
                path.inject(flight);
            } else {
                throw new RuntimeException(flight + " is not insertable into path.");
            }
        }

        if (wasComplete && !path.isComplete()) {
            throw new RuntimeException("Cycle was corrupted.");
        }
    }

}
