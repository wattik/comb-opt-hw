package combopt.problemSolver.completion;

import combopt.problemSolver.entity.Path;
import combopt.problemSolver.structures.CostAscendingRepository;
import combopt.problemSolver.structures.FlightsRepository;

public class LeastChangesCompletion implements PathCompletion {

    private final CostAscendingRepository bestFlights;
    private final FlightsRepository flights;
    private final int numOfDays;

    public LeastChangesCompletion(CostAscendingRepository bestFlights, FlightsRepository flights, int lastFlightDay) {
        this.bestFlights = bestFlights;
        this.flights = flights;
        this.numOfDays = lastFlightDay;
    }

    @Override
    public Path complete(Path path) {
//        if (path.isComplete())        return path;
//
//        for (int day = 0; day < numOfDays; day++) {
//            if (path.getDayFlights(day) != null) continue;
//
//            String currentPort = path.getMorningDestination(day);
//            // todo: ^^ can be null!
//
//            Flight bestFlight = null;
//            for (Flight flight : flights.getDayFlights(day, currentPort)) {
//                if (path.wouldBeForward(flight))
//            }

//        }
        return null;
    }
}
