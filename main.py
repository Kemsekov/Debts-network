import networkx as nx
import functools



def decrease_debt(g : nx.DiGraph, node, amount):
    """Decreases in and out debt by amount given, returning amount of debt left"""
    for source in g.predecessors(node):
        can_decrease=min(amount,g[source][node]['debt'])
        g[source][node]['debt'] -= can_decrease
        amount-=can_decrease
    for target in g.successors(node):
        can_decrease=min(amount,g[node][target]['debt'])
        g[node][target]['debt'] -= can_decrease
        amount-=can_decrease
    return amount

def node_in_debt(g : nx.DiGraph,node):
    return sum([g[pred][node]['debt'] for pred in g.predecessors(node)])
def node_out_debt(g : nx.DiGraph,node):
    return sum([g[node][succ]['debt'] for succ in g.successors(node)])

def reduce_debt_of_same_peoples(g : nx.DiGraph):
    edges = g.edges(data=True)
    for e in edges:
        u=e[0]
        v=e[1]
        if not g.has_edge(v,u): continue
        debt=g[u][v]['debt']
        backward_edge_debt = g[v][u]['debt']
        diff = debt-backward_edge_debt
        if diff>=0:
            g[u][v]['debt']-=backward_edge_debt
            g.remove_edge(v,u)

def remove_zero_debt_edges(g : nx.DiGraph):
    to_remove = [(u, v) for u, v, w in g.edges(data=True) if w['debt'] == 0]
    g.remove_edges_from(to_remove)
    isolated_nodes = [node for node, degree in dict(g.degree()).items() if degree == 0]
    g.remove_nodes_from(isolated_nodes)

def graph_sources(g : nx.DiGraph):
    return [node for node in g.nodes() if g.in_degree(node) == 0]
def graph_sinks(g : nx.DiGraph):
    return [node for node in g.nodes() if g.out_degree(node) == 0]

def DAG_max_flow(g : nx.DiGraph) -> tuple[float,dict]:
    sources = graph_sources(g)
    sinks = graph_sinks(g)
    copy = g.copy()
    super_source = "SUPER SOURCE"
    super_sink = "SUPER_SINK"

    for s in sources:
        copy.add_edge(super_source,s,debt=1e10)
    for t in sinks:
        copy.add_edge(t,super_sink,debt=1e10)
    flow_value,flow_dict = nx.maximum_flow(copy,super_source,super_sink,capacity='debt')

    return (flow_value,flow_dict)

g : nx.DiGraph = nx.read_edgelist("debts.edgelist", create_using=nx.DiGraph())
reduce_debt_of_same_peoples(g)
# on this stage we have removed backward edges,so graph is strictly directed

while(True):
    try:
        debt_cycle = nx.find_cycle(g)
    except:
        break
    smallest_flow_edge=min(debt_cycle,key=lambda n:g[n[0]][n[1]]['debt'])
    smallest_flow = g[smallest_flow_edge[0]][smallest_flow_edge[1]]['debt']
    for e in debt_cycle:
        g[e[0]][e[1]]['debt']-=smallest_flow
    remove_zero_debt_edges(g)

    print("-----------------")
    print("These people have cycle debt of "+str(smallest_flow)+" money - they simply forget this much debt")
    print(debt_cycle)
# on this stage we have removed all debt cycles, so out graph is DAG
# now we find max flow from sources to sinks.

# every source now - is is people who will remain with same debt
# every sink - people who need to just receive money.

# we need to remember how much money every source need to give, find max flow
# remove from graph debts computed by max flow - some zero debt edges will appear
# remove zero debt edges.

# repeat same process - once again find sources, remember their debts, and so on.

total_debts = []

while(len(g.edges)!=0):
    sources = graph_sources(g)
    targets = graph_sinks(g)
    # save debts of source nodes
    # print(g.edges(data=True))
    for s in sources:
        for e in g.out_edges(s,data=True):
            e_debt = g[e[0]][e[1]]['debt']
            total_debts.append((e[0],e[1],e_debt))
    flow_value, flow_dict = DAG_max_flow(g)

    for e in g.edges:
        g[e[0]][e[1]]['debt']-=flow_dict[e[0]][e[1]]
    remove_zero_debt_edges(g)
    print("----------------------")
    print(sources)
    print("Gives "+str(flow_value)+" money trough people they debts to")
    print(targets)

print("If you follow these instructions you will pay off debts of all people")

