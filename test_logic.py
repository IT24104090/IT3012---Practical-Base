from logic_engine import KnowledgeBase


def test_forward_chaining():

    kb = KnowledgeBase()

    # =====================================
    # Add Domain Rules
    # =====================================

    kb.tell_rule(
        ['TargetVisible', 'HasDust'],
        'SafeToEngage'
    )

    kb.tell_rule(
        ['SafeToEngage', 'BloodseekerMissing'],
        'Retreat'
    )

    # =====================================
    # Test Case 1
    # Safe Engagement
    # =====================================

    kb.clear_facts()

    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')

    kb.forward_chain()

    assert 'SafeToEngage' in kb.facts, \
        "Test 1 Failed: Should deduce SafeToEngage"

    assert 'Retreat' not in kb.facts, \
        "Test 1 Failed: Should NOT deduce Retreat"

    print("✅ Test Case 1 Passed")

    # =====================================
    # Test Case 2
    # Unsafe Engagement
    # =====================================

    kb.clear_facts()

    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.tell_fact('BloodseekerMissing')

    kb.forward_chain()

    assert 'Retreat' in kb.facts, \
        "Test 2 Failed: Should deduce Retreat to override search"

    print("✅ Test Case 2 Passed")

    # =====================================
    # Success Message
    # =====================================

    print("✅ All Logic Engine Test Cases Passed!")


if __name__ == "__main__":
    test_forward_chaining()