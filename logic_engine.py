# logic_engine.py

class KnowledgeBase:
    """
    Knowledge Base for storing facts and rules,
    and performing Forward Chaining inference.
    """

    def __init__(self):
        # Store unique facts
        self.facts = set()

        # Store rules as:
        # ( [premises], conclusion )
        self.rules = []

    def tell_fact(self, fact_string):
        """
        Add a fact to the knowledge base.
        """
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        """
        Add a Horn Clause rule.
        Example:
        ["TargetVisible", "HasAmmo"] -> "CanAttack"
        """
        self.rules.append(
            (premise_list, conclusion_string)
        )

    def clear_facts(self):
        """
        Remove all current facts.
        """
        self.facts.clear()

    def forward_chain(self):
        """
        Forward Chaining Inference Engine

        Repeatedly applies rules until
        no new facts can be inferred.
        """

        new_facts_added = True

        while new_facts_added:

            new_facts_added = False

            for premises, conclusion in self.rules:

                # Skip if already known
                if conclusion not in self.facts:

                    # Check whether ALL premises exist
                    if all(
                        premise in self.facts
                        for premise in premises
                    ):

                        self.facts.add(conclusion)

                        new_facts_added = True

    def show_facts(self):
        """
        Display all facts.
        """
        print("\nFacts:")
        for fact in sorted(self.facts):
            print("-", fact)

    def show_rules(self):
        """
        Display all rules.
        """
        print("\nRules:")
        for premises, conclusion in self.rules:
            print(
                f"{premises} -> {conclusion}"
            )


# ==================================================
# Testing
# ==================================================

if __name__ == "__main__":

    kb = KnowledgeBase()

    # ------------------------------------------------
    # Initial Facts
    # ------------------------------------------------

    kb.tell_fact("TargetVisible")
    kb.tell_fact("HasAmmo")

    # ------------------------------------------------
    # Rules
    # ------------------------------------------------

    kb.tell_rule(
        ["TargetVisible", "HasAmmo"],
        "CanAttack"
    )

    kb.tell_rule(
        ["CanAttack"],
        "Shoot"
    )

    kb.tell_rule(
        ["Shoot"],
        "EnemyHit"
    )

    # ------------------------------------------------
    # Before Inference
    # ------------------------------------------------

    print("BEFORE FORWARD CHAINING")
    kb.show_facts()

    # ------------------------------------------------
    # Run Inference
    # ------------------------------------------------

    kb.forward_chain()

    # ------------------------------------------------
    # After Inference
    # ------------------------------------------------

    print("\nAFTER FORWARD CHAINING")
    kb.show_facts()

    kb.show_rules()