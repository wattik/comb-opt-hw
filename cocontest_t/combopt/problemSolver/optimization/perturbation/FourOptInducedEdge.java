package combopt.problemSolver.optimization.perturbation;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;
import combopt.problemSolver.entity.PathManager;
import combopt.problemSolver.optimization.perturbation.candidates.CandidateFinder;
import combopt.problemSolver.optimization.perturbation.exceptions.NoFlightsForCandidate;
import combopt.problemSolver.optimization.perturbation.exceptions.PerturbationNotPossible;
import combopt.problemSolver.structures.FlightsRepository;

public class FourOptInducedEdge implements PathPerturbator {

    private CandidateFinder candidateFinder;
    private FlightsRepository flights;
    private int numOfDays;

    public FourOptInducedEdge(CandidateFinder candidateFinder, FlightsRepository flights, int lastFlightDay) {
        this.candidateFinder = candidateFinder;
        this.flights = flights;
        this.numOfDays = lastFlightDay + 1;
    }

    @Override
    public Perturbation proposePerturbation(Path path) throws PerturbationNotPossible {
        Flight candidate = candidateFinder.findCandidate(path);
        return this.induceByCandidate(candidate, path);
    }

    private Perturbation induceByCandidate(Flight candidate, Path path) throws NoFlightsForCandidate {
        Flight[] additions;
        Flight[] deletions;

        int day0 = candidate.getDay();
        int day1 = PathManager.getNextDay(day0, numOfDays);
        int dayT = PathManager.getNextDay(path.getDayByDestination(candidate.getDestinationCode()), numOfDays);
        int dayTmin1 = PathManager.getPreviousDay(dayT, numOfDays);

        // general case
        int dayDifference = (numOfDays + dayT - candidate.getDay()) % numOfDays;
        if (dayDifference > 2) {

            Flight flight0 = path.getFlight(day0);
            Flight flight1 = path.getFlight(day1);
            Flight flightTmin1 = path.getFlight(dayTmin1);
            Flight flightT = path.getFlight(dayT);
            deletions = new Flight[]{flight0, flight1, flightTmin1, flightT};

            Flight newFlight1 = flights.getFlight(day1, candidate.getDestination(), flight1.getDestination());
            if (newFlight1 == null) throw new NoFlightsForCandidate("New Flight 1 not existing.");

            Flight newFlightTmin1 = flights.getFlight(dayTmin1, flightTmin1.getOrigin(), flight0.getDestination());
            if (newFlightTmin1 == null) throw new NoFlightsForCandidate("New Flight T-1 not existing.");

            Flight newFlightT = flights.getFlight(dayT, flight0.getDestination(), flightT.getDestination());
            if (newFlightT == null) throw new NoFlightsForCandidate("New Flight T not existing.");

            additions = new Flight[]{candidate, newFlight1, newFlightTmin1, newFlightT};

            return new Perturbation(additions, deletions);

        } else if (dayDifference == 2) {

            Flight flight0 = path.getFlight(day0);
            Flight flightTmin1 = path.getFlight(dayTmin1);
            Flight flightT = path.getFlight(dayT);
            deletions = new Flight[]{flight0, flightTmin1, flightT};

            Flight newFlightTmin1 = flights.getFlight(dayTmin1, candidate.getDestination(), flight0.getDestination());
            if (newFlightTmin1 == null)
                throw new NoFlightsForCandidate("New Flight T-1 not existing (special case dayDiff = 2).");

            Flight newFlightT = flights.getFlight(dayT, flight0.getDestination(), flightT.getDestination());
            if (newFlightT == null)
                throw new NoFlightsForCandidate("New Flight T not existing (special case dayDiff = 2).");

            additions = new Flight[]{candidate, newFlightTmin1, newFlightT};

            return new Perturbation(additions, deletions);
        }

        throw new RuntimeException("Perturbing no feasible. Day difference=" + dayDifference);
    }

//    private Flight getFlightTmin1(int dayTmin1, Flight flightTmin1, Flight flight0) throws NoFlightsForCandidate {
//        Flight newFlightTmin1;
//
//        if (flight0 == null) {
//            if (flightTmin1 == null) {
//
//            } else {
//                newFlightTmin1 =
//            }
//        } else {
//            if (flightTmin1 == null) {
//
//            } else {
//                newFlightTmin1 = flights.getFlight(dayTmin1, flightTmin1.getOrigin(), flight0.getDestination());
//            }
//        }
//        if (newFlightTmin1 == null) throw new NoFlightsForCandidate("New Flight T-1 not existing.");
//        return newFlightTmin1
//    }

}
