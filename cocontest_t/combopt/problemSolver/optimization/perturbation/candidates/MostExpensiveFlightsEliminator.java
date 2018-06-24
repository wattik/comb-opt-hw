package combopt.problemSolver.optimization.perturbation.candidates;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;
import combopt.problemSolver.optimization.LocalOptimizer;
import combopt.problemSolver.optimization.perturbation.exceptions.OptimizerFinished;
import combopt.problemSolver.structures.FlightsRepository;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

public class MostExpensiveFlightsEliminator implements CandidateFinder {

    private FlightsRepository flights;
    private String origin;

    private Set<Flight> formerCandidates;
    private Set<Flight> formerExpensiveFlights;

    public MostExpensiveFlightsEliminator(FlightsRepository flights, String origin) {
        this.flights = flights;
        this.origin = origin;
        this.formerCandidates = new HashSet<>();
        this.formerExpensiveFlights = new HashSet<>();
    }

    @Override
    public Flight findCandidate(Path path) throws OptimizerFinished {
        Flight expensiveFlight = getMostExpensiveFlight(path);
        if (expensiveFlight == null) {
            throw new OptimizerFinished("All flights tried");
        }

        Flight candidate = LocalOptimizer.optimizeFlightsLocally(flights, expensiveFlight.getDay(), expensiveFlight.getOrigin(), Collections.singleton(origin), formerCandidates);
        if (candidate == null) {
            formerExpensiveFlights.add(expensiveFlight);
            return this.findCandidate(path);
        }
        formerCandidates.add(candidate);


        Flight currentFlight = path.getFlight(candidate.getDay());
        if (candidate.getOriginCode() == currentFlight.getOriginCode()
                && candidate != currentFlight
                && !currentFlight.getDestination().equals(origin)
                && !candidate.getDestination().equals(origin)) {
            return candidate;
        } else {
            return findCandidate(path);
        }
    }

    private Flight getMostExpensiveFlight(Path path) {
        int cost = Integer.MIN_VALUE;
        Flight expensiveFlight = null;

        for (Flight flight : path) {
            if (flight.getCost() > cost && ! formerExpensiveFlights.contains(flight)) {
                cost = flight.getCost();
                expensiveFlight = flight;
            }
        }

        return expensiveFlight;
    }
}
