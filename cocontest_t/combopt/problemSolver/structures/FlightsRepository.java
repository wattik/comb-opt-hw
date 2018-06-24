package combopt.problemSolver.structures;

import combopt.problemSolver.entity.Flight;

import java.util.List;

public class FlightsRepository {
    private AirPortFlights[] flights;

    public FlightsRepository(int lastDay, List<Flight> flightList) {
        this.flights = new AirPortFlights[lastDay + 1];

        for (int i = 0; i <= lastDay; i++) {
            this.flights[i] = new AirPortFlights();
        }

        for (Flight flight : flightList) {
            flights[flight.getDay()].registerFlight(flight.getOrigin(), flight);
            // todo: sort
        }
    }

    public Iterable<Flight> getDayFlights(int day, String from) {
        return flights[day].getFlight(from);
    }

    public Flight getFlight(int day, String from, String to) {
        return flights[day].getFlight(from, to);
    }
}
