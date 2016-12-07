package triangle;

import org.junit.Test;
import static org.junit.Assert.*;

import static triangle.Triangle.Type;
import static triangle.Triangle.Type.*;

/**
 * Test suite that satisfies statement coverage.
 */
public class StatementCoverageTest {

    @Test
    public void bogusTest() {
        Triangle triangle = new Triangle();
    }	
    
    /*
     * Test the classification of an equilateral triangle.
     */
    @Test
    public void testEquilateral() {
        Type actual = Triangle.classify(1, 1, 1);
        Type expected = EQUILATERAL;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidZeros() {
		Type actual = Triangle.classify(0, 0, 0);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidImpossible1() {
		Type actual = Triangle.classify(1, 2, 6);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidImpossible2() {
		Type actual = Triangle.classify(4, 4, 60);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testScalene() {
		Type actual = Triangle.classify(3, 4, 5);
        Type expected = SCALENE;
        assertEquals (expected, actual);
    }

    /*
     * Test the classification of an isosceles triangle.
     */
    @Test
    public void testIsosceles1() {
    	Type actual = Triangle.classify(3, 3, 4);
        Type expected = ISOSCELES;
        assertEquals (expected, actual);
    }
    @Test
    public void testIsosceles2() {
    	Type actual = Triangle.classify(4, 3, 3);
        Type expected = ISOSCELES;
        assertEquals (expected, actual);
    }
    @Test
    public void testIsosceles3() {
    	Type actual = Triangle.classify(3, 4, 3);
        Type expected = ISOSCELES;
        assertEquals (expected, actual);
    }
}
