package combopt.problemSolver.structures;

import combopt.problemSolver.entity.Flight;

import java.util.*;

public class CostAscendingRepository implements Iterable<Flight> {
    private Flight[] bestFlights;

    public CostAscendingRepository(List<Flight> flightList) {
        bestFlights = new Flight[flightList.size()];
        bestFlights = flightList.toArray(bestFlights);

        Arrays.sort(bestFlights, Comparator.comparingInt(Flight::getCost));
    }

    @Override
    public Iterator<Flight> iterator() {
        return Arrays.asList(bestFlights).iterator();
    }
}
