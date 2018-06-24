package combopt.problemSolver.entity;

public class PathManager {

    public static int getPreviousDay(int day, int numOfDays) {
        int previousDay = (day - 1) % numOfDays;
        if (previousDay < 0) {
            previousDay = (day + numOfDays - 1) % numOfDays;
        }
        return previousDay;
    }

    public static int getNextDay(int day, int numOfDays) {
        return (day + 1) % numOfDays;
    }

    public static boolean isFlightInsertableToPath(Path path, Flight flight) {
        int day = flight.getDay();

        if (day == path.numOfDays - 1 && flight.getDestinationCode() != path.origin) {
            return false;
        }

        if (day == 0 && flight.getOriginCode() != path.origin) {
            return false;
        }

        if (path.hasLanded[flight.getDestinationCode()]) {
            return false;
        }

        if (path.hasTakenOff[flight.getOriginCode()]) {
            return false;
        }

        boolean isDayOccupied = path.getFlight(day) != null;
        int previousDay = PathManager.getPreviousDay(day, path.numOfDays);
        int nextDay = PathManager.getNextDay(day, path.numOfDays);

        if (isDayOccupied) {
            return false;
        }

        boolean isPreviousDayOccupied = path.getFlight(previousDay) != null;
        if (isPreviousDayOccupied && !path.getFlight(previousDay).getDestination().equals(flight.getOrigin())) {
            return false;
        }

        boolean isNextDayOccupied = path.getFlight(nextDay) != null;
        if (isNextDayOccupied && !path.getFlight(nextDay).getOrigin().equals(flight.getDestination())) {
            return false;
        }

        return true;
    }
}
