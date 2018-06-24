package combopt.problemSolver.optimization;

import combopt.problemSolver.entity.Path;
import combopt.problemSolver.initiation.PathInitiator;
import combopt.problemSolver.optimization.perturbation.PathPerturbator;
import combopt.problemSolver.optimization.perturbation.Pertubator;
import combopt.problemSolver.optimization.perturbation.Perturbation;
import combopt.problemSolver.optimization.perturbation.exceptions.OptimizerFinished;
import combopt.problemSolver.optimization.perturbation.exceptions.NoFlightsForCandidate;
import combopt.problemSolver.optimization.perturbation.exceptions.PerturbationNotPossible;

import java.util.Queue;
import java.util.Random;

public class Optimization {

    private final static double ALPHA = 1/6.0;

    private PathInitiator initiator;
    private Queue<PathPerturbator> optimizers;
    private PathPerturbator optimizer;

    public Optimization(PathInitiator initiator, Queue<PathPerturbator> optimizers) {
        this.initiator = initiator;
        this.optimizers = optimizers;
        // get first optimizer
        this.optimizer = optimizers.poll();
    }

    public Path optimize(long stopTime, String origin) {
        long startTime = System.currentTimeMillis();

        Path path = initiator.initiatePath(origin);

        long currentTime = System.currentTimeMillis();
        while (currentTime < stopTime) {
            try {
                Perturbation perturbation = optimizer.proposePerturbation(path);
                boolean admissible = computeAdmissibility(perturbation, currentTime, startTime, stopTime);

                if (admissible) {
                    Pertubator.perturbate(perturbation, path);
//                    System.out.println("Pert cost differ: " + perturbation.getCostDiff());
                }

            } catch (NoFlightsForCandidate ignored) {
            } catch (OptimizerFinished e) {
                this.optimizer = optimizers.poll();
                if (optimizer == null) {
                    break;
                }
            } catch (PerturbationNotPossible e) {
                System.out.println(e);
                break;
            }

            currentTime = System.currentTimeMillis();
        }

        return path;
    }

    private boolean computeAdmissibility(Perturbation perturbation, long t, long tmin, long tmax) {
        Random random = new Random();
        double threshold = random.nextDouble();

        double K = t * (-1) / (tmax - tmin) + tmax / (tmax - tmin) + 0.001;
        double prob = (ALPHA / K) * Math.exp(-perturbation.getCostDiff() * ALPHA / K);
        return prob > threshold;
    }
}
