import pytest
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from math_geometry_generators import generate_nets_of_cubes, generate_opposite_face_questions, VALID_NETS, INVALID_NETS, render_net, FILLED, EMPTY

class TestMathGeometryGenerators:
    def test_generate_nets_of_cubes_structure(self):
        """Test that the generator returns correctly structured questions."""
        questions = generate_nets_of_cubes(num_questions=5)
        assert len(questions) == 5

        for q in questions:
            assert "text" in q
            assert "answer" in q
            assert "options" in q
            assert "explanation" in q
            assert len(q["options"]) == 4
            assert q["answer"] in q["options"]

            # Check options uniqueness
            assert len(set(q["options"])) == 4

    def test_valid_nets_integrity(self):
        """Test that the valid nets list contains 11 items and they are matrices."""
        assert len(VALID_NETS) == 11
        for net in VALID_NETS:
            assert isinstance(net, list)
            assert len(net) > 0
            assert isinstance(net[0], list)

    def test_render_net(self):
        """Test the rendering helper."""
        matrix = [[1, 0], [0, 1]]
        expected = f"{FILLED}{EMPTY}\n{EMPTY}{FILLED}"
        assert render_net(matrix) == expected

        # Test padding behavior (jagged rows)
        matrix_jagged = [[1], [1, 1]]
        # The function finds max width (2)
        # Row 0: [1] -> index 0=1, index 1=0 (default)
        # Row 1: [1,1] -> index 0=1, index 1=1
        expected_jagged = f"{FILLED}{EMPTY}\n{FILLED}{FILLED}"
        assert render_net(matrix_jagged) == expected_jagged

    def test_render_net_with_strings(self):
        """Test the rendering helper with string labels."""
        matrix = [["1", "2"], ["3", "4"]]
        expected = "12\n34"
        assert render_net(matrix) == expected

        # Mixed types
        matrix_mixed = [["1", 0], [1, "4"]]
        expected_mixed = f"1{EMPTY}\n{FILLED}4"
        assert render_net(matrix_mixed) == expected_mixed

    def test_generate_opposite_face_questions(self):
        """Test the opposite face question generator."""
        questions = generate_opposite_face_questions(num_questions=5)
        assert len(questions) == 5
        for q in questions:
             assert "text" in q
             assert "answer" in q
             assert "options" in q
             assert "explanation" in q
             assert "OPPOSITE" in q["text"]
             assert q["answer"] in q["options"]
             assert len(q["options"]) == 4
             # Answer should be a string digit
             assert q["answer"].isdigit()

    def test_generated_answers_are_valid(self):
        """Verify that the generated answer is valid for the question type."""
        questions = generate_nets_of_cubes(num_questions=20)
        # valid_renderings check removed as nets are now randomly transformed (rotated/flipped)

        for q in questions:
            if "OPPOSITE" in q["text"]:
                # For opposite face questions, answer should be a digit string
                assert q["answer"].isdigit()
            else:
                # For valid net questions, answer should be a string representation of a net
                assert isinstance(q["answer"], str)
                assert FILLED in q["answer"]
                assert EMPTY in q["answer"]

                # Verify distractors are unique
                assert len(set(q["options"])) == 4
                assert q["answer"] in q["options"]
