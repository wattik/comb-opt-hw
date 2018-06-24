package combopt.problemSolver.structures;

import combopt.problemSolver.entity.Flight;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class AirPortFlights {

    private Map<String, List<Flight>> originFlights;
    private Map<String, Flight> flights;

    public AirPortFlights() {
        this.originFlights = new HashMap<>();
        this.flights = new HashMap<>();
    }

    public void registerFlight(String from, Flight flight) {
        if (! originFlights.containsKey(from)) {
            originFlights.put(from, new LinkedList<>());
        }

        originFlights.get(from).add(flight);
        flights.put(from + flight.getDestination(), flight);
    }

    public List<Flight> getFlight(String from) {
        return originFlights.get(from);
    }

    public Flight getFlight(String from, String to) {
        return flights.get(from + to);
    }
}
