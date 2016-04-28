% Bratko Figure 11.10. An implementation of breadth-first search.

% solve(Start, Solution)
% Solution is a path (in reverse order) from Start to a goal state

solve(Start, Solution, N)  :-
   breadthfirst([[Start]], Solution, 1, N).

% breadthfirst([Path1, Path2, ...], Solution, L, N)
% Store the paths (in reverse order) in a queue ordered by path length
% Extend the path at the head of the queue by adding the
% successors of its head node.
% Add newly created paths to the end of the queue

breadthfirst([[Node|Path]|_], [Node|Path], N, N)  :-
   goal(Node).

breadthfirst([Path | Paths], Solution, L, N)  :-
   extend(Path, NewPaths),
   M is L + 1,
   append(Paths, NewPaths, Paths1),
   breadthfirst(Paths1, Solution, M, N).

extend([Node|Path], NewPaths)  :-
   findall([NewNode, Node|Path], (s(Node, NewNode, _)
   , not(member(NewNode, [Node|Path])) % exclude repeated states
   ), NewPaths).
