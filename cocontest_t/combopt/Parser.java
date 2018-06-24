package combopt;

import java.io.*;
import java.util.HashSet;
import java.util.Set;

public class Parser {

    public static BufferedReader getStdInReader() {
        return new BufferedReader(new InputStreamReader(System.in));
    }

    public static BufferedReader getFileReader(String filename) throws FileNotFoundException {
        return new BufferedReader(new FileReader(filename));
    }

    public static PrintWriter getFileWriter(String filename) throws FileNotFoundException {
        return new PrintWriter(filename);
    }

    public static char[] parseCharsFromLine(BufferedReader reader) throws IOException {
        String s = reader.readLine();
        char[] chars = new char[s.length()];

        for (int i = 0; i < s.length(); i++) {
            chars[i] = s.charAt(i);
        }

        return chars;
    }

    public static String[] parseStringsFromLine(BufferedReader reader) throws IOException {
        return reader.readLine().split(" ");
    }

    public static int[] parseIdsFromLine(BufferedReader reader, int numberOfIntegers) throws IOException {
        int[] integers = new int[numberOfIntegers];
        String[] integersAsString = reader.readLine().split(" ");
        for (int i = 0; i < numberOfIntegers; i++) {
            integers[i] = Integer.parseInt(integersAsString[i]) - 1;
        }
        return integers;
    }

    public static Set<Integer> parseIntegersFromLine(BufferedReader reader) throws IOException {
        String[] integersAsString = reader.readLine().split(" ");
        Set<Integer> integers = new HashSet<>(integersAsString.length + 1, 1);
        for (String anIntegersAsString : integersAsString) {
            integers.add(Integer.parseInt(anIntegersAsString));
        }
        return integers;
    }

    public static int[] parseIntegersFromLine(BufferedReader reader, int numberOfIntegers) throws IOException {
        int[] integers = new int[numberOfIntegers];
        String[] integersAsString = reader.readLine().split(" ");
        for (int i = 0; i < numberOfIntegers; i++) {
            integers[i] = Integer.parseInt(integersAsString[i]);
        }
        return integers;
    }

    public static int parseIntegerFromLine(BufferedReader reader) throws IOException {
        return Parser.parseIntegersFromLine(reader, 1)[0];
    }

    public static long[] parseLongsFromLine(BufferedReader reader, int numberOfIntegers) throws IOException {
        long[] longs = new long[numberOfIntegers];
        String[] integersAsString = reader.readLine().split(" ");
        for (int i = 0; i < numberOfIntegers; i++) {
            longs[i] = Long.parseLong(integersAsString[i]);
        }
        return longs;
    }

    public static String parseStringFromLine(BufferedReader reader) throws IOException {
        return Parser.parseStringsFromLine(reader)[0];
    }
}
