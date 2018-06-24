package combopt.problemSolver.initiation;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;
import combopt.problemSolver.entity.PathManager;
import combopt.problemSolver.optimization.LocalOptimizer;
import combopt.problemSolver.structures.CostAscendingRepository;
import combopt.problemSolver.structures.FlightsRepository;

import java.util.HashSet;

public class GreedySearch implements PathInitiator {

    private final CostAscendingRepository bestFlights;
    private final FlightsRepository flights;
    private final int numOfDays;

    public GreedySearch(CostAscendingRepository bestFlights, FlightsRepository flights, int lastFlightDay) {
        this.bestFlights = bestFlights;
        this.flights = flights;
        this.numOfDays = lastFlightDay;
    }

    @Override
    public Path initiatePath(String origin) {
        Path path = new Path(Flight.dictionary.encode(origin), numOfDays);

        Flight firstFlight = LocalOptimizer.optimizeFlightsLocally(flights, 0, origin, new HashSet<>());
        path.inject(firstFlight);

        for (Flight flight : bestFlights) {
            System.out.println(flight);

            if (PathManager.isFlightInsertableToPath(path, flight)) {
                path.inject(flight);
            } else {
                System.out.println("Piča");
            }

            if (path.isComplete()){
                return path;
            }
        }

        return path;
    }
}
