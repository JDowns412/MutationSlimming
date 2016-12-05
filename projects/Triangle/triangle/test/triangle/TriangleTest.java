package triangle;

import org.junit.Test;
import static org.junit.Assert.*;

import static triangle.Triangle.Type;
import static triangle.Triangle.Type.*;

/**
 * Test class for the Triangle implementation.
 */
public class TriangleTest {

    /*
     * Test the classification of an equilateral triangle.
     */
    @Test
    public void test1() {
        Type actual = Triangle.classify(1, 1, 1);
        Type expected = EQUILATERAL;
        assertEquals (expected, actual);
    }
}
