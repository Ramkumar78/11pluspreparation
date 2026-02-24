import pytest
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from math_geometry_generators import generate_nets_of_cubes, VALID_NETS, INVALID_NETS, render_net, FILLED, EMPTY

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

    def test_generated_answers_are_valid(self):
        """Verify that the generated answer is indeed one of the VALID_NETS rendered."""
        questions = generate_nets_of_cubes(num_questions=20)
        valid_renderings = {render_net(net) for net in VALID_NETS}

        for q in questions:
            assert q["answer"] in valid_renderings

            # Verify distractors are NOT in valid_renderings
            for opt in q["options"]:
                if opt != q["answer"]:
                    assert opt not in valid_renderings
