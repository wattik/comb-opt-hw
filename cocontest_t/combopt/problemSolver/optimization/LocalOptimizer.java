package combopt.problemSolver.optimization;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.structures.FlightsRepository;

import java.util.Collections;
import java.util.Set;

public class LocalOptimizer {
    public static Flight optimizeFlightsLocally(FlightsRepository flights, int day, String origin, Set<String> visited) {
        return optimizeFlightsLocally(flights, day, origin, visited, Collections.emptySet());
    }

    public static Flight optimizeFlightsLocally(FlightsRepository flights, int day, String origin, Set<String> visited, Set<Flight> tabuList) {
        int minCost = Integer.MAX_VALUE;
        Flight bestFlight = null;
        for (Flight flight : flights.getDayFlights(day, origin)) {
            if (flight.getCost() < minCost && !visited.contains(flight.getDestination()) && !tabuList.contains(flight)) {
                minCost = flight.getCost();
                bestFlight = flight;
            }
        }
        return bestFlight;
    }
}
