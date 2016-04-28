% A-Star Best-First Search. A simplified version of Bratko Fig. 12.3.
% Store paths and costs in a list of pairs [Path, Cost],
% ordered according to f(n) where f(n) = g(n) + h(n)
% with g(n) the path cost and h(n) the heuristic cost from n to a goal
% Nodes in a path are listed in reverse order,
% i.e. list [t,g,f,e,s] represents path s->e->f->g->t
% To search from the a node Start for a solution path SolPath,
% call ?- solve(Start, SolPath, N)

solve(Start, SolPath, N) :-
    astar([[[Start], 0]], SolPath, 1, N).

astar([BestPath|_Paths], Path, N, N) :-
    BestPath = [Path, _Cost],
    Path = [LastNode|_],
    goal(LastNode).

astar([BestPath|Paths], SolPath, L, N) :-
    BestPath = [Path, Cost],
    extend(Path, Cost, Paths, NewPaths),
    M is L + 1,
    astar(NewPaths, SolPath, M, N).

% extend best path by successors of last node

extend(Path, Cost, Paths, NewPaths) :-
    Path = [LastNode|_],
    findall(S, (s(LastNode, S, _), not(member(S, Path))), Succs),
    not(Succs = []),
    extend_path(Succs, Path, Cost, Paths, NewPaths).

% extend path by each node in Succs and insert into Paths in order of costs

extend_path([], _, _, Paths, Paths).        % no more paths

extend_path([S|Succs], Path, Cost, Paths, Paths2) :-
    Path = [LastNode|_],
    s(LastNode, S, C),
    NewCost is Cost + C,            % g(S) = NewCost
    h(S, H),                        % h(S) = estimate S->goal
    NewEst is NewCost + H,          % f(S) = estimate of node's value
    insert([S|Path], NewCost, NewEst, Paths, Paths1),
    extend_path(Succs, Path, Cost, Paths1, Paths2).

% insert path in order in the list of paths

insert(Path, Cost, _Estimate, [], [[Path, Cost]]).

insert(Path, Cost, Estimate, Paths, [[Path, Cost]|Paths]) :-
    Paths = [Path1|_],
    Path1 = [[Last1|_], Cost1],
    h(Last1, H),
    Estimate1 is Cost1 + H,
    Estimate1 > Estimate.              % new path is better

insert(Path, Cost, Estimate, [Path1|Paths], [Path1|Paths1]) :-
    insert(Path, Cost, Estimate, Paths, Paths1).
