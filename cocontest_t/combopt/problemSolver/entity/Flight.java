package combopt.problemSolver.entity;

public class Flight {

    public static final StringEncoder dictionary = new StringEncoder();

    private final int toCode;
    private final int fromCode;

    private int day;
    private String from;
    private String to;
    private int cost;

    public Flight(int day, String from, String to, int cost) {
        this.day = day;
        this.from = from;
        this.to = to;
        this.cost = cost;

        this.toCode = dictionary.encode(to);
        this.fromCode = dictionary.encode(from);
    }

    public static Flight getInstance(String[] flight) {
        String from = flight[0];
        String to = flight[1];
        int day = Integer.parseInt(flight[2]);
        int cost = Integer.parseInt(flight[3]);

        return new Flight(day, from, to, cost);
    }

    public int getCost() {
        return cost;
    }

    public String getDestination() {
        return to;
    }

    public int getDestinationCode() {
        return toCode;
    }

    public String getOrigin() {
        return from;
    }

    public int getOriginCode() {
        return fromCode;
    }

    @Override
    public String toString() {
        return day + " " + from +
                " " + to +
                " " + cost;
    }

    public int getDay() {
        return day;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(day) + Integer.hashCode(this.toCode) + Integer.hashCode(this.fromCode);
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Flight && ((Flight) obj).cost == this.cost && ((Flight) obj).fromCode == this.fromCode && ((Flight) obj).toCode == this.toCode;
    }
}
