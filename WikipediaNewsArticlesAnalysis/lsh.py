#%%
import random
from datasketch import MinHash, MinHashLSH
from sklearn.feature_extraction.text import CountVectorizer
#%%
articles = [] 
#%%
from summarization import Summarizer
from page_news import PageNews
import json
page_name = "Maharashtra Elections"
summarizer = Summarizer(False)
page_news_obj = PageNews(summarizer, page_name)
json_pages = page_news_obj.fetch_news_article(200)

json_pages_parsed = json.loads(json_pages)
for json_page in json_pages_parsed:
    articles.append(json_page["title"] + json_page["content"])
#%%
len(articles)
# shuffle articles
random.shuffle(articles)
#%%
org_articles = articles
len(org_articles)
#%%
# Parameters for LSH
shingle_size = 5  # Number of words in each shingle
num_perm = 128  # Number of permutations for MinHash
threshold = 0.2  # Similarity threshold for LSH
#%%
def get_shingles(text, shingle_size):
    words = text.split()
    return set([' '.join(words[i:i + shingle_size]) for i in range(len(words) - shingle_size + 1)])
#%%
# Initialize MinHashLSH
lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

# Store original article and its MinHash
minhash_objects = []
#%%


# Process each article
for idx, article in enumerate(articles):
    # Create shingles
    shingles = get_shingles(article, shingle_size)

    # Create MinHash
    m = MinHash(num_perm=num_perm)
    for shingle in shingles:
        m.update(shingle.encode('utf8'))

    # Store MinHash object
    minhash_objects.append((article, m))

    # Add to LSH
    if f"article_{idx}" not in lsh.keys:
        lsh.insert(idx, m)
    else:
        print(f"Key article_{idx} already exists. Skipping insertion.")


#%%
buckets = {}
unique_buckets = []
for idx, (article, m) in enumerate(minhash_objects):
    similar_ids = lsh.query(m)
    print(f"Similar articles to article {idx} are in bucket(s): {similar_ids}")
    
    unique_buckets.append(set(similar_ids)) if set(similar_ids) not in unique_buckets else None
    
    # Find the first existing bucket for this article, if any
    assigned_bucket = None
    for bucket_id in similar_ids:
        if bucket_id in buckets:
            assigned_bucket = bucket_id
            break

    if assigned_bucket:
        # Add the article to the existing bucket
        buckets[assigned_bucket].append(article)
    else:
        # Create a new bucket with this article as the head
        new_bucket_id = f"bucket_{len(buckets)}"
        buckets[new_bucket_id] = [article]

# Output the results
# for bucket_id, articles in buckets.items():
#     print(f"Bucket ID: {bucket_id}, Head Article: {articles[0]}, All Articles: {articles}")
#%%
unique_buckets
#%%
# Create a graph
G = nx.Graph()

# Add nodes and edges
for group in unique_buckets[:60]:
    group_list = list(group)
    for article in group_list:
        G.add_node(article)
    for i in range(len(group_list)):
        for j in range(i + 1, len(group_list)):
            G.add_edge(group_list[i], group_list[j])

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Layout for better visualization
nx.draw(
    G, pos, with_labels=True, node_size=500, node_color="lightblue",
    font_size=8, font_color="black", edge_color="gray"
)
plt.title("Connected Graph of Articles", fontsize=16)
plt.show()

#%%

#%%
import networkx as nx
import matplotlib.pyplot as plt
import random

# Create a graph
G = nx.Graph()

# Add nodes and edges
for group in unique_buckets[:60]:
    group_list = list(group)
    color = f"#{random.randint(0, 0xFFFFFF):06x}"  # Random color for the group
    for article in group_list:
        G.add_node(article, group_color=color)  # Add group color as node attribute
    for i in range(len(group_list)):
        for j in range(i + 1, len(group_list)):
            G.add_edge(group_list[i], group_list[j])

# Visualizing with enhancements
plt.figure(figsize=(6, 4))

# Extract node colors from attributes
node_colors = [data['group_color'] for _, data in G.nodes(data=True)]

# Position the nodes using spring layout
pos = nx.spring_layout(G, seed=42)

# Draw the nodes with custom colors and sizes
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600, alpha=0.9)

# Draw the edges with transparency and weight
nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.6, width=1.5)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

