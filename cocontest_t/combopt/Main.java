package combopt;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.Solution;
import combopt.problemSolver.Solver;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.LinkedList;
import java.util.List;

public class Main {
    public final static long EPSILON = 200;

    public static void main(String[] args) throws IOException {
        final long startTime = System.currentTimeMillis();

        String inputFileName = args[0];
        String outputFileName = args[1];
        final long timeLimit = Long.parseLong(args[2]) * 1000; // to make it millis

        BufferedReader reader = Parser.getFileReader(inputFileName);
        String origin = Parser.parseStringFromLine(reader);

        List<Flight> flights = new LinkedList<>();

        int lastFightDay = 0;
        while (true) {
            try {
                final String[] flight = Parser.parseStringsFromLine(reader);
                flights.add(Flight.getInstance(flight));
                lastFightDay = Math.max(lastFightDay, Integer.parseInt(flight[2]));
            } catch (NullPointerException e) {
                break;
            }
        }

        Solver solver = new Solver(startTime, timeLimit, Main.EPSILON);
        Solution solution = solver.solver(origin, flights, lastFightDay);

        PrintWriter writer = Parser.getFileWriter(outputFileName);
        writer.println(solution.getCost());
        writer.println(solution.getPath());
        writer.close();

        System.out.println("Cost: " + solution.getCost());
        System.out.println("Timelimit: " + timeLimit);
        System.out.println("Remaining: " + ((startTime + timeLimit) - System.currentTimeMillis()));
    }
}
