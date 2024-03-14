import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

head = ['Vector space','Vector space','Vector space','Vector space']
relation = ['another name','object','subject','notion']
tail = ['linear space','vector,linear transformation','linear algebra','Matrices']

df = pd.DataFrame({'head': head, 'relation': relation, 'tail': tail})

G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row['head'], row['tail'], label=row['relation'])

pos = nx.spring_layout(G, seed=42, k=0.9)
labels = nx.get_edge_attributes(G, 'label')
plt.figure(figsize=(12, 10))
nx.draw(G, pos, with_labels=True, font_size=10, node_size=700, node_color='lightblue', edge_color='gray', alpha=0.6)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, label_pos=0.3, verticalalignment='baseline')
plt.title('Knowledge Graph')
plt.show()