# Title and aesthetics
plt.title("Connected Graph of Articles with Threshold = 0.8", fontsize=16, fontweight="bold")
plt.axis("off")
plt.show()

#%%
import networkx as nx
import matplotlib.pyplot as plt
import random

# Create a graph
G = nx.Graph()

# Add nodes and edges
for group in unique_buckets[:60]:
    group_list = list(group)
    color = f"#{random.randint(0, 0xFFFFFF):06x}"  # Random color for the group
    for article in group_list:
        G.add_node(article, group_color=color)  # Add group color as node attribute
    for i in range(len(group_list)):
        for j in range(i + 1, len(group_list)):
            G.add_edge(group_list[i], group_list[j])

# Visualizing with enhancements
plt.figure(figsize=(6, 4))

# Extract node colors from attributes
node_colors = [data['group_color'] for _, data in G.nodes(data=True)]

# Position the nodes using spring layout
pos = nx.spring_layout(G, seed=42)

# Draw the nodes with custom colors and sizes
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600, alpha=0.9)

# Draw the edges with transparency and weight
nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.6, width=1.5)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

# Title and aesthetics
plt.title("Connected Graph of Articles with Threshold = 0.5", fontsize=16, fontweight="bold")
plt.axis("off")
plt.show()

#%%
import networkx as nx
import matplotlib.pyplot as plt
import random

# Create a graph
G = nx.Graph()

# Add nodes and edges
for group in unique_buckets[:60]:
    group_list = list(group)
    color = f"#{random.randint(0, 0xFFFFFF):06x}"  # Random color for the group
    for article in group_list:
        G.add_node(article, group_color=color)  # Add group color as node attribute
    for i in range(len(group_list)):
        for j in range(i + 1, len(group_list)):
            G.add_edge(group_list[i], group_list[j])

# Visualizing with enhancements
plt.figure(figsize=(6, 4))

# Extract node colors from attributes
node_colors = [data['group_color'] for _, data in G.nodes(data=True)]

# Position the nodes using spring layout
pos = nx.spring_layout(G, seed=42)

# Draw the nodes with custom colors and sizes
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600, alpha=0.9)

# Draw the edges with transparency and weight
nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.6, width=1.5)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

# Title and aesthetics
plt.title("Connected Graph of Articles with Threshold = 0.2", fontsize=16, fontweight="bold")
plt.axis("off")
plt.show()

#%%
import networkx as nx
import matplotlib.pyplot as plt
from datasketch import MinHash

# Function to compute Jaccard similarity
def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def cosine_similarity(set1, set2):
    dot_product = sum(a * b for a, b in zip(set1, set2))
    magnitude1 = sum(a ** 2 for a in set1) ** 0.5
    magnitude2 = sum(b ** 2 for b in set2) ** 0.5
    return dot_product / (magnitude1 * magnitude2)

# Create a graph of articles
def create_article_graph(articles, threshold=0.5, perm_size=128):
    """
    Create and visualize a graph of articles based on similarity.

    :param articles: List of article contents (strings)
    :param threshold: Similarity threshold to connect nodes
    :param perm_size: Number of permutations for MinHash
    """
    # Generate MinHash for each article
    minhashes = []
    for article in articles:
        tokens = set(article.split())
        minhash = MinHash(num_perm=perm_size)
        for token in tokens:
            minhash.update(token.encode('utf8'))
        minhashes.append((article, minhash))
    
    # Create a graph
    G = nx.Graph()
    for i, (article1, m1) in enumerate(minhashes):
        G.add_node(i, label=article1)  # Add each article as a node
        for j, (article2, m2) in enumerate(minhashes):
            if i < j:  # Avoid duplicate comparisons
                sim = m1.jaccard(m2)
                if sim >= threshold:  # Add an edge if similarity exceeds threshold
                    G.add_edge(i, j, weight=sim)
    
    # Visualize the graph
    pos = nx.spring_layout(G)  # Layout for better visualization
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.2f}" for k, v in labels.items()})
    plt.title("Article Similarity Graph")
    plt.show()



create_article_graph(org_articles, threshold=0.3)
    
#%%
# Output one representative article from each bucket
print(f"Number of unique buckets: {len(buckets)}\n")
for bucket_id, representative_article in buckets.items():
    print(f"Bucket {bucket_id}")  # Print first 100 characters

