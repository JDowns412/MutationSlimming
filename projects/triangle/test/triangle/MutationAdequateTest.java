package triangle;

import org.junit.Test;
import static org.junit.Assert.*;

import static triangle.Triangle.Type;
import static triangle.Triangle.Type.*;

/**
 * Test suite that is mutation adequate.
 */
public class MutationAdequateTest {

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

    /**
     * Test invalid triangles
     */
	@Test
    public void testInvalidNegative0() {
		Type actual = Triangle.classify(-1, 1, 1);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

	@Test
    public void testInvalidNegative1() {
		Type actual = Triangle.classify(1, -1, 1);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

	@Test
    public void testInvalidNegative2() {
		Type actual = Triangle.classify(1, 1, -1);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

	@Test
    public void testInvalidNegative3() {
		Type actual = Triangle.classify(-1, -1, 1);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }
	
	@Test
    public void testInvalidZeros0() {
		Type actual = Triangle.classify(0, 1, 1);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }
	
	@Test
    public void testInvalidZeros1() {
		Type actual = Triangle.classify(1, 1, 0);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }
    
    @Test
    public void testInvalidZeros2() {
		Type actual = Triangle.classify(1, 0, 1);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidZeros3() {
		Type actual = Triangle.classify(0, 0, 0);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidZeros4() {
		Type actual = Triangle.classify(1, 0, 0);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidZeros5() {
		Type actual = Triangle.classify(1, 1, 0);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidZeros6() {
		Type actual = Triangle.classify(0, 0, 1);
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
		Type actual = Triangle.classify(6, 1, 2);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidImpossible3() {
		Type actual = Triangle.classify(2, 6, 1);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidImpossible4() {
		Type actual = Triangle.classify(4, 4, 60);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidImpossible5() {
		Type actual = Triangle.classify(4, 60, 4);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testInvalidImpossible6() {
		Type actual = Triangle.classify(60, 4, 4);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    /**
     * Test Scalene Triangles
     */
    @Test
    public void testScalene0() {
		Type actual = Triangle.classify(3, 4, 5);
        Type expected = SCALENE;
        assertEquals (expected, actual);
    }

    @Test
    public void testScalene1() {
		Type actual = Triangle.classify(2, 4, 6);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testScalene2() {
		Type actual = Triangle.classify(6, 4, 2);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testScalene3() {
		Type actual = Triangle.classify(4, 6, 2);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testScalene4() {
		Type actual = Triangle.classify(5, 3, 4);
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

    @Test
    public void testIsosceles4() {
    	Type actual = Triangle.classify(3, 3, 7);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testIsosceles5() {
    	Type actual = Triangle.classify(3, 3, 6);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testIsosceles6() {
    	Type actual = Triangle.classify(3, 6, 3);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testIsosceles7() {
    	Type actual = Triangle.classify(6, 3, 3);
        Type expected = INVALID;
        assertEquals (expected, actual);
    }

    @Test
    public void testIsosceles8() {
    	Type actual = Triangle.classify(3, 4, 4);
        Type expected = ISOSCELES;
        assertEquals (expected, actual);
    }
}
