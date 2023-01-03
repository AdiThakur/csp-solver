from typing import Dict, List, Tuple, Union
from abc import ABC, abstractmethod
import copy


Value = int
Variable = int
Assignment = Dict[Variable, Value]
Domain = Dict[Variable, List[Value]]


class Constraint(ABC):

    scope: List[Variable] = []

    def  __init__(self, scope: List[Variable]) -> None:
        self.scope = scope

    @abstractmethod
    def is_satisfied(self, assignment: Assignment) -> bool:
        pass


class CSP:

    def __init__(
        self,
        variables: List[Variable],
        domains: Domain,
        constraints: List[Constraint],
        vars_to_cons: Dict[Variable, List[Constraint]],
        assigned_variables: List[Variable] = []
        ) -> None:

        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.vars_to_cons = vars_to_cons

        self._init_curr_domains()
        self._init_assigned_vars(assigned_variables)
        self.pruned_domains_at_depth: Dict[int, Domain] = {}
        self.gac_stack: List[Constraint] = []

    def _init_curr_domains(self) -> None:
        self.curr_domains: Domain = {}
        for variable in self.domains:
            self.curr_domains[variable] = [val for val in self.domains[variable]]

    def _init_assigned_vars(self, assigned_variables: List[Variable]) -> None:
        self.assigned: Dict[Variable, bool] = {}
        for var in self.variables:
            self.assigned[var] = var in assigned_variables

    def satisfy(self, depth: int = 0) -> Tuple[bool, Domain]:

        var = self._pick_unassigned_variable()
        if var is None:
            return True, self.curr_domains
        self.assigned[var] = True

        for value in self.domains[var]:

            self.gac_stack = [con for con in self.vars_to_cons[var]]
            self._prune_curr_domain(
                depth, var, copy.copy(self.curr_domains[var]), _except=value
            )

            if self.gac_enforce(depth) == True:
                solved, state = self.satisfy(depth + 1)
                if solved:
                    return True, state
            self._restore_pruned_domains(depth)

        self.assigned[var] = False

        return False, {}

    def _pick_unassigned_variable(self) -> Union[Variable, None]:
        for var in self.assigned:
            if not self.assigned[var]:
                return var
        return None

    def _prune_curr_domain(
        self,
        depth: int,
        variable: Variable,
        values: List[Value],
        _except: Union[Value, None] = None
        ) -> None:

        if depth not in self.pruned_domains_at_depth:
            self.pruned_domains_at_depth[depth] = {}
        if variable not in self.pruned_domains_at_depth[depth]:
            self.pruned_domains_at_depth[depth][variable] = []

        for value in values:
            if value != _except:
                self.curr_domains[variable].remove(value)
                self.pruned_domains_at_depth[depth][variable].append(value)

    def gac_enforce(self, depth) -> bool:

        while len(self.gac_stack) > 0:
            constraint = self.gac_stack.pop()

            for variable in constraint.scope:
                for value in self.curr_domains[variable]:

                    if self._find_support(constraint, { variable: value }, 1):
                        continue

                    self._prune_curr_domain(depth, variable, [value])

                    # Domain wipe-out
                    if len(self.curr_domains[variable]) == 0:
                        self.gac_stack = []
                        return False
                    else:
                        for related_constraint in self.vars_to_cons[variable]:
                            # TODO: Implement a augmented DS for fast lookup
                            if related_constraint not in self.gac_stack:
                                self.gac_stack.append(related_constraint)

        return True

    def _restore_pruned_domains(self, depth: int) -> None:
        for variable in self.pruned_domains_at_depth[depth]:
            self.curr_domains[variable].extend(
                self.pruned_domains_at_depth[depth][variable]
            )
        self.pruned_domains_at_depth.pop(depth)

    def _find_support(
        self,
        constraint: Constraint,
        support: Assignment,
        vars_assigned: int
        ) -> bool:

        if vars_assigned == len(constraint.scope):
            return constraint.is_satisfied(support)

        for variable in constraint.scope:

            if variable in support:
                continue

            for value in self.curr_domains[variable]:
                support[variable] = value
                is_satisfied = self._find_support(
                    constraint, support, vars_assigned + 1
                )
                if is_satisfied:
                    return True

            break

        return False
