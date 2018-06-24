package combopt.problemSolver.entity;

import java.util.Arrays;
import java.util.Iterator;

public class Path implements Iterable<Flight> {
    private final static int NOT_LANDED_YET = -1;

    int origin;
    final Flight[] path;

    final boolean[] hasTakenOff;
    final boolean[] hasLanded;
    final int[] dayOfLandingAtPort;

    final int numOfDays;
    private int numOfInjections = 0;

    public Path(int origin, int lastFlightDay) {
        this.origin = origin;
        this.numOfDays = lastFlightDay + 1;
        this.path = new Flight[numOfDays];
        this.hasTakenOff = new boolean[numOfDays];
        this.hasLanded = new boolean[numOfDays];
        this.dayOfLandingAtPort = new int[numOfDays];
        Arrays.fill(dayOfLandingAtPort, NOT_LANDED_YET);

        // origin set-up
        dayOfLandingAtPort[origin] = numOfDays - 1;
    }

    @Override
    public Iterator<Flight> iterator() {
        return Arrays.asList(path).iterator();
    }

    public void inject(Flight flight) {
        removeByDay(flight.getDay());
        numOfInjections++;

        path[flight.getDay()] = flight;
        dayOfLandingAtPort[flight.getDestinationCode()] = flight.getDay();
        hasLanded[flight.getDestinationCode()] = true;
        hasTakenOff[flight.getOriginCode()] = true;

    }

    public void removeByDay(int day) {
        Flight flight = path[day];
        if (flight != null) {
            numOfInjections--;
            path[flight.getDay()] = null;
            hasLanded[flight.getDestinationCode()] = false;
            hasTakenOff[flight.getOriginCode()] = false;
            dayOfLandingAtPort[flight.getDestinationCode()] = NOT_LANDED_YET;
        }
    }

    public Flight getFlight(int day) {
        return path[day];
    }

    public boolean isComplete() {
        return numOfInjections == numOfDays;
    }

    public int getDayByDestination(int destinationCode) {
        return dayOfLandingAtPort[destinationCode];
    }
}
