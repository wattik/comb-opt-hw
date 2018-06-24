package combopt.problemSolver.optimization.perturbation;

import combopt.problemSolver.entity.Flight;

public class Perturbation {

    private final Flight[] additions;
    private final Flight[] deletions;
    private int costDiff;

    public Perturbation(Flight[] additions, Flight[] deletions) {
        this.additions = additions;
        this.deletions = deletions;

        this.costDiff = 0;

        for (Flight addition : additions) {
            costDiff += addition.getCost();
        }

        for (Flight deletion : deletions) {
            costDiff -= deletion.getCost();
        }
    }

    public Flight[] getAdditions() {
        return additions;
    }

    public Flight[] getDeletions() {
        return deletions;
    }

    public int getCostDiff() {
        return costDiff;
    }
}
