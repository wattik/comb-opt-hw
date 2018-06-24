package combopt.problemSolver.initiation;

import combopt.problemSolver.optimization.LocalOptimizer;
import combopt.problemSolver.structures.FlightsRepository;
import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;

import java.util.HashSet;
import java.util.Set;

public class BestFitSearch implements PathInitiator {

    private FlightsRepository flights;
    private int numOfDays;

    public BestFitSearch(FlightsRepository flights, int numOfDays) {
        this.flights = flights;
        this.numOfDays = numOfDays;
    }

    @Override
    public Path initiatePath(String origin) {
        Path path = new Path(Flight.dictionary.encode(origin), numOfDays);

        Set<String> visited = new HashSet<>();
        String currentDestination = origin;

        // d = 0,..,n-1
        for (int day = 0; day < numOfDays; day++) {
            visited.add(currentDestination);
            Flight bestFlight = LocalOptimizer.optimizeFlightsLocally(flights, day, currentDestination, visited);
            path.inject(bestFlight);
            currentDestination = bestFlight.getDestination();
        }

        // d = n
        for (Flight flight : flights.getDayFlights(numOfDays, currentDestination)) {
            if (flight.getDestination().equals(origin)) {
                path.inject(flight);
                break;
            }
        }

        return path;
    }

}
