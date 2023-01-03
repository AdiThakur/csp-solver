from typing import Dict, List, Set

from csp import CSP, Constraint, Domain, Value, Variable


class CSPBuilder():

    def __init__(self) -> None:
        self.variables: Set[Variable] = set()
        self.domains: Domain = {}
        self.assigned_variables: List[Variable] = []
        self.constraints: List[Constraint] = []
        self.variables_to_constraints: Dict[Variable, List[Constraint]] = {}

    def add_variable(self, variable: Variable, domain: List[Value]) -> None:
        if variable in self.variables:
            raise KeyError(f"Variable {variable} already added")

        self.variables.add(variable)
        self.domains[variable] = domain

        if len(domain) == 1:
            self.assigned_variables.append(variable)

    def add_constraint(self, constraint: Constraint) -> None:
        if len(constraint.scope) < 1:
            raise ValueError("Constraints must have at least one variable in scope")
        for variable in constraint.scope:
            if variable not in self.variables:
                raise KeyError("Constraint scope contains unknown variable")

        self.constraints.append(constraint)

        for variable in constraint.scope:
            if variable not in self.variables_to_constraints:
                self.variables_to_constraints[variable] = []
            self.variables_to_constraints[variable].append(constraint)

    def build(self) -> CSP:
        if len(self.variables) == 0:
            raise ValueError("No variables added")
        if len(self.domains) == 0:
            raise ValueError("No domains assigned")
        if len(self.constraints) == 0:
            raise ValueError("No constraints added")

        return CSP(
            variables=list(self.variables),
            domains=self.domains,
            assigned_variables=self.assigned_variables,
            constraints=self.constraints,
            vars_to_cons=self.variables_to_constraints
        )
