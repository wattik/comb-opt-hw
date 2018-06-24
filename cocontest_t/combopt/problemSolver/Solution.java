package combopt.problemSolver;

import combopt.problemSolver.entity.Flight;
import combopt.problemSolver.entity.Path;

import java.util.LinkedList;
import java.util.List;

public class Solution {

    private int cost;
    private List<String> cities;

    public Solution(Path path) {
        if (! path.isComplete()) {
            throw new RuntimeException("Path/cycle not complete.");
        }
        cities = new LinkedList<>();
        cost = 0;

        for (Flight flight : path) {
            cost += flight.getCost();
            cities.add(flight.getOrigin());
        }
    }

    public int getCost() {
        return cost;
    }

    public String getPath() {
        return String.join(" ", cities);
    }
}
