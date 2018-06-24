package combopt.problemSolver.optimization;

import combopt.problemSolver.optimization.perturbation.PathPerturbator;

import java.util.Collection;
import java.util.Iterator;
import java.util.Queue;

public abstract class InstantQueue implements Queue<PathPerturbator> {
    @Override
    public int size() {
        return 0;
    }

    @Override
    public boolean isEmpty() {
        return false;
    }

    @Override
    public boolean contains(Object o) {
        return false;
    }

    @Override
    public Iterator<PathPerturbator> iterator() {
        return null;
    }

    @Override
    public Object[] toArray() {
        return new Object[0];
    }

    @Override
    public <T> T[] toArray(T[] a) {
        return null;
    }

    @Override
    public boolean add(PathPerturbator pathPerturbator) {
        return false;
    }

    @Override
    public boolean remove(Object o) {
        return false;
    }

    @Override
    public boolean containsAll(Collection<?> c) {
        return false;
    }

    @Override
    public boolean addAll(Collection<? extends PathPerturbator> c) {
        return false;
    }

    @Override
    public boolean removeAll(Collection<?> c) {
        return false;
    }

    @Override
    public boolean retainAll(Collection<?> c) {
        return false;
    }

    @Override
    public void clear() {

    }

    @Override
    public boolean offer(PathPerturbator pathPerturbator) {
        return false;
    }

    @Override
    public PathPerturbator remove() {
        return null;
    }

    @Override
    public PathPerturbator element() {
        return null;
    }

    @Override
    public PathPerturbator peek() {
        return null;
    }
}
