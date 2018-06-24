package combopt.problemSolver.entity;

import java.util.*;

public class StringEncoder {
    private Map<String, Integer> encoder;
    private List<String> decoder;
    private int nextVacantCodeName;

    public StringEncoder() {
        encoder = new HashMap<>();
        decoder = new ArrayList<>();
        nextVacantCodeName = 0;
    }

    public int encode(String name) {
        Integer code = encoder.putIfAbsent(name, nextVacantCodeName);
        if (code == null) {
            code = nextVacantCodeName++;
            decoder.add(name);
        }
        return code;
    }

    public String decode(int code) {
        return decoder.get(code);
    }

}
