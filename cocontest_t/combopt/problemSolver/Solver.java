package combopt.problemSolver;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;
import combopt.problemSolver.initiation.*;
import combopt.problemSolver.optimization.InstantQueue;
import combopt.problemSolver.optimization.perturbation.candidates.CostAscendingFinder;
import combopt.problemSolver.optimization.perturbation.FourOptInducedEdge;
import combopt.problemSolver.optimization.Optimization;
import combopt.problemSolver.optimization.perturbation.PathPerturbator;
import combopt.problemSolver.structures.CostAscendingRepository;
import combopt.problemSolver.structures.FlightsRepository;

import java.util.List;
import java.util.Queue;

public class Solver {

    private long stopTime;

    public Solver(long startTime, long timeLimit, long epsilon) {
        stopTime = startTime + timeLimit - epsilon;
    }

    public Solution solver(String origin, List<Flight> flightList, int lastFlightDay) {
        // Structures
        final FlightsRepository flights = new FlightsRepository(lastFlightDay, flightList);
        final CostAscendingRepository bestFlights = new CostAscendingRepository(flightList);

        // Optimization tools
        PathInitiator initiator = new BestFitSearch(flights, lastFlightDay);

        Queue<PathPerturbator> optimizers = new InstantQueue() {
            @Override
            public PathPerturbator poll() {
                return new FourOptInducedEdge(new CostAscendingFinder(bestFlights, origin), flights, lastFlightDay);
            }
        };

//        PathPerturbator ascendingCost = new FourOptInducedEdge(new CostAscendingFinder(bestFlights, origin), flights, lastFlightDay);
//        optimizers.add(ascendingCost);
//
//        PathPerturbator expensiveEliminator = new FourOptInducedEdge(new MostExpensiveFlightsEliminator(flights, origin), flights, lastFlightDay);
//        optimizers.add(expensiveEliminator);
//        optimizers.add();
//        optimizers.add(new FourOptInducedEdge(new CostAscendingFinder(bestFlights, origin), flights, lastFlightDay));
//        optimizers.add(new FourOptInducedEdge(new CostAscendingFinder(bestFlights, origin), flights, lastFlightDay));
//        optimizers.add(new FourOptInducedEdge(new CostAscendingFinder(bestFlights, origin), flights, lastFlightDay));
//        optimizers.add(new FourOptInducedEdge(new CostAscendingFinder(bestFlights, origin), flights, lastFlightDay));


        // Actual optimization
        Optimization optimization = new Optimization(initiator, optimizers);
        Path finalPath = optimization.optimize(stopTime, origin);

        return new Solution(finalPath);
    }

}
